FROM ubuntu:latest

RUN apt update && \
    apt install -y python3 python3-pip sqlite3 ffmpeg nginx openssl

# Install Python dependencies
RUN python3 -m pip install django django-rest-framework django-tailwind django-widget-tweaks daphne yt-dlp pillow requests httpx tzdata

WORKDIR /app

COPY . /app

# Configure Nginx
COPY nginx.conf /etc/nginx/sites-available/default


WORKDIR /app/backloader

# Ensure database
RUN python3 manage.py migrate

# Build the static files
RUN python3 manage.py collectstatic --noinput

# Expose ports
EXPOSE 80

CMD sh -c "nginx && daphne backloader.asgi:application --port 8000 --bind 0.0.0.0"
