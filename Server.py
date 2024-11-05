import socket
from threading import Thread

QUEUE_SIZE = 10
IP = '0.0.0.0'
PORT = 8080
ranges = 100
found = False

def send(msg, client_socket):
    # Send message with length header
    final_msg = str(len(msg)) + "#" + msg
    client_socket.send(final_msg.encode())

def recv(client_socket):
    # Receive message with length header
    msg_len = ''
    msg = ''
    char = client_socket.recv(1).decode()
    while char != "#":
        msg_len += char
        char = client_socket.recv(1).decode()
    for a in range(int(msg_len)):
        msg += client_socket.recv(1).decode()
    return msg

def handle_connection(client_socket, client_address):
    # handles each client connection
    global ranges, found
    try:
        print(f'New connection from {client_address[0]}:{client_address[1]}')

        while not found:
            send(str(ranges), client_socket)
            ranges += 10

            response = recv(client_socket)
            if response == "found":
                found = True
                print("Hash found, notifying all clients.")
                break
            elif response != "next":
                print(f"Unexpected response: {response}")

        send("found", client_socket)

    except socket.error as err:
        print(f"Socket error - {err}")
    finally:
        client_socket.close()

def main():
    global ranges
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server_socket.bind((IP, PORT))
        server_socket.listen(QUEUE_SIZE)
        print(f"Listening on port {PORT}")

        while True:
            client_socket, client_address = server_socket.accept()
            thread = Thread(target=handle_connection, args=(client_socket, client_address))
            thread.start()

    except socket.error as err:
        print(f"Socket error - {err}")
    finally:
        server_socket.close()

if __name__ == "__main__":
    main()
