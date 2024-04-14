from experimental.classes import Controller

if __name__ == "__main__":
    server_controller = Controller(server_bool=True)
    try:
        while True:
            user_input = input()
            server_controller.put(user_input)
    except KeyboardInterrupt:
        pass
    # server_controller.process.join()