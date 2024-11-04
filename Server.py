import socket
from threading import Thread

QUEUE_SIZE = 10
IP = '0.0.0.0'
PORT = 8080
ranges = 100


def send(msg, client_socket):
    final_msg = str(len(msg)) + "#" + msg
    client_socket.send(final_msg.encode())


def recv(client_socket):
    msg_len = ''
    msg = ''
    print(client_socket)
    char = client_socket.recv(1).decode()
    while char != "#":
        msg_len += char
        char = client_socket.recv(1).decode()
    for a in range(int(msg_len)):
        msg += client_socket.recv(1).decode()
    return msg


def handle_connection(client_socket, client_address):
    """
   handle a connection
   :param client_socket: the connection socket
   :param client_address: the remote address
   :return: None
   """
    global ranges
    try:
        print('New connection received from ' + client_address[0] + ':' + str(client_address[1]))
        send(str(ranges), client_socket)
        if recv(client_socket) == "found":
            print("found")

    except socket.error as err:
        print('received socket exception - ' + str(err))
    finally:
        client_socket.close()


def main():
    global ranges
    # Open a socket and loop forever while waiting for clients
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server_socket.bind((IP, PORT))
        server_socket.listen(QUEUE_SIZE)
        print("Listening for connections on port %d" % PORT)

        while True:
            client_socket, client_address = server_socket.accept()
            thread = Thread(target=handle_connection,
                            args=(client_socket, client_address))
            thread.start()
            ranges += 10
    except socket.error as err:
        print('received socket exception - ' + str(err))
    finally:
        server_socket.close()


if __name__ == "__main__":
    # Call the main handler function
    main()