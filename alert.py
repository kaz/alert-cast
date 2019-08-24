import time
import socket
import pychromecast
from flask import Flask, render_template, redirect

app = Flask(__name__)
device = None

@app.route("/", methods=["GET"])
def index():
	return render_template("index.html", status=device is not None)

@app.route("/mode/<mode>", methods=["GET", "POST"])
def mode(mode):
	global device

	if mode == "on":
		for cast in pychromecast.get_chromecasts():
			if cast.model_name == "Google Home Mini":
				device = cast
	else:
		device = None

	return redirect("/")

@app.route("/alert", methods=["GET", "POST"])
def alert():
	if device is None:
		return "alert is disabled"

	addr = socket.gethostbyname("%s.local" % socket.gethostname())

	if not device.is_idle:
		device.quit_app()

	device.wait()
	device.media_controller.play_media("http://%s:8080/static/alert.flac" % addr, "audio/flac")
	device.media_controller.block_until_active()

	return "ok"

if __name__ == "__main__":
	app.run(host="0.0.0.0", port=8080, threaded=True)
