import socket
import random

def save_keys_to_file(public_key, private_key, filename):
    with open(filename, "w") as file:
        file.write(str(public_key) + '\n')
        file.write(str(private_key))

def load_keys_from_file(filename):
    with open(filename, "r") as file:
        public_key_str = file.readline().strip()
        private_key_str = file.readline().strip()
    if len(public_key_str) > 0 and len(private_key_str) > 0:
        public_key = int(public_key_str)
        private_key = int(private_key_str)
    else:
        raise ValueError("Keys not found in file")
    return public_key, private_key

def generate_keys(p, g):
    private_key = random.randint(2, p - 1)
    public_key = (g ** private_key) % p
    return public_key, private_key

def encrypt(message, key):
    return [(char + key) % 256 for char in message]

def decrypt(ciphertext, key):
    return [(char - key) % 256 for char in ciphertext]

def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 9091))
    server_socket.listen(1)
    print("Server started. Waiting for connections...")

    client_socket, client_address = server_socket.accept()
    print("Connection established with:", client_address)

    p = 23
    g = 5

    try:
        server_public_key, server_private_key = load_keys_from_file("server_pk.txt")
    except ValueError:
        server_public_key, server_private_key = generate_keys(p, g)
        save_keys_to_file(server_public_key, server_private_key, "server_pk.txt")

    client_socket.sendall(str(server_public_key).encode())

    client_public_key = int(client_socket.recv(1024).decode())

    secret_key = (client_public_key ** server_private_key) % p
    print("Secret key:", secret_key)

    while True:
        encrypted_message = client_socket.recv(1024)

        decrypted_message = decrypt(encrypted_message, secret_key)

        print("Received message:", bytes(decrypted_message).decode())

        message = input("Enter a message to send (or 'q' to quit): ")
        if message == 'q':
            break

        encrypted_response = encrypt(message.encode(), secret_key)

        client_socket.sendall(bytes(encrypted_response))

    server_socket.close()


server()
