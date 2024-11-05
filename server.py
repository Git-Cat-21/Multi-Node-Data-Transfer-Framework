""" import socket
import threading

def handle_client(client_socket, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    
    try:
        # Initial handshake: expecting "HELLO" message
        message = client_socket.recv(1024).decode('utf-8')
        if message == "HELLO":
            client_socket.send("ACK".encode('utf-8'))  # Send acknowledgment
            print(f"Connection successful with {addr}")
            
            # Data transfer after handshake
            while True:
                data = client_socket.recv(1024).decode('utf-8')
                #print(data)
                file = open("id_passwd.txt","r")
                text = file.read()
                for i in text.split():
                    if i.split(":")[0] == data:
                        pwd = i.split(":")[1]
                print(pwd)
                if not data:  # No data means client disconnected
                    break
                print(f"Received from [{addr}]: {data}")
                
                # Echo back data
                client_socket.send(f"Echo: {pwd}".encode('utf-8'))
        else:
            client_socket.send("Invalid handshake".encode('utf-8'))
            print(f"[HANDSHAKE FAILED] Handshake failed with {addr}")
    finally:
        client_socket.close()
        print(f"[DISCONNECTED] {addr} disconnected.")

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 12345))
    server_socket.listen()
    print("[SERVER STARTED] Listening on port 12345")

    while True:
        client_socket, addr = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(client_socket, addr))
        client_thread.start()

        # Optional: Keep track of threads
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

start_server()
 """

import socket
import threading
import signal
import sys

# Signal handler for graceful shutdown
def signal_handler(sig, frame):
    print("\n[SERVER SHUTDOWN] Signal received, closing server socket...")
    server_socket.close()
    sys.exit(0)

# Attach the signal handler to SIGINT
signal.signal(signal.SIGINT, signal_handler)

def handle_client(client_socket, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    
    try:
        # Initial handshake: expecting "HELLO" message
        message = client_socket.recv(1024).decode('utf-8')
        if message == "HELLO":
            client_socket.send("ACK".encode('utf-8'))  # Send acknowledgment
            print(f"Connection successful with {addr}")
            
            # Data transfer after handshake
            while True:
                data = client_socket.recv(1024).decode('utf-8')
                if not data:
                    break

                # Check credentials in the file
                file = open("id_passwd.txt", "r")
                text = file.read()
                pwd = None
                for i in text.split():
                    if i.split(":")[0] == data:
                        pwd = i.split(":")[1]
                file.close()

                if pwd:
                    client_socket.send(f"Echo: {pwd}".encode('utf-8'))
                else:
                    client_socket.send("User not found".encode('utf-8'))
                
                print(f"Received from [{addr}]: {data}")
        else:
            client_socket.send("Invalid handshake".encode('utf-8'))
            print(f"[HANDSHAKE FAILED] Handshake failed with {addr}")
    except Exception as e:
        print(f"[ERROR] An error occurred with {addr}: {e}")
    finally:
        client_socket.close()
        print(f"[DISCONNECTED] {addr} disconnected.")

def start_server():
    global server_socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 12345))
    server_socket.listen()
    print("[SERVER STARTED] Listening on port 12345")

    while True:
        try:
            client_socket, addr = server_socket.accept()
            client_thread = threading.Thread(target=handle_client, args=(client_socket, addr))
            client_thread.start()

            # Optional: Keep track of threads
            print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")
        except OSError:
            break  # Exit loop if server socket is closed

if _name_ == "_main_":
    start_server()