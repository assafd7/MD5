import socket

def send(msg, client_socket):
    """Send message with length header."""
    final_msg = f"{len(msg)}#{msg}"
    client_socket.send(final_msg.encode())

def recv(client_socket):
    """Receive message with length header."""
    msg_len = ""
    while True:
        char = client_socket.recv(1).decode()
        if char == "#":
            break
        msg_len += char
    msg_len = int(msg_len)
    return client_socket.recv(msg_len).decode()
