import socketio
import subprocess
import signal
from capp import App
# ─── Setup ───────────────────────────────────────────────────────────────────────
# connect to the SocketIO server
SIO = socketio.Client()
record_proc = None
app = App(src=0, show=True)  # Use 0 for webcam or provide a video file pat
@SIO.event
def connect():
    print("✅ Connected to server")

@SIO.event
def disconnect():
    print("🔌 Disconnected from server")

@SIO.on('record')
def on_record(data):
    global record_proc
    action = data.get('action')
    if action == 'start':
        print("▶️  start recording")
        app.run()
    elif action == 'stop':
        print("⏹ stop recording")
        app.stop()

# ─── Main ────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    SIO.connect('http://localhost:8050')  # point to your Dash host
    SIO.wait()  # keep the client alive to receive events
