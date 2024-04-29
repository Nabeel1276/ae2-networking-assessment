import socket
import argparse
import os


def start_server(host, port):
    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to a host and port
    server_socket.bind((host, port))

    # Listen for incoming connections
    server_socket.listen(1)

    while True:
        try:
            print("Server up and running on localhost port", port)

            # Accept incoming connection
            client_socket, client_address = server_socket.accept()
            print("Connected to:", client_address)

            # Receive and save uploaded files
            while True:
                file_info = client_socket.recv(1024).decode()
                if not file_info:
                    break

                # Extract filename and file size from file_info
                filename, filesize = file_info.split("|")
                filename = os.path.basename(filename)
                filesize = int(filesize)

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
                with open(filename, "wb") as f:
                    f.write(received_data)
                print("File '{}' received and saved.".format(filename))

        finally:
            # Close the connection
            client_socket.close()


def parse_arguments():
    parser = argparse.ArgumentParser(description="Server for file uploading")
    parser.add_argument(
        "-H",
        "--host",
        default="127.0.0.1",
        help="Host address to bind (default: 127.0.0.1)",
    )
    parser.add_argument(
        "-p",
        "--port",
        type=int,
        default=5555,
        help="Port number to listen on (default: 5555)",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    start_server(args.host, args.port)
