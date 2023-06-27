import socket
import random

def save_keys_to_file(public_key, private_key, filename):
    with open(filename, "w") as f:
        f.write(str(public_key) + '\n')
        f.write(str(private_key))

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

def client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 9091))

    p = 23
    g = 5

    try:
        client_public_key, client_private_key = load_keys_from_file("client_pk.txt")
    except ValueError:
        client_public_key, client_private_key = generate_keys(p, g)
        save_keys_to_file(client_public_key, client_private_key, "client_pk.txt")

    client_socket.sendall(str(client_public_key).encode())

    server_public_key = int(client_socket.recv(1024).decode())

    secret_key = (server_public_key ** client_private_key) % p
    print("Secret key:", secret_key)

    while True:
        message = input("Enter a message to send (or 'q' to quit): ")
        if message == 'q':
            break

        encrypted_message = encrypt(message.encode(), secret_key)

        client_socket.sendall(bytes(encrypted_message))

        encrypted_response = client_socket.recv(1024)

        decrypted_response = decrypt(encrypted_response, secret_key)

        print("Received message:", bytes(decrypted_response).decode())

    client_socket.close()


client()
