# Build the docker image with:  `docker build -t celtix .`
# Put `IMAGE` in the same directory as this Dockerfile, and then run:
# `docker run --rm -v .:/w -w /w celtix PUZZLE SOLUTION.png`
# Replace `PUZZLE` with the name of your white-background Celtix screenshot.
# When done, `SOLUTION.png` (pick any name for SOLUTION, defaults to `output`) will appear in the same directory.

FROM python:3.11-slim

RUN apt-get update \
	&& apt-get install -y python3-venv libgl1 libglib2.0-0 libsm6 libxext6 libxrender-dev git \
	&& rm -rf /var/lib/apt/lists/*

WORKDIR /d
#RUN git clone https://github.com/amirlb/celtix-solver .
#RUN sed -i 's/opencv/opencv-python/' requirements.txt
RUN git clone https://github.com/pepa65/celtix-solver .
RUN python3 -m venv .
RUN bin/pip install -r requirements.txt
RUN sed -i 's/if len(sys.argv) != 2/if len(sys.argv) > 1:\n    sys.argv[1] = f"\/w\/{sys.argv[1]}"\nif len(sys.argv) < 2/' main.py
RUN sed -i 's/cv.imwrite("output.png", drawn)/out = f"\/w\/{sys.argv[2]}" if len(sys.argv) > 2 else "\/w\/output.png"\n    cv.imwrite(out, drawn)\n    stat = os.stat(sys.argv[1])\n    os.chown(out, stat.st_uid, stat.st_gid)/' main.py
RUN cat main.py
ENTRYPOINT ["/d/bin/python3", "/d/main.py"]
