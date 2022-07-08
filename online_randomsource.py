from os import remove
from urllib import request
from m3u8 import load
from time import sleep
import streamlink
import TRNG


class Source:
    def __init__(self):
        self.url = "https://www.youtube.com/watch?v=h3MuIUNCCzI"
        self.filename = "live"

    def get_stream(self):
        # Get upload chunk url

        streams = streamlink.streams(self.url)
        stream_url = streams["best"]

        m3u8_obj = load(stream_url.args["url"])
        return m3u8_obj.segments[0]

    def dl_stream(self, filename):
        # Download each chunk

        stream_segment = self.get_stream()
        file = open(filename + "_" + "chunk" + ".mp4", "ab+")
        with request.urlopen(stream_segment.uri) as response:
            html = response.read()
            file.write(html)
        return file.name

    def execute(self, byte_count):
        random_bytes = b''
        print("Hello, I'm generating random bits...")
        while len(random_bytes) < byte_count:
            filepath = self.dl_stream(self.filename)
            random_bytes += TRNG.trng_algorithm(filepath, byte_count)
            length = len(random_bytes)
            if length >= byte_count:
                print("Done.")
                sleep(0.5)
                remove("audio.wav")
                remove("live_chunk.mp4")
                return random_bytes
            # print(random_bytes)
            sleep(0.5)
            remove("audio.wav")
            remove("live_chunk.mp4")
