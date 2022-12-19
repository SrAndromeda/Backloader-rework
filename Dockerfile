FROM ubuntu:latest


RUN apt update
RUN apt install python3 -y
RUN apt install python3-pip -y
RUN apt install ffmpeg -y
RUN python3 -m pip install yt-dlp pillow

WORKDIR /app
COPY . /app


CMD ["python3", "backloader.py"]
