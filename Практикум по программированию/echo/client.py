import socket

host = input("Введите имя хоста (по умолчанию localhost): ") or 'localhost'
port = int(input("Введите номер порта (по умолчанию 9090): ") or '9090')

sock = socket.socket()
sock.connect((host, port))

data = sock.recv(1024)
print(data.decode('utf-8'))

name = ''

with open('user_data.txt', 'r') as file:
    for line in file:
        data = line.strip().split(' ')
        if data[1]:
            name = data[1]
            break

if not name:
    name = input("Введите ваше имя: ")

sock.send(name.encode('utf-8'))

data = sock.recv(1024)
print(data.decode('utf-8'))

sock.close()
