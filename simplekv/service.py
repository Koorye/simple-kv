import rpyc
from fastapi import HTTPException
from rpyc import Service

from logger import Logger
from store import KVStore


class KVService(Service):
    def __init__(self, 
                 host,
                 hosts,
                 rpc_port):
        self.host = host
        self.hosts = hosts
        self.rpc_port = rpc_port
        
        self.logger = Logger(f'logs/log.txt')
        self.store = KVStore()
    
    def handle_http_request(self, operation, k, v=None):
        logger = self.logger
        target_rpc_host = self._select_rpc(k)

        if self._is_local(target_rpc_host):
            logger.info('send operation to local')
            result = self.exposed_handle_rpc_request(operation, k, v)
        else:
            logger.info(f'send operation to {target_rpc_host}')
            conn = rpyc.connect(target_rpc_host, port=self.rpc_port)
            result = conn.root.handle_rpc_request(operation, k, v)
        
        if operation == 'get' and result is None:
            raise HTTPException(404)
        
        return result
    
    def exposed_handle_rpc_request(self, operation, k, v=None):
        func = getattr(self, 'do_' + operation)
        return func(k, v) if v is not None else func(k)

    def do_set(self, k, v):
        self.logger.info(f'handle operation: set {k}, {v}')
        return self.store.set(k, v)
        
    def do_get(self, k):
        self.logger.info(f'handle operation: get {k}')
        return self.store.get(k)
    
    def do_delete(self, k):
        self.logger.info(f'handle operation: delete {k}')
        return self.store.delete(k)

    def _select_rpc(self, k):
        id_ = hash(k) % len(self.hosts)
        return self.hosts[id_]

    def _is_local(self, host):
        return host == self.host
