import socket
import hashlib
from protocol import send, recv
from threading import Thread, Lock
import os

found = False
lock = Lock()


def get_md5_of_string(input_string):
    """Calculate MD5 hash."""
    return hashlib.md5(input_string.encode()).hexdigest()


def worker_thread(start, end, target_hash, client_socket):
    """Worker thread to compute MD5 hashes within the range."""
    global found
    for a in range(start, end):
        # Check if another thread has already found the hash
        with lock:
            if found:
                return

        result = get_md5_of_string(str(a))
        print(f"Checking {a}: {result}")

        if result == target_hash:
            print("Match found!")
            with lock:
                found = True  # Set the flag to stop other threads
            send("found", client_socket)
            return


def start_client(host='127.0.0.1', port=8080):
    """Initialize client and manage threads for hash computation."""
    global found
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((host, port))

        # Receive the target hash from the server
        target_hash = recv(client_socket)

        # Start threads based on CPU core count
        core_count = os.cpu_count()

        while not found:
            data = recv(client_socket)
            if data == "found":
                print("Stopping search, found by another client.")
                break

            start = int(data)
            range_per_thread = 10 // core_count
            threads = []

            for i in range(core_count):
                thread_start = start + (i * range_per_thread)
                thread_end = thread_start + range_per_thread
                thread = Thread(target=worker_thread, args=(thread_start, thread_end, target_hash, client_socket))
                threads.append(thread)
                thread.start()

            # Wait for all threads to finish
            for thread in threads:
                thread.join()

            if not found:
                send("next", client_socket)


if __name__ == "__main__":
    start_client()
