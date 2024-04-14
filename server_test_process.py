
from experimental.classes import BetterServerController

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