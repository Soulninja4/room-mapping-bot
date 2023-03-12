import socket
import json
import time

ip = '127.0.0.1'
port = 1234

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect((ip, port))

prox_data = {
    'up': 10,
    'down': 20,
    'left': 30,
    'right': 40
}
prox_data = json.dumps(prox_data)
last_triggered = 0

while True:
    data = server.recv(1024)
    # Decode the received data and print it
    # print(f"{data.decode('utf-8')}")

    # add a debounce function to wait for 0.1 seconds before triggering the code
    current_time = time.time()
    if current_time - last_triggered < 0.01:
        continue
    last_triggered = current_time

    if data.decode('utf-8') == 'up':
        # server.sendall(b'received')
        server.sendall(bytes(prox_data, encoding="utf-8"))
        print("up")
    if data.decode('utf-8') == 'down':
        # server.sendall(b'received')
        print("down")
    if data.decode('utf-8') == 'left':
        # server.sendall(b'received')
        print("left")
    if data.decode('utf-8') == 'right':
        # server.sendall(b'received')
        print("right")
