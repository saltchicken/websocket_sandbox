from better_websocket.classes import Server
import multiprocessing, queue, asyncio

from loguru import logger

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

def start_server(queue):
    server = BetterServer(queue)
    server.run()

def server_init():
    q = multiprocessing.Queue()
    process = multiprocessing.Process(target=start_server, args=(q,))
    return process, q

if __name__ == "__main__":
    process, q = server_init()
    process.start()
    try:
        while True:
            user_input = input()
            q.put(user_input)
    except KeyboardInterrupt:
        pass
    process.join()