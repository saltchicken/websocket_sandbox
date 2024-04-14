from better_websocket.experimental import Controller

if __name__ == "__main__":
    server_controller = Controller(server_bool=True)
    try:
        while True:
            # user_input = input()
            # server_controller.put(user_input)
            received = server_controller.get()
            print(received)
    except KeyboardInterrupt:
        pass
    # server_controller.process.join()