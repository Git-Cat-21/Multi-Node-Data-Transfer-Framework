""" import socket

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 12345))

    # Initial handshake
    client_socket.send("HELLO".encode('utf-8'))
    response = client_socket.recv(1024).decode('utf-8')
    if response == "ACK":
        print("Handshake successful")

        # Send and receive messages
        while True:
            userid = input("Username: ")
            pwd = input("Password: ")
            client_socket.send(userid.encode('utf-8'))
            response = client_socket.recv(1024).decode('utf-8')
            pwd_check = response.split(":")
            if pwd_check[1].strip() == pwd.strip():
                print("1.Exit\t2.Copy\t3.Break")
                choice = int(input("Enter your choice:"))
                if choice == 1:
                    print("Exit session")
                elif choice == 2:
                    print("Copy")
                elif choice == 3:
                    print("Bye!")
                    continue
                else:
                    print("Wrong choice. Please try again!")
            else:
                print("Not matched")
            if userid.lower() == "exit":
                break
    else:
        print("Handshake failed")

    client_socket.close()

start_client()
 """


import socket
import signal
import sys

# Signal handler for graceful shutdown
def signal_handler(sig, frame):
    print("\n[CLIENT SHUTDOWN] Signal received, closing client socket...")
    client_socket.close()
    sys.exit(0)

# Attach the signal handler to SIGINT
signal.signal(signal.SIGINT, signal_handler)

def start_client():
    global client_socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 12345))

    # Initial handshake
    client_socket.send("HELLO".encode('utf-8'))
    response = client_socket.recv(1024).decode('utf-8')
    if response == "ACK":
        print("Handshake successful")

        # Send and receive messages
        while True:
            userid = input("Username: ")
            pwd = input("Password: ")
            client_socket.send(userid.encode('utf-8'))
            response = client_socket.recv(1024).decode('utf-8')
            pwd_check = response.split(":")
            if pwd_check[1].strip() == pwd.strip():
                print("1.Exit\t2.Copy\t3.Break")
                choice = int(input("Enter your choice:"))
                if choice == 1:
                    print("Exit session")
                elif choice == 2:
                    print("Copy")
                elif choice == 3:
                    print("Bye!")
                    continue
                else:
                    print("Wrong choice. Please try again!")
            else:
                print("Not matched")
            if userid.lower() == "exit":
                break
    else:
        print("Handshake failed")

    client_socket.close()

if _name_ == "_main_":
    start_client()