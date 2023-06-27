import socket
import threading
import queue

def handle_client(client_socket, address, clients):
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        message = data.decode()
        print(f"Сообщение от клиента {address}: {message}")
        for client in clients:
            if client != client_socket:
                client.send(data)
    client_socket.close()
    clients.remove(client_socket)

def start_server(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', port))
    server_socket.listen(5)

    print(f"Сервер запущен и прослушивает порт {port}")

    clients = []

    command_queue = queue.Queue()

    is_listening = True

    def listen_for_clients():
        while is_listening:
            try:
                client_socket, address = server_socket.accept()
                print(f"Подключение клиента {address[0]}:{address[1]}")
                clients.append(client_socket)
                client_thread = threading.Thread(target=handle_client, args=(client_socket, address, clients))
                client_thread.start()
            except socket.error as e:
                if not is_listening:
                    break
                else:
                    raise e

    listen_thread = threading.Thread(target=listen_for_clients)
    listen_thread.start()

    while True:
        if not command_queue.empty():
            command = command_queue.get()
            if command == "pause":
                server_socket.close()
                is_listening = False
                print("Прослушивание порта приостановлено")
            elif command == "resume":
                server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                server_socket.bind(('localhost', port))
                server_socket.listen(5)
                is_listening = True
                print(f"Сервер возобновил прослушивание порта {port}")
            elif command == "log":
                print("Логи:")
                for client in clients:
                    print(f"Клиент {client.getpeername()}")
            elif command == "clear":
                clients.clear()
                print("Логи очищены")

        user_input = input("Введите команду: ")
        if user_input == "exit":
            break
        elif user_input in ["pause", "resume", "log", "clear"]:
            command_queue.put(user_input)

    for client in clients:
        client.close()

    server_socket.close()

start_server(8080)
