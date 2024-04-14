from better_websocket.classes import Client
import asyncio

class BetterClient(Client):
    def __init__(self):
        super().__init__()

if __name__ == "__main__":
    client = Client()
    client.run()