from better_websocket.classes import Server, Client
import multiprocessing, queue, asyncio

from loguru import logger

class BetterServerController():
    def __init__(self):
        self.q = multiprocessing.Queue()
        self.process = multiprocessing.Process(target=self.start_server, args=(self.q,))
        self.process.start()

    def start_server(self, queue):
        server = BetterServer(queue)
        server.run()

class BetterServer(Server):
    def __init__(self, queue):
        super().__init__()
        self.queue = queue
    
    # def process_input(self, input):
    #     # return super().process_input(input)
    #     logger.debug(f"Process this: {input}")

    async def send(self):
        try:
            message = self.queue.get_nowait()
            logger.debug(message)
            return message
        except queue.Empty:
            # logger.debug("Queue was empty")
            await asyncio.sleep(0.3)
            # return "Nope"


class BetterClientController():
    def __init__(self):
        self.q = multiprocessing.Queue()
        self.process = multiprocessing.Process(target=self.start_client, args=(self.q,))
        self.process.start()

    def start_client(self, queue):
        client = BetterClient(queue)
        client.run()

class BetterClient(Client):
    def __init__(self, queue):
        super().__init__()
        self.queue = queue

    async def send(self):
        try:
            message = self.queue.get_nowait()
            logger.debug(message)
            return message
        except queue.Empty:
            # logger.debug("Queue was empty")
            await asyncio.sleep(0.3)
            # return "Nope"