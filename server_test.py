from better_websocket.classes import Server
import asyncio

if __name__ == "__main__":
    server = Server()
    asyncio.run(server.main())