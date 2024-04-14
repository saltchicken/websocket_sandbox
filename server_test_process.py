from better_websocket.classes import Server
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



if __name__ == "__main__":
    server_controller = BetterServerController()
    # server_controller.process.start()
    try:
        while True:
            user_input = input()
            server_controller.q.put(user_input)
    except KeyboardInterrupt:
        pass
    server_controller.process.join()