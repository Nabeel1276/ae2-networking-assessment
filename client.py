import socket
import argparse
import os, sys


def run_command(action, file_path, client_socket):
    # Process the user's choice
    if action == "put":
        print("You specified that you want to Upload a file")
        # Prompt the user for text input
        upload_file(file_path, client_socket)
    elif action == "get":
        print("You specified that you want to Download a file")
        download_file(file_path, client_socket)
    elif action == "list":
        print("You specified that you want to Listing of 1st-level directory contents")
    else:
        print("Invalid action specified. Please enter a valid action.")


def download_file(file_name, client_socket):
    print("You want to download '{}'".format(file_name))
    # Send file info to the server
    client_socket.send("{}|{}|{}".format("download", file_name, 0).encode())
    # Receive data from the server and write it to a file
    with open(file_name, "wb") as file:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            file.write(data)

    print("File received successfully")
    client_socket.close()


def upload_file(file_path, client_socket):
    # Extract filename and file size
    filename = os.path.basename(file_path)
    filesize = os.path.getsize(file_path)

    # Send file info to the server
    client_socket.send("{}|{}|{}".format("upload", filename, filesize).encode())

    # Wait for server's confirmation
    confirmation = client_socket.recv(1024).decode()

    if confirmation != "READY":
        print("Upload denied, it is possible that the file already exists.")
        client_socket.close()
        return

    # Open and send the file
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(1024), b""):
            client_socket.sendall(chunk)

    print("File '{}' sent successfully.".format(filename))

def start_client():
    host = sys.argv[1]
    port = int(sys.argv[2])
    action = sys.argv[3]
    file_path = sys.argv[4]

    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server
    client_socket.connect((host, port))

    run_command(action, file_path, client_socket)

    # Close the connection
    client_socket.close()

if __name__ == "__main__":
    start_client()
