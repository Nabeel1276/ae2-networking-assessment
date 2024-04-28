import sys
import socket

def socket_to_screen(socket, sock_addr):
	print(sock_addr + ": ", end="", flush=True) # Use end="" to avoid adding a newline after the communicating partner's info, flush=True to force-print the info

	data = bytearray(1)
	bytes_read = 0
	
	while len(data) > 0 and "\n" not in data.decode():
		data = socket.recv(4096)

		print("AAAAAAAAAAAAAA", data.decode(), end="")
		print(data.decode(), end="") # Use end="" to avoid adding a newline per print() call
		bytes_read += len(data)
	return bytes_read

def keyboard_to_socket(socket):
	print("You: ", end="", flush=True) # Use end="" to avoid adding a newline after the prompt, flush=True to force-print the prompt

	# Read a full line from the keyboard. The returned string will include the terminating newline character.
	user_input = sys.stdin.readline()
	if user_input == "EXIT\n": # The user requested that the communication is terminated.
		return 0

	# Send the whole line through the socket; remember, TCP provides no guarantee that it will be delivered in one go.
	bytes_sent = socket.sendall(str.encode(user_input))
	return bytes_sent
