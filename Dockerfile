FROM ubuntu:latest


RUN apt update
RUN apt install python3 -y
RUN apt install python3-pip -y
RUN apt install ffmpeg -y
RUN python3 -m pip install django django-rest-framework django-tailwind django-widget-tweaks yt-dlp pillow requests httpx 

WORKDIR /code
COPY . /code

RUN python3 backloader/manage.py migrate

ENTRYPOINT ["python3", "backloader/manage.py"]
CMD ["runserver", "0.0.0.0:8000"]
