from better_websocket.classes import Server, Client
import multiprocessing, queue, asyncio

from loguru import logger

class Controller():
    def __init__(self):
        self._send_q = multiprocessing.Queue()
        self._receive_q = multiprocessing.Queue()
    
    def put(self, message):
        self._send_q.put(message)

    def get(self):
        message = self._receive_q.get()
        return message

class BetterServerController(Controller):
    def __init__(self):
        super().__init__()
        self._process = multiprocessing.Process(target=self.start_server)
        self._process.start()

    def start_server(self):
        self.server = BetterServer(self._send_q, self._receive_q)
        self.server.run()

class BetterClientController(Controller):
    def __init__(self):
        super().__init__()
        self._process = multiprocessing.Process(target=self.start_client)
        self._process.start()

    def start_client(self):
        self.client = BetterClient(self._send_q, self._receive_q)
        self.client.run()


class BetterServer(Server):
    def __init__(self, send_q, receive_q):
        super().__init__()
        self.send_q = send_q
        self.receive_q = receive_q
    
    # async def process_input(self, input):
    #     # return super().process_input(input)
    #     logger.debug(f"ADding to queue: {input}")
    #     await self.queue.put(input)

    async def send(self):
        try:
            message = self.send_q.get_nowait()
            logger.debug(message)
            return message
        except queue.Empty:
            # logger.debug("Queue was empty")
            await asyncio.sleep(0.3)
            # return "Nope"




class BetterClient(Client):
    def __init__(self, send_q, receive_q):
        super().__init__()
        self.send_q = send_q
        self.receive_q = receive_q

    async def process_input(self, input):
        # return super().process_input(input)
        logger.debug(f"Client received: {input}")
        return True
        # await self.queue.put(input)
        # print('complet')

    async def send(self):
        try:
            message = self.send_q.get_nowait()
            logger.debug(message)
            return message
        except queue.Empty:
            # logger.debug("Queue was empty")
            await asyncio.sleep(0.3)
            # return "Nope"