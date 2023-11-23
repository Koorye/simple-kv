import argparse
import logging
import threading
import uvicorn
from fastapi import FastAPI
from rpyc.utils.server import ThreadedServer
from typing import Dict

from service import KVService


app = FastAPI()


@app.get('/')
def handle_ping():
    return 'pong!'


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
    parser.add_argument('--port', type=int)
    parser.add_argument('--all-ports', type=int, nargs='+')
    args = parser.parse_args()
    port = args.port
    all_ports = args.all_ports
    
    rpc_port = port + 10000
    all_rpc_ports = [port + 10000 for port in all_ports]
    
    service = KVService(rpc_port, all_rpc_ports)

    print(f'Starting RPC Server on port {rpc_port}')
    rpc_server = ThreadedServer(service=service, port=rpc_port,
                                protocol_config={'allow_all_attrs': True})
    rpc_server.logger.setLevel(logging.WARN)
    t = threading.Thread(target=rpc_server.start, daemon=True)
    t.start()
    
    print(f'Starting HTTP Server on {port}')
    uvicorn.run(app, host='0.0.0.0', port=port, log_level='info')
