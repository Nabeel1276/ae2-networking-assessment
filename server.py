import socket
import sys
from common import socket_to_screen, keyboard_to_socket

# Create the socket on which the server will receive new connections
srv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
	srv_sock.bind(("0.0.0.0", int(sys.argv[1]))) # sys.argv[1] is the 1st argument on the command line
	srv_sock.listen(5)
except Exception as e:
	# Print the exception message
	print(e)
	# Exit with a non-zero value, to indicate an error condition
	exit(1)

# Loop forever (or at least for as long as no fatal errors occur)
while True:
	try:
		print("Waiting for new client... ")
		
		cli_sock, cli_addr = srv_sock.accept()
		cli_addr_str = str(cli_addr) # Translate the client address to a string (to be used shortly)

		print("Client " + cli_addr_str + " connected. Now chatting...")

		# Loop until either the client closes the connection or the user requests termination
		while True:
			# First, read data from client and print on screen
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
