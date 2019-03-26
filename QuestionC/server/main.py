import rpyc
import config
import json
import time
from doublelinkedlist import *
import rpyc
from rpyc.utils.server import ThreadedServer

# The cached data needs to be accessed by all instances of LRUCacheServer
# Defined as singleton to make it all simpler
class Data:
    total_memory = 0
    itemsDic = dict()
    head = None
    tail = None

    instance = None
    def __new__(c):
        if not c.instance:
            c.instance = super().__new__(c)
        return c.instance

# Accessed by each instance of LRUCacheServer (1 client = 1 instance)
class LRUCacheServer(rpyc.Service):

    def __init__(self):
        self.d = Data()
        for server in config.replicated_servers:
            try:
                server['connection'] = rpyc.connect(server['host'], server['port'])
            except ConnectionError:
                pass

    # Store an item in the cache
    def _setItem(self, value, replicate = True):
        value = json.loads(value)
        node = Node(value[0], value[1], time.time() + config.expiry)
        item_size = node.getSize()

        if node.key in self.d.itemsDic:
            self.d.total_memory -= self.d.itemsDic[node.key].getSize()
            self._removeItem(self.d.itemsDic[node.key])

        # Remove oldest items until there's enough capacity for incoming item
        while self.d.total_memory + item_size > config.memory:
            if not self.d.tail:
                raise Exception('Not enough memory available')

            self.d.total_memory -= self.d.tail.getSize()
            del self.d.itemsDic[self.d.tail.key]
            self._removeItem(self.d.tail)
            
        self.d.total_memory += item_size

        self._addItem(node)
        if replicate:
            self._replicateItem(node)

        print('Added ' + str(item_size) + ' bytes, new size: ' + str(self.d.total_memory) + ' bytes')

    # Client requests to store an item
    def exposed_setItem(self, value):
        self._setItem(value)
        
    # Other server requests an item to be replicated on this server
    def exposed_setItemByReplication(self, value):
        self._setItem(value, False)

    # Client fetches an item
    def exposed_getItem(self, key):
        if key in self.d.itemsDic:
            node = self.d.itemsDic[key]

            # check cache expiry
            if node.expiry < time.time():
                self._removeItem(node)
                del self.d.itemsDic[key]
                return None

            # Move the item to self.d.head
            self._removeItem(node)
            node.prev = self.d.head
            if self.d.head:
                self.d.head.next = node
            self.d.head = node

            return node.value
        return None

    # Remove item from the double linked list
    def _removeItem(self, node):
        if node.next:
            node.next.prev = node.prev
        if node.prev:
            node.prev.next = node.next
        if node == self.d.head:
            self.d.head = node.prev
        if node == self.d.tail:
            self.d.tail = node.next

    # Add an item to the hashtable and to the head of the linked list
    def _addItem(self, node):
        self.d.itemsDic[node.key] = node

        if not self.d.head:
            self.d.head = node
            self.d.tail = node
        else:
            self.d.head.next = node
            self.d.head = node

    # Replicate an item to all servers across network
    def _replicateItem(self, node):
        for server in config.replicated_servers:
            if 'connection' in server:
                server['connection'].root.setItemByReplication(json.dumps((node.key, node.value)))



if __name__ == "__main__":
    server = ThreadedServer(LRUCacheServer, port = config.port)
    server.start()