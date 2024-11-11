import socket
from threading import Thread, Lock
from protocol import send, recv

QUEUE_SIZE = 10
IP = '0.0.0.0'
PORT = 8080
RANGE_STEP = 10

found = False
ranges = 0
lock = Lock()
TARGET_HASH = "202cb962ac59075b964b07152d234b70".lower()  # Move MD5 hash to the server


def handle_connection(client_socket, client_address):
    """Handle each client connection."""
    global ranges, found
    try:
        print(f'New connection from {client_address[0]}:{client_address[1]}')

        # Send the hash target to the client
        send(TARGET_HASH, client_socket)

        while not found:
            # Critical section: safely increment the range
            with lock:
                current_range = ranges
                ranges += RANGE_STEP

            # Send range to client
            send(str(current_range), client_socket)

            response = recv(client_socket)
            if response == "found":
                found = True
                print("Hash found, notifying all clients.")
                break
            elif response != "next":
                print(f"Unexpected response: {response}")

        # Notify the client to stop if hash is found
        send("found", client_socket)

    except socket.error as err:
        print(f"Socket error - {err}")
    finally:
        client_socket.close()


def main():
    global found
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server_socket.bind((IP, PORT))
        server_socket.listen(QUEUE_SIZE)
        print(f"Listening on port {PORT}")

        while not found:
            client_socket, client_address = server_socket.accept()
            thread = Thread(target=handle_connection, args=(client_socket, client_address))
            thread.start()

    except socket.error as err:
        print(f"Socket error - {err}")
    finally:
        server_socket.close()


if __name__ == "__main__":
    main()
