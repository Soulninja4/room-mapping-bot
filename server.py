import socket
import threading
import pygame
import math


class Bot:
    def __init__(self, screen, conn) -> None:
        self.screen = screen
        self.conn = conn
        self.color = (255, 255, 255)
        self.height = 10
        self.width = 10
        self.speed = 0.1
        self.x = self.screen.get_width() // 2
        self.y = self.screen.get_height() // 2

        self.angle = 0
        self.rot_speed = 0

        self.block = pygame.Surface((30, 30))
        self.block.fill(self.color)
        self.block.set_colorkey((0, 0, 0))
        self.block_copy = self.block.copy()
        self.block_copy.set_colorkey((0, 0, 0))

        self.rect = self.block.get_rect()
        self.rect.center = (self.x, self.y)

    # def draw(self):

    #     pygame.draw.rect(self.screen, self.color,
    #                      (self.x, self.y, self.width, self.height))

    def handle_event(self, keys):
        if keys[pygame.K_UP]:
            self.x += self.speed*math.sin((360-self.angle)*(math.pi/180))
            self.y -= self.speed*math.cos((360-self.angle)*(math.pi/180))
            self.conn.sendall(b'up')
        if keys[pygame.K_DOWN]:
            self.x -= self.speed*math.sin((360-self.angle)*(math.pi/180))
            self.y += self.speed*math.cos((360-self.angle)*(math.pi/180))
            self.conn.sendall(b'down')
        if keys[pygame.K_LEFT]:
            self.rot_speed = .2
            self.conn.sendall(b'left')
        if keys[pygame.K_RIGHT]:
            self.rot_speed = -.2
            self.conn.sendall(b'right')
        if keys is None:
            self.rot_speed = 0

    def handle_rotation(self):
        # defining angle of the rotation
        self.angle = (self.angle + self.rot_speed) % 360
        print(self.angle)
        # rotating the orignal image
        self.block_copy = pygame.transform.rotate(self.block, self.angle)
        self.rect = self.block_copy.get_rect(center=(self.x, self.y))
        # drawing the rotated rectangle to the screen
        screen.blit(self.block_copy, self.rect)
        # flipping the display after drawing everything
        self.rot_speed = 0


# Initialize Pygame
pygame.init()

# Set the window size and title
size = (800, 600)
pygame.fastevent.init()
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Socket Thread")

# Set the server address and port
HOST = '127.0.0.1'
PORT = 1234

# Create a socket object
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))
sock.listen(5)

print(f"Listening on {HOST}:{PORT}...")


def handle_connection(conn):
    while True:
        # Receive data from the client
        data = conn.recv(1024)
        if not data:
            break

        # Print the received data
        print(f"Received data: {data.decode('utf-8')}")

    # Close the connection
    conn.close()


# Accept incoming connections and handle them in separate threads
while True:
    # Accept an incoming connection
    conn, addr = sock.accept()
    print(f"Connected by {addr}")
    bot = Bot(screen, conn)

    # Create a new thread to handle the connection
    thread = threading.Thread(target=handle_connection, args=(conn,))
    thread.start()

    # Listen for an up arrow key press
    while True:
        screen.fill((0, 0, 0))

        e = pygame.fastevent.poll()
        keys = pygame.key.get_pressed()
        if e.type == pygame.QUIT:
            pygame.quit()
            conn.close()
            exit()

        bot.handle_event(keys)
        bot.handle_rotation()
        pygame.display.flip()
