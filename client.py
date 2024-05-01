import socket
import argparse
import os, sys


def display_options(client_socket):
    # Display options to the user
    print("Please select an option:")
    print("1. Upload a file")
    print("2. Download a file")
    print("3. Listing of 1st-level directory contents \n")

    # Prompt the user for input
    choice = input("Enter the number of your choice: \n")

    # Process the user's choice
    if choice == "1":
        print("You selected Upload a file")
        # Prompt the user for text input
        file_path = input(f"Please enter filepath for the file you wish to upload: ")
        upload_file(file_path, client_socket)
    elif choice == "2":
        print("You selected Download a file")
        filename = input(f"Please enter filename for the file you wish to download: ")
        download_file(filename, client_socket)
    elif choice == "3":
        print("You selected Listing of 1st-level directory contents")
    else:
        print("Invalid choice. Please enter a valid option.")


def download_file(filename, client_socket):
    print("You want to download '{}'".format(filename))
    # Send file info to the server
    client_socket.send("{}|{}|{}".format("download", filename, 0).encode())
    # Receive data from the server and write it to a file
    with open(filename, "wb") as file:
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

    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server
    client_socket.connect((host, port))

    display_options(client_socket)

    # Close the connection
    client_socket.close()

if __name__ == "__main__":
    start_client()
