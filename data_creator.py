import random
import sys


class DataCreator:
    def __init__(self, data):
        self.data = data

    def get_random_element(self):
        return random.choice(self.data)

    def execute(self, byte_count):
        random_bytes = b''
        while len(random_bytes) < byte_count:
            element = self.get_random_element()
            random_bytes += element

        return random_bytes
