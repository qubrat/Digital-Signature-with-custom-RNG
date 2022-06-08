from os import remove
from urllib import request
from m3u8 import load
from time import sleep
import streamlink
import TRNG

url = "https://www.youtube.com/watch?v=h3MuIUNCCzI"  # FRANCE 24 English – LIVE - 24/7 stream


def get_stream(url):
    # Get upload chunk url

    streams = streamlink.streams(url)
    stream_url = streams["best"]

    m3u8_obj = load(stream_url.args["url"])
    return m3u8_obj.segments[0]


def dl_stream(url, filename):
    # Download each chunk

    stream_segment = get_stream(url)
    cur_time_stamp = stream_segment.program_date_time.strftime("%Y%m%d-%H%M%S")

    print(cur_time_stamp)
    file = open(filename + "_" + "chunk" + ".mp4", "ab+")
    with request.urlopen(stream_segment.uri) as response:
        html = response.read()
        file.write(html)
    TRNG.trng_algorithm(file.name)


def execute():
    print("Hello, I'm generating random bits...")
    dl_stream(url, "live")
    print("Done.")
    sleep(3)
    remove("audio.wav")
    remove("live_chunk.mp4")
