import moviepy.editor as mp
from cv2 import VideoCapture
from numpy import var
import sys
from os import remove

# data amount given in kB
data_amount = 50
filepath = 'video.mp4'


def kB_to_bits(kB):
    return kB * 1024 * 8


def trng_algorithm(filepath, online_flag=0):
    print("Processing given video...")
    audio = mp.AudioFileClip(filepath)
    audio = audio.to_soundarray(nbytes=2, buffersize=1000, fps=44100)
    audio = (audio*10000).flatten().astype(int)
    cap = VideoCapture(filepath)
    frame_number = 1
    cap.set(1, frame_number)
    res, frame = cap.read()  # wczytujemy dane z klatki
    height, width, channels = frame.shape  # pobieramy dane z klatki

    x = int(width / 2)
    y = int(height / 2)

    color_i_1 = (frame[y - 1, x - 1, 2] << 16) + (frame[y - 1, x - 1, 1] << 8) + (frame[y - 1, x - 1, 1])
    color_i_2 = (frame[y - 1, x, 2] << 16) + (frame[y - 1, x, 1] << 8) + (frame[y - 1, x, 1])
    color_i_3 = (frame[y - 1, x + 1, 2] << 16) + (frame[y - 1, x + 1, 1] << 8) + (frame[y - 1, x + 1, 1])
    color_i_4 = (frame[y, x - 1, 2] << 16) + (frame[y, x - 1, 1] << 8) + (frame[y, x - 1, 1])
    color_i_5 = (frame[y, x, 2] << 16) + (frame[y, x, 1] << 8) + (frame[y, x, 1])
    color_i_6 = (frame[y, x + 1, 2] << 16) + (frame[y, x + 1, 1] << 8) + (frame[y, x + 1, 1])
    color_i_7 = (frame[y + 1, x - 1, 2] << 16) + (frame[y + 1, x - 1, 1] << 8) + (frame[y + 1, x - 1, 1])
    color_i_8 = (frame[y + 1, x, 2] << 16) + (frame[y + 1, x, 1] << 8) + (frame[y + 1, x, 1])
    color_i_9 = (frame[y + 1, x + 1, 2] << 16) + (frame[y + 1, x + 1, 1] << 8) + (frame[y + 1, x + 1, 1])

    color_i = int(
        (color_i_1 + color_i_2 + color_i_3 + color_i_4 + color_i_5 + color_i_6 + color_i_7 + color_i_8 + color_i_9) / 9)
    # print (color_i)

    x = int((color_i % (width / 2)) + (width / 4))
    y = int((color_i % (height / 2)) + (height / 4))
    # print(x,y)

    bit_result = []
    vt = int(var(frame[:, :, :]) / 2)
    threshold = 100
    watchdog = 0
    K = 2000
    i = 1
    j = 0
    runcnt = 0
    control = 1
    r_1 = 0
    g_1 = 0
    b_1 = 0
    r_2 = 0
    g_2 = 0
    b_2 = 0
    skip_count = 0

    while len(bit_result) < kB_to_bits(data_amount):
        r = frame[y, x, 2]
        g = frame[y, x, 1]
        b = frame[y, x, 0]

        if (((r - r_1) ** 2) + ((g - g_1) ** 2) + ((b - b_1) ** 2)) < vt:
            x = (x + (r ^ g) + 1) % width
            y = (y + (g ^ b) + 1) % height
            watchdog += 1
            if watchdog > threshold:
                frame_number += 1
                cap.set(1, frame_number)
                res, frame = cap.read()
                try:
                    vt = int(var(frame[:, :, :]) / 2)
                except TypeError:
                    print("\nEmpty frame, skipping to the next one.")
                    continue
                watchdog = 0
                skip_count += 1
                sys.stdout.write("\rSkipped %i frames" % skip_count)
                sys.stdout.flush()
                continue
            else:
                continue
        else:
            if control < 1000:
                # print("mixing bits")
                sn_1 = audio[int(j + 10 + ((r * i) + (g << 2) + b + runcnt) % (K / 2))]
                sn_2 = audio[int(j + 15 + ((r * i) + (g << 3) + b + runcnt) % (K / 2))]
                sn_3 = audio[int(j + 20 + ((r * i) + (g << 4) + b + runcnt) % (K / 2))]
                sn_4 = audio[int(j + 5 + ((r * i) + (g << 1) + b + runcnt) % (K / 2))]
                sn_5 = audio[int(j + 25 + ((r * i) + (g << 5) + b + runcnt) % (K / 2))]

                bit_i = 1 & (r ^ g ^ b ^ r_1 ^ b_1 ^ g_1 ^ r_2 ^ g_2 ^ b_2 ^ sn_1 ^ sn_2 ^ sn_3 ^ sn_4 ^ sn_5)
                bit_result.append(str(bit_i))
                r_1 = r
                g_1 = g
                b_1 = b
                i += 1
                control += 1
            else:
                control = 0
                runcnt += 1
            if i >= 8:
                r_2 = r
                g_2 = g
                b_2 = b
                i = 0
            x = (((r ^ x) << 4) ^ (g ^ y)) % width
            y = (((g ^ x) << 4) ^ (b ^ y)) % height
            j += K / 1000
    print('\n')
    result = []
    print('Preparing data...')
    for i in range(0, len(bit_result), 8):
        tmp = "".join(bit_result[i:i + 8])
        result.append("%s\n" % str(int(tmp, 2)))

    if online_flag == 1:
        remove(filepath)
    print('Done')
    return result


if __name__ == "__main__":
    trng_algorithm(filepath)
