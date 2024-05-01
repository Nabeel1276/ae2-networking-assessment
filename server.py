import socket
import argparse
import sys, os


def download_file(files_dir, filename, client_socket):
    print("you want to download", filename)
    with open(files_dir + filename, "rb") as file:
        data = file.read(1024)
        while data:
            client_socket.send(data)
            data = file.read(1024)
        print("File sent successfully")
        return

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
            action_type, file_name, filesize = file_info.split("|")

            # Receive and save uploaded files
            while True:
                if not file_info:
                    break
                if action_type == "upload":
                    file_name = os.path.basename(file_name)
                    filesize = int(filesize)
                    dest_file_path = files_dir + file_name

                    if os.path.exists(dest_file_path):
                        print(dest_file_path, "already exists. Upload denied.")
                        break

                    # Inform client to start sending the file
                    client_socket.send("READY".encode())

                    # Receive the file data
                    received_data = bytearray()
                    while len(received_data) < filesize:
                        packet = client_socket.recv(1024)
                        if not packet:
                            break
                        received_data.extend(packet)

                    # Write the received data to the file
                    with open(dest_file_path, "wb") as f:
                        f.write(received_data)
                    print("File '{}' received and saved.".format(file_name))
                elif action_type == "download":
                    print("We are in the download function")
                    download_file(files_dir, file_name, client_socket)
                    break

        finally:
            # Close the connection
            client_socket.close()
            print("Closed client connection.")

if __name__ == "__main__":
    start_server()
