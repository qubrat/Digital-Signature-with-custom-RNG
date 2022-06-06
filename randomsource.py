import urllib
import m3u8
import streamlink
import TRNG


# https://www.youtube.com/watch?v=h3MuIUNCCzI - LIVE 24/7


def get_stream(url):
    # Get upload chunk url

    streams = streamlink.streams(url)
    stream_url = streams["best"]

    m3u8_obj = m3u8.load(stream_url.args['url'])
    return m3u8_obj.segments[0]


def dl_stream(url, filename):
    # Download each chunk

    stream_segment = get_stream(url)
    cur_time_stamp = \
        stream_segment.program_date_time.strftime("%Y%m%d-%H%M%S")

    print(cur_time_stamp)
    file = open(filename + '_' + str(cur_time_stamp) + '.mp4', 'ab+')
    with urllib.request.urlopen(stream_segment.uri) as response:
        html = response.read()
        file.write(html)
    TRNG.trng_algorithm(file.name)


url = "https://www.youtube.com/watch?v=h3MuIUNCCzI"


def execute():
    print("Hello, I'm working...")
    dl_stream(url, "src/live")
