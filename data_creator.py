import random


class DataCreator:
    def __init__(self, data):
        self.data = data

    def get_random_element(self):
        return random.choice(self.data)

    def execute(self, byte_count):
        random_bytes = b''
        print("Hello, I'm generating random bits...")
        while len(random_bytes) < byte_count:
            random_bytes += self.get_random_element()
            return random_bytes
