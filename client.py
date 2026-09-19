import socket
import threading
import json
import pygame

#До якого сервера підключатись ====
SERVER_HOST = "localhost"   # "127.0.0.1" означає "цей самий компʼютер"
SERVER_PORT = 5555

#Налаштування вікна ====
WIDTH = 1000
HEIGHT = 1000
FPS = 60

#Спільні дані, якими користуються ОБИДВА потоки ====
latest_state = {"players": [], "food": []}   # останній стан гри, надісланий сервером
my_player_id = None                           # який саме гравець у latest_state - це "я"
connected = True                              # чи ще тримаємо звʼязок із сервером
state_lock = threading.Lock()                 # захищає всі змінні вище від одночасного доступу

def send_json_line(sock, data):
    text = json.dumps(data)
    message = text + "\n"
    try:
        sock.sendall(message.encode("utf-8"))
        return True
    except OSError:
        return False   
        
def extract_complete_messages(messages, buffer):
    messages = []
    index = buffer.find("/n")
    while index > -1:
        index = buffer.find("/n")
        line = buffer[:index]
        messages.append(line)
        buffer = buffer[index+1:]
    return messages, buffer

def receive_messages(sock):
    global my_player_id, connected, latest_state
    buffer = ""
    connected = True

    while connected:
        try:
            data = sock.recv(4096)
        except OSError:
            break
        if not data:
                break
        buffer += data.decode("utf-8")
        messages, buffer = extract_complete_messages(buffer)

        for message_text in messages:
            try:
                data_dict = json.loads(message_text)
            except json.JSONDecodeError:
                continue

            with state_lock:
                if "your_id" in data_dict:
                
                    my_player_id = data_dict["your_id"]
                if "error" in data_dict:
                    print(f"Помилка: {data_dict['error']}")
                    connected = False
                if "players" in data_dict:
                    latest_state = data_dict

    with state_lock:
        connected = Falsе
    print("звязок розірвано")



def connect_to_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.connect(( SERVER_HOST, SERVER_PORT))
    return server_socket

def get_pressed_keys_dict():
    return {
    "w": keys[pygame.K_w],
    "a": keys[pygame.K_a],
    "s": keys[pygame.K_s],
    "d": keys[pygame.K_d]
}

def calculate_camera_scale(player_radius):
    comfortble_scale = 1.0
    threshold_radius = 100
    zoom_out_speed = 0.8

    if player_radius <= threshold_radius:
        return comfortble_scale

    else:
        a = threshold_radius / player_radius
        b = a ** zoom_out_speed
        return b 


def calculate_food_scale(player_radius):
    comfortble_scale = 1.0
    threshold_radius = 100
    zoom_out_speed = 0.15
    if player_radius <= threshold_radius:
        return comfortble_scale

    else:
        a = threshold_radius / player_radius
        b = a ** zoom_out_speed
        return b  


def world_to_screen(x, y, camera_x, camera_y, scale):
    b_x = x - camera_x
    b_y = y - camera_y
    h_x = b_x * scale
    h_y = b_y * scale
    halfx = WIDTH // 2
    halfy = HEIGHT // 2
    screen_x = h_x + halfx
    screen_y = h_y + halfy
    return screen_x, screen_y
    
def find_my_player(players_list):
    for player in players_list:
        if player["id"] == my_player_id:
            return player   
    return None


def draw_food(window, food_list, camera_x, camera_y, camera_scale, food_scale):
    for food in food_list:
        sx, sy = world_to_screen(food["x"], food["y"], camera_x, camera_y, camera_scale)
        scaled_radius = max(1, int(food["radius"] * food_scale))
        pygame.draw.circle(window, food["color"], (sx, sy), scaled_radius)


def draw_players(window, font, player_list, camera_x, camera_y, camera_scale):
    for player in player_list:
        sx, sy = world_to_screen(player["x"], player["y"],camera_x, camera_y, camera_scale)
        rad = int(player["radius"] * camera_scale)
        if player["id"] == my_player_id:
            pygame.draw.circle(window, (0, 255, 0), (sx, sy), rad)
            textme = font.render(player["name"],True, (0, 255, 0))
            window.blit(textme, (sx, sy + 3))
        else:
            pygame.draw.circle(window, tuple(player["color"]), (sx, sy), rad)
            textme2 = font.render(player["name"],True, (0, 255, 0))
            window.blit(textme2, (sx, sy + 3))











def draw_everything(window, font, state):
    window.fill("white")
    my_player = find_my_player(state["players"])
    if my_player is None:
        pygame.display.update()
        return
    camera_x = my_player["x"]
    camera_y = my_player["y"]
    camera_scale = calculate_camera_scale(my_player["radius"])
    food_scale = calculate_food_scale(my_player["radius"])
    draw_food(window, state["food"], camera_x, camera_y, camera_scale, food_scale)
    draw_players(window, font, state["players"], camera_x, camera_y, camera_scale)
    pygame.display.update()


def main():
    global connected

    print(f"Підключаюсь до сервера {SERVER_HOST}:{SERVER_PORT}...")
    try:
        sock = connect_to_server()
    except OSError as error:
        print("Не вдалося підключитись до сервера:", error)
        return

    threading.Thread(target=receive_messages, args=(sock,), daemon=True).start()

    pygame.init()
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("З'їж кружечки! (онлайн)")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 24)

    running = True
    while running and connected:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        keys_dict = get_pressed_keys_dict(keys)
        send_json_line(sock, {"keys": keys_dict})

        with state_lock:
            state_copy = {
                "players": list(latest_state["players"]),
                "food": list(latest_state["food"]),
            }

        draw_everything(window, font, state_copy)
        clock.tick(FPS)

    connected = False
    sock.close()
    pygame.quit()




if __name__ == "__main__":
    main()
