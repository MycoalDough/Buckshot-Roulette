import socket
import time
import json
import numpy as np
import threading
from typing import Optional
# Define host and port for the server
host = "127.0.0.1"  # Use your local or external IP address
port = 12345
current_data = []
server_socket: Optional[socket.socket] = None
client_socket: Optional[socket.socket] = None

# Create a socket and bind it to the host and port
def create_host(callback):
    global server_socket, client_socket
    if server_socket:
        server_socket.close()
        
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("localhost", 12345))  # Change to your host and port
    server_socket.listen()  # Allow only one connection

    print("Listening for Unity connection")

    while True:
        # Accept a connection from Unity
        client_socket, client_address = server_socket.accept()
        print(f"Accepted connection from {client_address}")

        # Call the callback function to signal the connection is established
        callback(client_socket)



def get_state():
    try:
            client_socket.send("get_state".encode("utf-8"))

            data = client_socket.recv(1024).decode("utf-8")
            data_list = data.split(',')
            current_data = []
            if data:

                result_list = []

                for element in data_list:
                    if element.isdigit():
                        result_list.append(int(element))
                    elif element.replace('.', '', 1).isdigit():
                      result_list.append(float(element))
                    elif element.lower() == 'true' or element.lower() == 'false':
                        result_list.append(element.lower() == 'true')
                    else:
                        result_list.append(element)


                for value in result_list:
                    if isinstance(value, (bool, int, float)):
                        float_value = float(value)
                        current_data.append(float_value)
                current_data = np.array(current_data, dtype=float)
                return current_data
    except Exception as e:
        print("Error in get_state:", e)
        return None

def convert_list(string):
    l = string.split(",")
    l = [int(number) for number in l]
    return l


def play_step(step):
    try:
        to_send = "play_step:" + str(step)
        client_socket.send(to_send.encode("utf-8"))
        data = client_socket.recv(1024).decode("utf-8")
        if data:
            elements = data.split(':')

            result_list = []

            for element in elements:
                if is_float(element):
                    result_list.append(float(element))
                elif element.replace('.', '', 1).isdigit():
                    result_list.append(float(element))
                elif element.lower() == 'true' or element.lower() == 'false':
                    result_list.append(element.lower() == 'true')
                else:
                    result_list.append(element)
            return np.array(convert_list(elements[0]), dtype=float), result_list[1], result_list[2]
    except Exception as e:
        print("Error in get_state:", e)
        return None

def is_float(s):
    try:
        float_value = float(s)
        return True
    except ValueError:
        return False

def reset():
    client_socket.send("reset".encode("utf-8"))
#client_socket.close()
