import asyncio
import websockets
from websockets.exceptions import ConnectionClosed

from loguru import logger

async def send_routine(ws):
    # TODO: How can I properly break this loop?
    while True:
        try:
            user_input = await get_user_input()
            if user_input == 'quit':
                break
            # logger.debug(f"You entered: {user_input}")
            await ws.send(user_input)
        except websockets.exceptions.ConnectionClosedOK:
            logger.warning('Connection was already closed. Breaking')
            break

async def get_user_input():
    loop = asyncio.get_event_loop()
    user_input = await loop.run_in_executor(None, input, "Enter something: ")
    return user_input

async def receive_routine(ws):
    try:
        while True:
            response = await ws.recv()
            if response == 'quit':
                logger.debug('Quit received')
                break
            logger.debug(f"Received: {response}")
    except ConnectionClosed:
        # TODO: This needs to quit the client
        logger.debug("Server closed connection")
    except asyncio.CancelledError:
        logger.debug("Routine cancelled")


async def main():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        # send_task = asyncio.create_task(send_routine(websocket))
        task = asyncio.create_task(receive_routine(websocket))
        send_task = send_routine(websocket)
        # task = receive_routine(websocket)
        await send_task
        task.cancel()
        logger.debug("End of main reached")
        # await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())