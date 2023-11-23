import hashlib
import rpyc
from fastapi import HTTPException
from rpyc import Service

from logger import Logger
from store import KVStore


_HOST = '127.0.0.1'


class KVService(Service):
    def __init__(self, 
                 port,
                 all_ports):
        self.port = port
        self.all_ports = all_ports
        
        self.logger = Logger(f'log.txt')
        self.store = KVStore(self.logger)
    
    def handle_http_request(self, operation, k, v=None):
        logger = self.logger
        target_port = self._select_rpc(k)

        if self._is_local(target_port):
            logger.info(f'send operation "{operation} {k} {v}" to local')
            result = self.exposed_handle_rpc_request(operation, k, v)
        else:
            logger.info(f'send operation "{operation} {k} {v}" to {target_port}')
            with rpyc.connect(_HOST, port=target_port) as conn:
                result = conn.root.handle_rpc_request(operation, k, v)
        
        if operation == 'get':
            if result is None:
                raise HTTPException(404)
            result = eval(result)
        
        return result
    
    def exposed_handle_rpc_request(self, operation, k, v=None):
        if operation == 'set':
            return self.do_set(k, v)
        elif operation == 'get':
            return self.do_get(k)
        else:
            return self.do_delete(k)

    def do_set(self, k, v):
        self.logger.info(f'handle operation: set {k}, {v}')
        self.store.set(k, v) # return None
        
    def do_get(self, k):
        self.logger.info(f'handle operation: get {k}')
        return self.store.get(k)
    
    def do_delete(self, k):
        self.logger.info(f'handle operation: delete {k}')
        return self.store.delete(k)

    def _select_rpc(self, k):
        id_ = self._hash(k) % len(self.all_ports)
        self.logger.info(f'hash id {id_}')
        return self.all_ports[id_]

    def _is_local(self, port):
        return port == self.port

    def _hash(self, x):
        md5_machine = hashlib.md5()
        md5_machine.update(x.encode('utf-8'))
        md5_hash_string = md5_machine.hexdigest()
        return int(md5_hash_string, 16)
