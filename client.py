import socket
import os
import sys


def run_command(action, client_socket, file_path):
    if action == "put":
        print("You specified that you want to Upload a file")
        upload_file(file_path, client_socket)
    elif action == "get":
        print("You specified that you want to Download a file")
        download_file(file_path, client_socket)
    elif action == "list":
        print("You want Listing of 1st-level directory contents")
        list_file(client_socket)
    else:
        print("Invalid action specified. Please enter a valid action.")


def download_file(file_name, client_socket):
    print("You want to download '{}'".format(file_name))
    # Send file info to the server
    client_socket.send("{}|{}|{}".format("download", file_name, 0).encode())

    response = client_socket.recv(1024).decode()

    if response == "ERROR_FILE_NOT_FOUND":
        print("File '{}' does not exist on the server.".format(file_name))
        client_socket.close()
        return

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
    file_name = os.path.basename(file_path)
    file_size = os.path.getsize(file_path)

    # Send file info to the server
    client_socket.send("{}|{}|{}".format("upload", file_name, file_size).encode())

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

    print("File '{}' sent successfully.".format(file_name))


def list_file(client_socket):
    # Send file info to the server
    client_socket.send("{}|{}|{}".format("list", "", 0).encode())

    # Receive the list of files from the server
    data = client_socket.recv(1024).decode()

    # Print the list of files
    print("List of files in server's working directory:")
    print(data)


def start_client():
    if len(sys.argv) >= 2:
        host = sys.argv[1]
        port = int(sys.argv[2])
        action = sys.argv[3]
        if len(sys.argv) == 5:
            file_path = sys.argv[4]
        else:
            file_path = None
    else:
        print("Invalid number of arguments provided.")
        return

    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server
    client_socket.connect((host, port))

    run_command(action, client_socket, file_path)

    # Close the connection
    client_socket.close()

if __name__ == "__main__":
    start_client()
