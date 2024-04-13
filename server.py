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
            logger.debug(f"Server received: {message}")
            # await asyncio.sleep(3)
            # await websocket.send(message)
    except ConnectionClosed:
        logger.debug(f"{path} disconnected")
        connected_clients.remove(websocket)

async def input_routine():
    # TODO: How can I properly break this loop?
    while True:
        user_input = await get_user_input()
        if user_input == 'quit':
            break
        # logger.debug("You entered:", user_input)
        for ws in connected_clients:
            await ws.send(user_input)

async def get_user_input():
    loop = asyncio.get_event_loop()
    user_input = await loop.run_in_executor(None, input, "Enter something: ")
    return user_input

async def main():
    async with websockets.serve(handle_client, "localhost", 8765):
        # asyncio.create_task(input_routine())
        # await asyncio.Future()
        task = input_routine()
        result = await task
        logger.debug("End of main reached")

if __name__ == "__main__":
    asyncio.run(main())
