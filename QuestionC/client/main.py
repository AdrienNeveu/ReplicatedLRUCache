import rpyc
import json

class LRUCacheClient:
    def __init__(self, servers):
        # Sorts the list of servers by descending weight
        self.serverList = sorted(servers, key = lambda i: i['weight'], reverse = True)

    # This method gets the closest responding server
    def _getClosestRespondingServer(self):
        id = 0
        while True:
            if id >= len(self.serverList):
                raise Exception('No cache server available')
            server = self.serverList[id]
            try:
                if not 'connection' in server:
                    server['connection'] = rpyc.connect(server['host'], server['port'])
                    return server
                else:
                    # Existing connection: ping it to check if still alive
                    try:
                        server['connection'].ping('ping',2)
                    except EOFError:
                        pass
                    else:
                        return server
            except ConnectionRefusedError:
                pass
            id += 1

    # Sets a cache item
    def set(self, key, value):
        server = self._getClosestRespondingServer()
        server['connection'].root.setItem(json.dumps((key, value)))

    # Fetches a cache item
    def get(self, key):
        server = self._getClosestRespondingServer()
        return server['connection'].root.getItem(key)
