import argparse
import logging
import threading
import uvicorn
from fastapi import FastAPI
from rpyc.utils.server import ThreadedServer
from typing import Dict

from service import KVService

HTTP_PORT = 80
RPC_PORT = 5000

app = FastAPI()


@app.post('/')
def handle_set(data: Dict):
    for k, v in data.items():
        return service.handle_http_request('set', k, v)


@app.get('/{key}')
def handle_get(key):
    return service.handle_http_request('get', key)


@app.delete('/{key}')
def handle_delete(key):
    return service.handle_http_request('delete', key)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', type=str)
    parser.add_argument('--all-hosts', type=str, nargs='+')
    args = parser.parse_args()

    service = KVService(args.host, args.all_hosts, RPC_PORT)

    print(f'Starting RPC Server on {RPC_PORT}')
    rpc_server = ThreadedServer(service=service, port=RPC_PORT, auto_register=False, 
                                protocol_config={'allow_public_attrs': True})
    rpc_server.logger.setLevel(logging.WARN)
    t = threading.Thread(target=rpc_server.start, daemon=True)
    t.start()
    
    print(f'Starting HTTP Server on {HTTP_PORT}')
    uvicorn.run(app, host='0.0.0.0', port=HTTP_PORT, log_level='info')
