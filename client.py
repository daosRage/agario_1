


def extract_complete_messages(messages, buffer):
    messages = []
    index = buffer.find("/n")
    while index > -1:
        index = buffer.find("/n")
        line = buffer[:index]
        messages.append(line)
        buffer = buffer[index+1:]
    return messages, buffer
    
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

def find_my_player(players_list):
    for player in players_list:
        if player["id"] == my_player_id:
            return player   
    return None

def calculate_camera_scale():
    comfortble_scale = 1.0
    threshold_radius = 100
    zoom_out_speed = 0.8

    if player_radius <= threshold_radius:
        return comfortble_scale

    else:
        a = threshold_radius / player_radius
        b = a ** zoom_out_speed
        return b 


def calculate_food_scale():
    comfortble_scale = 1.0
    threshold_radius = 100
    zoom_out_speed = 0.15

    if player_radius <= threshold_radius:
        return comfortble_scale

    else:
        a = threshold_radius / player_radius
        b = a ** zoom_out_speed
        return b  
def keys():
    return {
    "w": keys[pygame.K_w],
    "a": keys[pygame.K_a],
    "s": keys[pygame.K_s],
    "d": keys[pygame.K_d]
}
