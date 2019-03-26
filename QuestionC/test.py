from client.main import *
import time

# List of cache servers.
# Weight is based on distance from client to server
servers = [
    { "host": "localhost", "port": 1337, "weight": 5 },
    { "host": "localhost", "port": 1338, "weight": 3 },
]


cache = LRUCacheClient(servers)


cache.set('key1', 'value1')
cache.set('key2', 123456.789)
cache.set('key3', ("tuple1", 1234))
cache.set('key4', [{"foo":"bar", "foo2":456}])
cache.set('key5', True)
cache.set('key5', False)

print("key1", cache.get('key1'))
print("key2", cache.get('key2'))
print("key3", cache.get('key3'))
print("key4", cache.get('key4'))
print("key5", cache.get('key5'))

print('Kill closest server... retrying fetch in 5 seconds to test replication')
time.sleep(5)

print("key1", cache.get('key1'))
print("key2", cache.get('key2'))
print("key3", cache.get('key3'))
print("key4", cache.get('key4'))
print("key5", cache.get('key5'))