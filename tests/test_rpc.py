import rpyc


client = rpyc.connect('127.0.0.1', 5000)
print(client.root.handle_rpc_request('set', 'tasks', ['a', 'b', 'c']))
print(client.root.handle_rpc_request('get', 'tasks'))