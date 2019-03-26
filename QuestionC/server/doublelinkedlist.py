from pympler import asizeof

class Node:
    def __init__(self, key, value, expiry):
        self.key = key
        self.value = value
        self.expiry = expiry
        self.next = None
        self.prev = None

    def getSize(self):
        return asizeof.asizeof(self)