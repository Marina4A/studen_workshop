import socket

HOST = '127.0.0.1'
PORT = 8001


class Client:
    def __init__(self, host: str, port: int) -> None:
        self.host = host
        self.port = port
        self.socket = None

    def connect(self) -> None:
        """
        Establish connection with the server.
        """
        # Create a new client socket and establish a connection with the server
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))

        # Print message about successful connection to the server
        print(f"Connected to {self.host}:{self.port}")

    def send_data(self, data):
        """
        Send data to the server.
        """
        # Send data to the server
        with self.socket:
            self.socket.sendall(data)

        # Print message about successful sending of data
        print(f"Sent {len(data)} bytes to the server")

        # Receive data from the server
        received_data = b""
        while True:
            try:
                # Check if the socket is still open before calling recv()
                if self.socket.fileno() == -1:
                    break
                chunk = self.socket.recv(1024)
                if not chunk:
                    break
                received_data += chunk
            except socket.error as e:
               # Handle socket exception here
               print("Socket error occurred:", e)
               break

        # Print message about successful receiving of data
        print(f"Received {len(received_data)} bytes from the server")

        # Return the received data
        return received_data

    def disconnect(self) -> None:
        """
        Close the connection with the server.
        """
        # Close the client socket
        if self.socket is not None:
            self.socket.close()
            print(f"Disconnected from {self.host}:{self.port}")


if __name__ == "__main__":
    client = Client(host=HOST, port=PORT)
    client.connect()

    # Request a message from the user
    message = input("Enter message to send: ")

    # Send the message to the server and receive the response
    response = client.send_data(message.encode('utf-8'))

    # Print the response from the server
    print(response.decode('utf-8'))

    client.disconnect()
