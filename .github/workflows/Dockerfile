FROM tiangolo/node-frontend:20 as build-stage
WORKDIR /app
COPY ../frontend/package*.json /app/
RUN npm install yarn
RUN yarn install
COPY ./frontend /app/
RUN yarn run build

# -------------------------------------------------------------

FROM nginx:alpine-slim

RUN apk update && \
    apk add python3 py3-pip sqlite ffmpeg openssl

# Install Python dependencies
RUN python3 -m pip install django django-rest-framework django-tailwind django-widget-tweaks daphne yt-dlp pillow requests httpx tzdata django-cors-headers

WORKDIR /app

COPY . /app
COPY startup.sh /app/backloader/startup.sh

# Configure Nginx
COPY --from=build-stage /app/build/ /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

WORKDIR /app/backloader

# Ensure database
# RUN python3 manage.py migrate

# Build the static files
RUN python3 manage.py collectstatic --noinput

# Expose ports
EXPOSE 80

CMD sh -c "./startup.sh"