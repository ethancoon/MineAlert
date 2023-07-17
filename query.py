from mcipc.query import Client

def get_basic_stats(serverAddress):
    with Client(serverAddress, 25565) as client:
        return client.stats()