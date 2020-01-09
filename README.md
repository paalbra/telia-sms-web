# telia-sms-web

## About

Simple [Flask](https://flask.palletsprojects.com/) app using [telia-sms-api](https://github.com/paalbra/telia-sms-api).

## Setup

```
pip install git+https://github.com/paalbra/telia-sms-api.git@master
pip install Flask
pip install gunicorn
```

## Example

```
gunicorn app:app
```
