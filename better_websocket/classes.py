import asyncio
import websockets
from websockets.exceptions import ConnectionClosed
from loguru import logger

class Client():
    def __init__(self):
        pass

    async def send_routine(self, ws):
        # TODO: How can I properly break this loop?
        while True:
            try:
                user_input = await self.get_user_input()
                if user_input == 'quit':
                    break
                # logger.debug(f"You entered: {user_input}")
                await ws.send(user_input)
            except websockets.exceptions.ConnectionClosedOK:
                logger.warning('Connection was already closed. Breaking')
                break

    async def get_user_input(self):
        loop = asyncio.get_event_loop()
        user_input = await loop.run_in_executor(None, input, "Enter something: ")
        return user_input

    async def receive_routine(self, ws):
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


    async def main(self):
        uri = "ws://localhost:8765"
        async with websockets.connect(uri) as websocket:
            # send_task = asyncio.create_task(send_routine(websocket))
            task = asyncio.create_task(self.receive_routine(websocket))
            send_task = self.send_routine(websocket)
            # task = receive_routine(websocket)
            await send_task
            task.cancel()
            logger.debug("End of main reached")
            # await asyncio.Future()


class Server():
    def __init__(self):
        self.connected_clients = set()

    async def handle_client(self, websocket, path):
        logger.debug(f"{path} connected")
        self.connected_clients.add(websocket)
        try:
            while True:
                message = await websocket.recv()
                self.process_input(message)
        except ConnectionClosed:
            logger.debug(f"{path} disconnected")
            self.connected_clients.remove(websocket)

    async def send_routine(self):
        # TODO: How can I properly break this loop?
        while True:
            user_input = await self.get_user_input()
            if user_input == 'quit':
                for ws in self.connected_clients:
                    await ws.send('quit')
                break
            # logger.debug("You entered:", user_input)
            for ws in self.connected_clients:
                await ws.send(user_input)

    async def get_user_input(self):
        loop = asyncio.get_event_loop()
        user_input = await loop.run_in_executor(None, input, "Enter something: ")
        return user_input
    
    async def process_input(self, input):
        logger.debug(input)

    async def main(self):
        async with websockets.serve(self.handle_client, "localhost", 8765):
            # asyncio.create_task(send_routine())
            # await asyncio.Future()
            task = self.send_routine()
            result = await task
            logger.debug("End of main reached")