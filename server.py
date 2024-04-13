import asyncio
import websockets
from websockets.exceptions import ConnectionClosed
from loguru import logger

connected_clients = set()

async def handle_client(websocket, path):
    logger.debug(f"{path} connected")
    connected_clients.add(websocket)
    try:
        while True:
            message = await websocket.recv()
            await asyncio.sleep(3)
            await websocket.send(message)
    except ConnectionClosed:
        logger.debug(f"{path} disconnected")

async def get_user_input():
    loop = asyncio.get_event_loop()
    user_input = await loop.run_in_executor(None, input, "Enter something: ")
    for ws in connected_clients:
            await ws.send(user_input)
    return user_input

async def main():
    async with websockets.serve(handle_client, "localhost", 8765):
        # asyncio.create_task(send_input())
        # print('go forever')
        try:
            while True:
                user_input = await get_user_input()
                print("You entered:", user_input)
        except KeyboardInterrupt:
            logger.debug("Keyboard interrupt. Main function closing")

asyncio.run(main())
