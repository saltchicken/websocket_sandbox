import asyncio
import websockets
from websockets.exceptions import ConnectionClosed

from loguru import logger

connected_server = None

async def input_routine(connected_server):
    # TODO: How can I properly break this loop?
    while True:
        user_input = await get_user_input(connected_server)
        # logger.debug(f"You entered: {user_input}")
        if connected_server is not None:
            # logger.debug(f"Sending: {user_input}")
            await connected_server.send(user_input)

async def get_user_input(connected_server):
    loop = asyncio.get_event_loop()
    user_input = await loop.run_in_executor(None, input, "Enter something: ")
    return user_input

async def output_routine(connected_server):
    try:
        while True:
            response = await connected_server.recv()
            logger.debug(f"Received: {response}")
    except ConnectionClosed:
            # TODO: This needs to quit the client
            logger.debug("Client disconnected")

async def main():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        connected_server = websocket
        asyncio.create_task(input_routine(connected_server))
        asyncio.create_task(output_routine(connected_server))
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())