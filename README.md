# telia-sms-web

## About

Simple [Flask](https://flask.palletsprojects.com/) app using [telia-sms-api](https://github.com/paalbra/telia-sms-api).

## Setup

```
cd /path/to/telia-sms-web
python3 -m venv venv
. venv/bin/activate
pip install git+https://github.com/paalbra/telia-sms-api.git@master
pip install Flask
pip install gunicorn
```

## Example

With systemd, venv, gunicorn and nginx on a non-root. You should of course use HTTPS in real life.

Systemd unit:

```
[Unit]
Description=telia-sms-web
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/telia-sms-web
Environment=PATH=/path/to/telia-sms-web/venv/bin
ExecStart=/path/to/telia-sms-web/venv/bin/gunicorn -e SCRIPT_NAME=/telia-sms-web --workers 4 --bind unix:telia-sms-web.sock -m 007 app:app

[Install]
WantedBy=multi-user.target
```

Nginx config:

```
server {
    server_name example.com;
    listen 80;

    location /telia-sms-web/ {
        proxy_pass http://unix:/path/to/telia-sms-web/telia-sms-web.sock;
        proxy_redirect off;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $remote_addr;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Usage:

```
$ curl --data '{"message": "Hello SMS!", "contact": "12345678", "auth": "somethinglongandsecret"}' -H 'Content-Type: application/json' http://example.com/telia-sms-web/
```
