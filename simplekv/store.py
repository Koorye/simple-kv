class KVStore(object):
    def __init__(self):
        self.store = dict()
    
    def set(self, k, v):
        if k not in self.store:
            self.store[k] = v
            return 'ok'
        else:
            self.store[k] = v
            return 'overwrite'
    
    def get(self, k):
        if k not in self.store:
            return None
        else:
            return str({k: self.store[k]})

    def delete(self, k):
        if k not in self.store:
            return 0
        else:
            del self.store[k]
            return 1
