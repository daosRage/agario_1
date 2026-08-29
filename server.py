import json 
import socket

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
def create_random_food():
    x = randint(-WORLD_SIZE, WORLD_SIZE)
    y = randint(-WORLD_SIZE, WORLD_SIZE)
    c1 = randint(0, 255)
    c2 = randint(0, 255)
    c3 = randint(0, 255)
    color = (c1, c2, c3)
    f = Food(x, y, FOOD_RADIUS, color)
    return f

food_items = []
for i in range(FOOD_COUNT):
    food_items.append(create_random_food())
    
def to_dict(self):
    player = {
    "id": self.player_id,
    "id": self.x,
    "id": self.y,
    "id": self.radius,
    "id": self.color,
    "id": self.name,
    
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
