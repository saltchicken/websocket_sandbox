import asyncio
import websockets
from websockets.exceptions import ConnectionClosed

from loguru import logger

async def input_routine(ws):
    # TODO: How can I properly break this loop?
    while True:
        user_input = await get_user_input()
        # logger.debug(f"You entered: {user_input}")
        await ws.send(user_input)

async def get_user_input():
    loop = asyncio.get_event_loop()
    user_input = await loop.run_in_executor(None, input, "Enter something: ")
    return user_input

async def output_routine(ws):
    try:
        while True:
            response = await ws.recv()
            logger.debug(f"Received: {response}")
    except ConnectionClosed:
            # TODO: This needs to quit the client
            logger.debug("Client disconnected")

async def main():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        asyncio.create_task(input_routine(websocket))
        asyncio.create_task(output_routine(websocket))
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())