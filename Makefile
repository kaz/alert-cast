.PHONY: run
run:
	python3 alert.py

.PHONY: deps
deps:
	pip3 install -r requirements.txt

static/alert.flac: static/alert.wav
	ffmpeg -stream_loop 10 -i $< -acodec flac $@
