import random
import sys


class DataCreator:
    def __init__(self, data):
        self.data = data

    def get_random_element(self):
        return random.choice(self.data)

    def execute(self, byte_count):
        counter = 0
        random_bytes = b''
        while len(random_bytes) <= byte_count:
            random_bytes += self.get_random_element().encode('utf-8')
            counter += 1
            sys.stdout.write("\rFunction called %i times" % counter)
            sys.stdout.flush()
        return random_bytes
