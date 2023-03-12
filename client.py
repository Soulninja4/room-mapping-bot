import socket

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

while True:
    data = server.recv(1024)
    # Decode the received data and print it
    # print(f"{data.decode('utf-8')}")

    if data.decode('utf-8') == 'up':
        # server.sendall(b'received')
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
