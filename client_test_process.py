from experimental.classes import BetterClientController

if __name__ == "__main__":
    client_controller = BetterClientController()
    try:
        while True:
            user_input = input()
            client_controller.put(user_input)
    except KeyboardInterrupt:
        pass
    # client_controller.process.join()