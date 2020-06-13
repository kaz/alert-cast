import time
import socket
import pychromecast
from flask import Flask, render_template, redirect

app = Flask(__name__)
device = None

port = 8080
host = socket.gethostbyname(f"{socket.gethostname()}.local")
media_url = f"http://{host}:{port}/static/alert.flac"

@app.route("/", methods=["GET"])
def index():
	return render_template("index.html", status=device is not None)

@app.route("/mode/<mode>", methods=["GET", "POST"])
def mode(mode):
	global device

	if mode == "enable":
		for cast in pychromecast.get_chromecasts():
			if cast.model_name == "Google Home Mini":
				device = cast
	else:
		device = None

	return redirect("/")

@app.route("/alert/<mode>", methods=["GET", "POST"])
def alert(mode):
	if device is None:
		return "alert is disabled"

	if mode == "start":
		if not device.is_idle:
			device.quit_app()

		device.wait()
		device.media_controller.play_media(media_url, "audio/flac")
		device.media_controller.block_until_active()
	else:
		device.quit_app()

	return "ok"

if __name__ == "__main__":
	app.run(host="0.0.0.0", port=port, threaded=True)
