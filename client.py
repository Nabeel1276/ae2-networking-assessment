import socket
import argparse
import os, sys


def start_client():
    host = sys.argv[1]
    port = int(sys.argv[2])
    file_path = sys.argv[3]

    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server
    client_socket.connect((host, port))

    # Extract filename and file size
    filename = os.path.basename(file_path)
    filesize = os.path.getsize(file_path)

    # Send file info to the server
    client_socket.send("{}|{}".format(filename, filesize).encode())

    # Wait for server's confirmation
    confirmation = client_socket.recv(1024).decode()
    if confirmation != "READY":
        print("Server is not ready to receive the file.")
        client_socket.close()
        return

    # Open and send the file
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(1024), b""):
            client_socket.sendall(chunk)

    print("File '{}' sent successfully.".format(filename))

    # Close the connection
    client_socket.close()

if __name__ == "__main__":
    start_client()
