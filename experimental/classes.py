from better_websocket.classes import Server, Client
import multiprocessing, queue, asyncio

from loguru import logger

class BetterServerController():
    def __init__(self):
        self._q = multiprocessing.Queue()
        self._process = multiprocessing.Process(target=self.start_server)
        self._process.start()

    def start_server(self):
        self.server = BetterServer(self._q)
        self.server.run()

    def put(self, message):
        self._q.put(message)


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
        self._q = multiprocessing.Queue()
        self._process = multiprocessing.Process(target=self.start_client)
        self._process.start()

    def start_client(self):
        self.client = BetterClient(self._q)
        self.client.run()

    def put(self, message):
        self._q.put(message)

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