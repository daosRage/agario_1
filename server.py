import json 
import socket
def handle_client(conn, addr, player): 
    global state_lock, players
    buffer = ""
    conn.settimeout(30)

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

    with state_lock:
        players.pop(player.id, None)

    conn.close()
    print(f"Player {player.id} disconnected")
