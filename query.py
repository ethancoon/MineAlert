from mctools import QUERYClient

def query_basic_stats(serverAddress, serverPort):
    query = QUERYClient(serverAddress, serverPort)
    return query.get_basic_stats()

def query_advanced_stats(serverAddress, serverPort):
    query = QUERYClient(serverAddress, serverPort)
    return query.get_full_stats()