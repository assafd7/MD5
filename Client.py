import socket
import hashlib
import base64

MD5TODEC = "202cb962ac59075b964b07152d234b70".lower()


def send(msg, client_socket):
    final_msg = str(len(msg)) + "#" + msg
    client_socket.send(final_msg.encode())


def recv(client_socket):
    msg_len = ''
    msg = ''
    char = client_socket.recv(1).decode()
    while char != "#":
        msg_len += char
        char = client_socket.recv(1).decode()
    for a in range(int(msg_len)):
        msg += client_socket.recv(1).decode()
    return msg


def get_md5_of_string(input_string):
    return hashlib.md5(input_string.encode()).hexdigest()


def start_client(host='127.0.0.1', port=8080):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((host, port))
        data = recv(client_socket)
        data = int(data)
        print(f"Received back: {data}")
        ranged = [data, data + 10]
        for a in range(ranged[0], ranged[1]):
            result = get_md5_of_string(str(a))
            print(result)
            if result == MD5TODEC:
                print("got it")
                send("found", client_socket)
                break


if __name__ == "__main__":
    start_client()
