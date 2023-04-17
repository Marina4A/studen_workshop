import socket
import sys
from random import randint

# Constants
HOST: str = "localhost"
PORT: int = 12346
P: int = 23
G: int = 5
BUFFER_SIZE: int = 4096


# Generate shared secret key
def generate_key(p: int, g: int, a: int) -> int:
    return pow(g, a, p)


# Create socket and connect to server
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    try:
        client_socket.connect((HOST, PORT))
    except ConnectionRefusedError:
        print("Connection refused by the server. Please try again later.")
        sys.exit(1)

    # Receive public key A from server and send public key B
    A: int = int(client_socket.recv(BUFFER_SIZE).decode())
    b: int = randint(1, P - 2)
    B: int = pow(G, b, P)
    client_socket.sendall(str(B).encode())

    # Compute shared secret key
    shared_key: int = generate_key(P, A, b)
    print(f"Shared key: {shared_key}")

    # Send and receive encrypted message to server
    while True:
        message: str = input("Enter message: ")
        encrypted_message: str = "".join(chr(ord(c) ^ shared_key) for c in message)
        client_socket.sendall(encrypted_message.encode())
        data: bytes = client_socket.recv(BUFFER_SIZE)
        response: str = "".join(chr(ord(c) ^ shared_key) for c in data.decode())
        print(f"Received: {response}")

# Close connection (socket is automatically closed by the 'with' statement)
