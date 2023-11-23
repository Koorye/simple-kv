class KVStore(object):
    def __init__(self, logger):
        self.store = dict()
        self.logger = logger
    
    def set(self, k, v):
        self.logger.info(f'all: {self.store}')
        if k not in self.store:
            self.store[k] = str(v)
            return 'ok'
        else:
            self.store[k] = str(v)
            return 'overwrite'
    
    def get(self, k):
        self.logger.info(f'all: {self.store}')
        if k not in self.store:
            return None
        else:
            return str({k: self.store[k]})

    def delete(self, k):
        self.logger.info(f'all: {self.store}')
        if k not in self.store:
            return 0
        else:
            del self.store[k]
            return 1
