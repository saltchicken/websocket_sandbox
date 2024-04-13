from better_websocket.classes import Server
import asyncio

from loguru import logger

class BetterServer(Server):
    def __init__(self):
        super().__init__()
    
    # def process_input(self, input):
    #     # return super().process_input(input)
    #     logger.debug(f"Process this: {input}")

    # def send(self):
    #     time.sleep(1)
    #     yield "yes"


if __name__ == "__main__":
    server = BetterServer()
    asyncio.run(server.main())