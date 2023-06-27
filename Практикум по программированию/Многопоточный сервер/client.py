import socket
import threading

def receive_messages(client_socket):
    while True:
        message = client_socket.recv(1024).decode()
        print("Новое сообщение:", message)

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 8080))

    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()

    while True:
        message = input("Введите сообщение (для выхода введите 'exit'): ")
        if message == 'exit':
            break
        message = "@all: " + message
        client_socket.send(message.encode())

    client_socket.close()

start_client()
