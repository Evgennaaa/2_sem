import socket
import logging

logging.basicConfig(filename='server.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

data_file = 'user_data.txt'

def save_user_data(ip, name):
    with open(data_file, 'a') as file:
        file.write(f'{ip} {name}\n')

def get_user_name(ip):
    with open(data_file, 'r') as file:
        for line in file:
            data = line.strip().split(' ')
            if data[0] == ip:
                return data[1]
    return None

def handle_client(client_socket, client_address):
    ip = client_address[0]
    name = get_user_name(ip)

    if name is None:
        client_socket.send('Как вас зовут? '.encode())
        name_data = client_socket.recv(1024).decode().strip()
        save_user_data(ip, name_data)
        client_socket.send(f'Добро пожаловать, {name_data}!'.encode())
    else:
        client_socket.send(f'Привет, {name}!'.encode())

    client_socket.close()

def run_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('localhost', 0))
    port = sock.getsockname()[1]  # Получаем номер порта
    logging.info(f"Сервер слушает порт: {port}")

    sock.listen(1)

    logging.info("Запуск сервера")

    while True:
        client_socket, client_address = sock.accept()
        logging.info("Подключение клиента: %s", client_address)

        handle_client(client_socket, client_address)

if __name__ == '__main__':
    run_server()