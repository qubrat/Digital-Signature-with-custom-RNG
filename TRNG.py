import moviepy.editor as mp
import cv2
import wave
import numpy as np
import pytube
# https://www.youtube.com/watch?v=h3MuIUNCCzI - LIVE 24/7


def trng_algorithm():
    # video = mp.AudioFileClip(r"src/trains.mp4")
    # video.write_audiofile(r"src/audio_tr.wav")

    # video = mp.AudioFileClip(r"src/test.mp4")
    # video.write_audiofile(r"src/audio_t.wav")

    video = mp.AudioFileClip(r"src/wind.mp4")
    video.write_audiofile(r"src/audio_w.wav")

    # raw = wave.open('src/audio_tr.wav')
    # raw = wave.open('src/audio_t.wav')
    raw = wave.open('src/audio_w.wav')

    audio = raw.readframes(-1)
    audio = np.frombuffer(audio, dtype="int8")
    audio = np.trim_zeros(audio, 'fb')

    # cap = cv2.VideoCapture("src/trains.mp4")
    # cap = cv2.VideoCapture("src/test.mp4")
    cap = cv2.VideoCapture("src/wind.mp4")
    length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    frameNumber = 1
    cap.set(1, frameNumber)
    res, frame = cap.read()  # wczytujemy dane z klatki
    height, width, channels = frame.shape  # pobieramy dane z klatki

    x = int(width / 2)
    y = int(height / 2)

    R = frame[y, x, 2]
    G = frame[y, x, 1]
    B = frame[y, x, 0]

    # color_xy = (R << 16) + (G << 8) + B
    # print(color_xy)

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
    bit_i = 0
    vt = int(np.var(frame[:, :, :]) / 2)
    threshold = 100
    watchdog = 0
    K = 2000
    i = 1
    j = 0
    runcnt = 0
    control = 1
    R1 = 0
    G1 = 0
    B1 = 0
    R2 = 0
    G2 = 0
    B2 = 0
    SN1 = 0
    SN2 = 0
    SN3 = 0
    SN4 = 0
    SN5 = 0
    hundred_kB = 819200
    skipCount = 0

    while len(bit_result) < hundred_kB:
        R = frame[y, x, 2]
        G = frame[y, x, 1]
        B = frame[y, x, 0]

        if (((R - R1) ** 2) + ((G - G1) ** 2) + ((B - B1) ** 2)) < vt:
            x = (x + (R ^ G) + 1) % width
            y = (y + (G ^ B) + 1) % height
            watchdog += 1
            if watchdog > threshold:
                frameNumber += 1
                cap.set(1, frameNumber)
                res, frame = cap.read()
                vt = int(np.var(frame[:, :, :]) / 2)
                watchdog = 0
                skipCount += 1
                print("frame skipped")
                continue
            else:
                continue
        else:
            if control < 1000:
                # print("mixing bits")
                SN1 = audio[int(j + 10 + ((R * i) + (G << 2) + B + runcnt) % (K / 2))]
                SN2 = audio[int(j + 15 + ((R * i) + (G << 3) + B + runcnt) % (K / 2))]
                SN3 = audio[int(j + 20 + ((R * i) + (G << 4) + B + runcnt) % (K / 2))]
                SN4 = audio[int(j + 5 + ((R * i) + (G << 1) + B + runcnt) % (K / 2))]
                SN5 = audio[int(j + 25 + ((R * i) + (G << 5) + B + runcnt) % (K / 2))]

                bit_i = 1 & (R ^ G ^ B ^ R1 ^ B1 ^ G1 ^ R2 ^ G2 ^ B2 ^ SN1 ^ SN2 ^ SN3 ^ SN4 ^ SN5)
                bit_result.append(str(bit_i))
                R1 = R
                G1 = G
                B1 = B
                i += 1
                control += 1
            else:
                control = 0
                runcnt += 1
            if i >= 8:
                R2 = R
                G2 = G
                B2 = B
                i = 0
            x = (((R ^ x) << 4) ^ (G ^ y)) % width
            y = (((G ^ x) << 4) ^ (B ^ y)) % height
            j += K / 1000

    result = []
    for i in range(0, len(bit_result), 8):
        tmp = ''.join(bit_result[i:i + 8])
        result.append(int(tmp, 2))
        print(result[0])


def execute():
    trng_algorithm()