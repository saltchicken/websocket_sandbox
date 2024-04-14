from better_websocket.classes import Client
import asyncio
import multiprocessing, queue

from loguru import logger

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

def start_client(queue):
    client = BetterClient(queue)
    client.run()

def client_init():
    q = multiprocessing.Queue()
    process = multiprocessing.Process(target=start_client, args=(q,))
    return process, q

if __name__ == "__main__":
    process, q = client_init()
    process.start()
    try:
        while True:
            user_input = input()
            q.put(user_input)
    except KeyboardInterrupt:
        pass
    process.join()