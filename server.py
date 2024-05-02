import socket
import os
import sys


def list_files(client_socket):
    print("you want to list current directory content")
    # Get list of files in server's working directory
    files = os.listdir()

    # Send the list of files to the client
    client_socket.sendall("\n".join(files).encode())

    # Close the connection
    client_socket.close()


def download_file(files_dir, file_name, client_socket):
    print("You want to download", file_name)
    file_path = files_dir + file_name
    if not os.path.exists(file_path):
        print("Invalid! File '{}' does not exist.".format(file_name))
        client_socket.send("ERROR_FILE_NOT_FOUND".encode())
        return

    # Send confirmation to the client to start downloading
    client_socket.send("READY".encode())

    with open(file_path, "rb") as file:
        data = file.read(1024)
        while data:
            client_socket.send(data)
            data = file.read(1024)
        print("File sent successfully")


def start_server():
    port_number = int(sys.argv[1])
    files_dir = "./public_files/"

    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to a host and port
    server_socket.bind(("0.0.0.0", port_number))

    # Listen for incoming connections
    server_socket.listen(1)

    while True:
        try:
            print("Server up and running on localhost port", port_number)

            # Accept incoming connection
            client_socket, client_address = server_socket.accept()
            print("Connected to:", client_address)

            file_info = client_socket.recv(1024).decode()

            # Extract filename and file size from file_info
            action_type, file_name, file_size = file_info.split("|")

            # Receive and save uploaded files
            while True:
                if not file_info:
                    break
                if action_type == "upload":
                    file_name = os.path.basename(file_name)
                    file_size = int(file_size)
                    dest_file_path = files_dir + file_name

                    if os.path.exists(dest_file_path):
                        print(dest_file_path, "already exists. Upload denied.")
                        break

                    # Inform client to start sending the file
                    client_socket.send("READY".encode())

                    # Receive the file data
                    received_data = bytearray()
                    while len(received_data) < file_size:
                        packet = client_socket.recv(1024)
                        if not packet:
                            break
                        received_data.extend(packet)

                    # Write the received data to the file
                    with open(dest_file_path, "wb") as f:
                        f.write(received_data)
                    print("File '{}' received and saved.".format(file_name))
                    break
                elif action_type == "download":
                    download_file(files_dir, file_name, client_socket)
                    break
                elif action_type == "list":
                    list_files(client_socket)
                    break
        finally:
            # Close the connection
            client_socket.close()
            print("Closed client connection.")

if __name__ == "__main__":
    start_server()
