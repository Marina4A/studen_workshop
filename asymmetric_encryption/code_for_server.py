import socket
from random import randint

# Constants
HOST = "localhost"
PORT = 12346
P = 23
G = 5
BUFFER_SIZE = 4096


# Generate shared secret key
def generate_key(p, g, a):
    return pow(g, a, p)


# Create socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)

# Wait for client connection and send public key
print("Waiting for connection...")
client_socket, address = server_socket.accept()
print("Connected by", address)
a = randint(1, P - 2)
A = pow(G, a, P)
client_socket.sendall(str(A).encode())

# Receive public key B from client and compute shared secret key
B = int(client_socket.recv(BUFFER_SIZE).decode())
shared_key = generate_key(P, B, a)
print(f"Shared key: {shared_key}")

# Receive message from client and send encrypted response
while True:
    data = client_socket.recv(BUFFER_SIZE)
    if not data:
        break
    message = data.decode()
    print(f"Received: {message}")
    encrypted_message = "".join(
        [f"{chr(ord(message[i]) ^ shared_key)}" for i in range(len(message))]
    )
    client_socket.sendall(encrypted_message.encode())

# Close connection
client_socket.close()
server_socket.close()