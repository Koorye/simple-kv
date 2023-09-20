import rpyc


conn = rpyc.connect('127.0.0.1', 19527)
print(conn.root.set('name', 'koorye'))
print(conn.root.get('name'))
print(conn.root.delete('name'))
print(conn.root.get('name'))
