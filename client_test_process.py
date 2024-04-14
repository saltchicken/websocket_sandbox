from better_websocket.experimental import Controller

if __name__ == "__main__":
    client_controller = Controller()
    try:
        while True:
            user_input = input()
            client_controller.put(user_input)
            # received = client_controller.get()
            # print(received)
    except KeyboardInterrupt:
        pass
    # client_controller.process.join()