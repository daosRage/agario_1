import json 
import socket
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

def to_dict():
    player = []
    player.append(self.player_id)
    player.append(self.x)
    player.append(self.y)
    player.append(self.radius)
    player.append(self.color)
    player.append(self.name)
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
