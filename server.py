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

# async def send_message(message):
#     # Iterate over connected clients and send the message to each one
#     for client in connected_clients:
#         await client.send(message)

# async def send_input():
#     while True:
#         message = input("Enter message to send to clients: ")
#         for ws in connected_clients:
#             await ws.send(message)

async def get_user_input():
    loop = asyncio.get_event_loop()
    user_input = await loop.run_in_executor(None, input, "Enter something: ")
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
        # await asyncio.Future()  # run forever
    # server = await websockets.serve(echo, "localhost", 8765)
    # asyncio.create_task(send_input())
    # await server.wait_closed()
        # while True:
        #     message = input("Enter message to send (or 'quit' to exit): ")
        #     if message == 'quit':
        #         break
        #     await send_message(message)

asyncio.run(main())
