# Python Geo-Distributed and Replicated LRU Cache with Time Expiration

## Dependencies
* **rpyc** - Communication between client/server and server/server
* **pympler** - Accessing asizeof to get real size of items in bytes
* **json** - Items are sent over the network in JSON
* **time** - To check against items lifetimes

## Usage & tests
### Create a server

1. Copy the `server` folder into your different servers
2. Configure config.py with the other servers hostnames/ports, memory pool and cache lifetime
3. Run `python main.py` to launch the server

### Launch tests
1. Update your server list in test.py
2. Run the tests: `python test.py`


## Implementation Details

* The algorithm is based on a linked list and a hash table. The hash table serves as a lookup table when fetching an item while the linked list allows to sort items per access time.

* When the memory overflows, the tail of the linked list is removed until there's enough memory to store the item.

* Everytime an item is stored in a server by the client, the server request the item to be stored in all other servers of the network.

* The distance between the client and server should be calculated by the user and set as a weight (the smallest is the weight, the slower is the ping)

## Features

## Simplicty
Simple integration:

```python
from client.main import *
cache = LRUCacheClient([{'host':'localhost','port':1337, 'weight':1}])

cache.set('key1', 'My Value')
val = cache.get('key1') # > My Value
```

## Resilient to network failures / crashes
Every cached items are replicated over the network.

When setting an item, if the connection has timed out, the client will contact the next closest available server.

## Replication
All servers have the same cached items at nearly all time.

## Locality of reference
The client connects to the closest server (cf. weights in test.py)

## Flexible schema
Items are sent over the network in JSON.

## Cache lifetime
Cache can expire.