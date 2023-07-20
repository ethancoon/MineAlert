from mctools import QUERYClient

# The function to find basic stats for the server using the QUERY protocol
def query_basic_stats(serverAddress, serverPort):
    query = QUERYClient(serverAddress, serverPort)
    return query.get_basic_stats()

# The function to find more detailed stats for the server using the QUERY protocol
def query_advanced_stats(serverAddress, serverPort):
    query = QUERYClient(serverAddress, serverPort)
    return query.get_full_stats()