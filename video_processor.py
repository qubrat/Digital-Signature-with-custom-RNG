from urllib import request
from moviepy.editor import *
import m3u8
import streamlink
from os import remove


def get_stream(url):
    # Get upload chunk url

    streams = streamlink.streams(url)
    stream_url = streams["best"]

    m3u8_obj = m3u8.load(stream_url.args["url"])
    return m3u8_obj.segments[0]


def dl_stream(url, filename, chunks):
    pre_time_stamp = 0
    os.mkdir('source')
    for i in range(chunks + 1):
        stream_segment = get_stream(url)
        cur_time_stamp = \
            stream_segment.program_date_time.strftime("%Y%m%d-%H%M%S")

        if pre_time_stamp == cur_time_stamp:
            pass
        else:
            # print(cur_time_stamp)
            file = open('source/{}_{}.mp4'.format(filename, i), 'ab+')
            with request.urlopen(stream_segment.uri) as response:
                html = response.read()
                file.write(html)
            pre_time_stamp = cur_time_stamp
            print('File {} saved.'.format(file.name))


def merge_files():
    videos = []
    for root, dirs, files in os.walk("source"):
        for file in files:
            if os.path.splitext(file)[1] == '.mp4':
                filepath = os.path.join(root, file)
                video = VideoFileClip(filepath)
                videos.append(video)
    final_clip = concatenate_videoclips(videos)
    final_clip.to_videofile("video.mp4", fps=30)

    for root, dirs, files in os.walk("source"):
        for file in files:
            if os.path.splitext(file)[1] == '.mp4':
                filepath = os.path.join(root, file)
                remove(filepath)
    os.rmdir('source')


base_url = "https://www.youtube.com/watch?v=h3MuIUNCCzI"
name = "video_chunk"
iterations = 15


def get_video():
    dl_stream(base_url, name, iterations)
    merge_files()
    return 'video.mp4'


if __name__ == '__main__':
    get_video()
