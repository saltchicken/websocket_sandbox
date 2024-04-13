from better_websocket.classes import Client
import asyncio

if __name__ == "__main__":
    client = Client()
    asyncio.run(client.main())