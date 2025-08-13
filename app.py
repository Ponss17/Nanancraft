from flask import Flask, Response
from mcstatus import JavaServer

app = Flask(__name__)

SERVER_IP = "23.230.3.73"
SERVER_PORT = 25615

@app.route("/")
def index():
    return "API Minecraft funcionando :)"

@app.route("/status")
def status():
    server = JavaServer.lookup(f"{SERVER_IP}:{SERVER_PORT}")
    try:
        status = server.status()
        online = status.players.online
        max_players = status.players.max
        latency = round(status.latency)
        version = status.version.name
        motd = status.description.get('text') if isinstance(status.description, dict) else status.description
        player_names = [p.name for p in status.players.sample] if status.players.sample else []
        players_str = ", ".join(player_names) if player_names else "Nadie conectado"

        respuesta = (
            f"🌟 Servidor ONLINE 🌟\n"
            f"MOTD: {motd}\n"
            f"Versión: {version}\n"
            f"Latencia: {latency} ms\n"
            f"Jugadores conectados: {online}/{max_players}\n"
            f"Jugadores: {players_str}"
        )
    except Exception:
        respuesta = "🔴 Servidor OFFLINE o sin respuesta"

    return Response(respuesta, mimetype="text/plain")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
