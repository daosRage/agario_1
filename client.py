







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
