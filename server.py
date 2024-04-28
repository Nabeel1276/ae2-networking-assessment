import socket
import sys, os
from common import socket_to_screen, keyboard_to_socket


def get_client_args(socket, sock_addr):
    print(
        sock_addr + ": ", end="", flush=True
    )  # Use end="" to avoid adding a newline after the communicating partner's info, flush=True to force-print the info

    data = bytearray(1)
    bytes_read = 0

    while len(data) > 0 and "\n" not in data.decode():
        data = socket.recv(4096)
        client_args = data.decode().split()
    return client_args


def getfilename(filepath):
    return os.path.basename(filepath)


def get_file_content():
    print("hello")


def handle_file_upload(filepath, content):
    print("in handle file upload")
    filename = getfilename(filepath)
    if getfilename:
        print("YES! GOT THE FILE NAME", filename)
        if os.path.exists(filename):
            print("File already exists. Upload denied.", filepath)
    with open(filename, "w") as f:
        # Define the data to be written
        print(filename, filepath, content)
        # Use a for loop to write each line of data to the file
        for line in content:
            f.write(line)
            print(line)
        return

# Create the socket on which the server will receive new connections
srv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    port_number = int(sys.argv[1])
    srv_sock.bind(
        ("0.0.0.0", port_number)
    )  # sys.argv[1] is the 1st argument on the command line
    srv_sock.listen(5)
except Exception as e:
    # Print the exception message
    print(e)
    # Exit with a non-zero value, to indicate an error condition
    exit(1)

# Loop forever (or at least for as long as no fatal errors occur)
while True:
    try:
        print("Server up and running on localhost port", port_number)

        cli_sock, cli_addr = srv_sock.accept()
        cli_addr_str = str(
            cli_addr
        )  # Translate the client address to a string (to be used shortly)

        print("Client " + cli_addr_str + " connected. Now chatting...")

        # Loop until either the client closes the connection or the user requests termination
        while True:
            # First, read data from client and print on screen
            client_args = get_client_args(cli_sock, cli_addr_str)
            print("AAAAAAABBBBBBCCCCCCCC", client_args)
            if client_args[0] == "UPLOAD":
                handle_file_upload(client_args[1], client_args[2])

            bytes_read = socket_to_screen(cli_sock, cli_addr_str)
            if bytes_read == 0:
                print("Client closed connection.")
                break

            # Then, read data from user and send to client
            bytes_sent = keyboard_to_socket(cli_sock)
            if bytes_sent == 0:
                print("User-requested exit.")
                break

    finally:
        cli_sock.close()

        # Close the server socket as well to release its resources back to the OS
        srv_sock.close()

        # Exit with a zero value, to indicate success
        exit(0)
