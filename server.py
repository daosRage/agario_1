import socket
import threading
import json
from math import hypot
from random import randint
from time import sleep, time

#Налаштування сервера 
HOST = "localhost"       # слухати на всіх мережевих інтерфейсах
PORT = 5555
MAX_PLAYERS = 10        # більше десяти гравців одночасно сервер не пустить

#Налаштування гри (світ такий самий, як і в клієнтському коді)
WORLD_SIZE = 4000
FOOD_COUNT = 1000
FOOD_RADIUS = 10
START_PLAYER_RADIUS = 20
PLAYER_SPEED = 15
TICK_RATE = 30           # скільки разів на секунду сервер рахує гру й шле оновлення
EAT_SIZE_ADVANTAGE = 1.2  # наскільки більшим треба бути, щоб з'їсти іншого гравця


class Food:
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color

    def to_dict(self):

        a = {"x": self.x,
                "y": self.y,
                "radius": self.radius,
                "color": self.color}
        
        return a

def create_random_food():
    x = randint(-WORLD_SIZE, WORLD_SIZE)
    y = randint(-WORLD_SIZE, WORLD_SIZE)
    c1 = randint(0, 255)
    c2 = randint(0, 255)
    c3 = randint(0, 255)
    color = (c1, c2, c3)
    f = Food(x, y, FOOD_RADIUS, color)
    return f


class Player():
    def __init__(self,player_id,x,y,color,socket):
        self.player_id = player_id
        self.x = x
        self.y =y
        self.color = color
        self.socket = socket
        self.radius = START_PLAYER_RADIUS
        self.name = f"{player_id}"
        self.keys = {}


# ==== Спільні дані гри (доступ до них - тільки під замком!) ====
players = {}   # player_id -> обʼєкт Player
food_items = [create_random_food() for _ in range(FOOD_COUNT)]

state_lock = threading.Lock()          # захищає players і food_items
next_player_id = 1
next_player_id_lock = threading.Lock()  # захищає лічильник next_player_id




def handle_client(conn, addr, player): 
    global state_lock, players
    buffer = ""
    conn.settimeout(30)

    try:
        while True:
            try:
                data = conn.recv(1024)

                if not data:
                    break

                text = data.decode("utf-8")
                buffer = buffer + text

                messages, buffer = extract_complete_messages(buffer)

                for msg in messages:
                    try:
                        info = json.loads(msg)
                        keys = info["keys"]

                        with state_lock:
                            player.keys = keys

                    except json.JSONDecodeError:
                        continue

            except socket.timeout:
                break
            except (ConnectionResetError, OSError):
                break
    finally:
        with state_lock:
            players.pop(player.id, None)

        conn.close()
        print(f"Player {player.id} disconnected")
        
def send_json_line(sock, data):
    try:
        text = json.dumps(data)
        message = text + "\n"
        sock.sendall(message.encode("utf-8"))
        return True
    except OSError:
        return False        


food_items = []
for i in range(FOOD_COUNT):
    food_items.append(create_random_food())
    
def to_dict(self):
    player = {
    "id": self.player_id,
    "x": self.x,
    "y": self.y,
    "radius": self.radius,
    "color": self.color,
    "name": self.name,
    
    }
    return player


def extract_complete_messages(messages, buffer):
    messages = []
    index = buffer.find("/n")
    while index > -1:
        index = buffer.find("/n")
        line = buffer[:index]
        messages.append(line)
        buffer = buffer[index+1:]
    return messages, buffer

def playeris_touching(self, other_x, other_y, other_radius):

    distance_x = self.x - self.orher_x
    distance_y = self.y - self.orher_y
    distance = hypot(distance_x, distance_y)

    return distance <= self.radius + other_radius


if __name__ == "__main__":
    start_server()
