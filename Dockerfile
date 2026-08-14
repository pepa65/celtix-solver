# Put a jpg-image in the same directory as this Dockerfile, and then run:
# docker run -v ./IMAGE.jpg:/app/puzzle.jpg celtix-solver
# (replace IMAGE with the name of your white-background Celtix screenshot)

FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
RUN git clone https://github.com/amirlb/celtix-solver .
#RUN sed -i 's/opencv/opencv-python/' requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python3", "main.py", "/app/puzzle.jpg"]
