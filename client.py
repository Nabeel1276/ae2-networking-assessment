import socket
import argparse
import os


def start_client(host, port, file_path):
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


def parse_arguments():
    parser = argparse.ArgumentParser(description="Client for file uploading")
    parser.add_argument(
        "-H",
        "--host",
        default="127.0.0.1",
        help="Host address of the server (default: 127.0.0.1)",
    )
    parser.add_argument(
        "-p",
        "--port",
        type=int,
        default=5555,
        help="Port number of the server (default: 5555)",
    )
    parser.add_argument("file_path", help="Path of the file to upload")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    start_client(args.host, args.port, args.file_path)
