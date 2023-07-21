from mctools import QUERYClient

# The function to find basic stats for the server using the QUERY protocol
def query_basic_stats(serverAddress, serverPort):
    try:
        query = QUERYClient(serverAddress, serverPort, timeout = 10)
        return query.get_basic_stats()
    except Exception as e:
        print(e)
        return "The server is offline or I am searching the wrong address :("


# The function to find more detailed stats for the server using the QUERY protocol
def query_advanced_stats(serverAddress, serverPort):
    try:
        query = QUERYClient(serverAddress, serverPort, timeout = 10)
        return query.get_full_stats()
    except Exception as e:
        print(e)
        return "The server is offline or I am searching the wrong address :("