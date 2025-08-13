from flask import Flask, Response
from mcstatus import JavaServer
import threading
import time

app = Flask(__name__)

SERVER_IP = "23.230.3.73"
SERVER_PORT = 25615

@app.route('/')
def index():
    return "API de estado de NaNaCraft2 funcionando :)"

@app.route('/status')
def status():
    server = JavaServer(SERVER_IP, SERVER_PORT)
    try:
        status = server.status()
        online = status.players.online
        max_players = status.players.max
        latency = round(status.latency)
        version = status.version.name

        player_names = []
        if status.players.sample:
            player_names = [player.name for player in status.players.sample]
        players_str = ", ".join(player_names) if player_names else "Nadie conectado"

        respuesta = (
            f"🌟 NaNaCraft2 está ONLINE 🌟\n"
            f"Jugadores conectados: {online} de {max_players}\n"
            f"Jugadores: {players_str}\n"
            f"Latencia: {latency} ms\n"
            f"Versión: {version}\n"
        )
    except Exception as e:
        respuesta = "🔴 NaNaCraft2 está OFFLINE o no responde."

    return Response(respuesta, mimetype='text/plain')

def auto_ping():
    while True:
        try:
            print("⏳ Auto-ping para mantener la API activa...")
            requests.get("http://localhost:5000/")
        except Exception as e:
            print(f"Error en auto-ping: {e}")
        time.sleep(300)

if __name__ == "__main__":
    import requests
    threading.Thread(target=auto_ping, daemon=True).start()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
