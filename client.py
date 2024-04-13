import asyncio
import websockets
from websockets.exceptions import ConnectionClosed

async def hello():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        try:
            while True:
                await websocket.send("Hello, WebSocket!")
                response = await websocket.recv()
                print(f"Received: {response}")
        except ConnectionClosed:
                print("Client disconnected")

asyncio.run(hello())
