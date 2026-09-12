





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
