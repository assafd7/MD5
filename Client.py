import socket
import hashlib

MD5TODEC = "202cb962ac59075b964b07152d234b70".lower()

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

def get_md5_of_string(input_string):
    # Calculate MD5 hash
    return hashlib.md5(input_string.encode()).hexdigest()

def start_client(host='127.0.0.1', port=8080):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((host, port))
        while True:
            data = recv(client_socket)
            if data == "found":
                print("Stopping search, found by another client.")
                break

            start = int(data)
            end = start + 10
            for a in range(start, end):
                result = get_md5_of_string(str(a))
                print(f"Checking {a}: {result}")
                if result == MD5TODEC:
                    print("Match found!")
                    send("found", client_socket)
                    return  # Stop after finding the result

            send("next", client_socket)

if __name__ == "__main__":
    start_client()
