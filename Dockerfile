# Build the docker image with:  `docker build -t celtix .`
# Put `IMAGE` in the same directory as this Dockerfile, and then run:
# `docker run --rm -v .:/w -w /w celtix PUZZLE SOLUTION.png`
# Replace `PUZZLE` with the name of your white-background Celtix screenshot.
# When done, `SOLUTION.png` (pick any name for SOLUTION, defaults to `output`) will appear in the same directory.
# Use this `celtix` alias for convenience:  celtix PUZZLE SOLUTON.png
# alias celtix='docker run --rm -v .:/w -w /w celtix'

FROM python:3.11-slim

RUN apt-get update \
	&& apt-get install -y python3-venv libgl1 libglib2.0-0 libsm6 libxext6 libxrender-dev git \
	&& rm -rf /var/lib/apt/lists/*

WORKDIR /d
RUN git clone https://github.com/pepa65/celtix-solver .
RUN python3 -m venv .
RUN bin/pip install -r requirements.txt
ENTRYPOINT ["/d/bin/python3", "/d/main.py"]
