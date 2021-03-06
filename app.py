import functools
import os
import threading

from flask import (
    Flask,
    request
)
import telia

app = Flask(__name__)
app.config.from_object("config")

def check_auth(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if request.is_json:
            data = request.get_json()
            if "auth" in data:
                if data["auth"] == app.config["AUTH_KEY"]:
                    return func(*args, **kwargs)
                else:
                    return "Unauthorized", 401
        return "Bad request", 400
    return wrapper

def send_sms(message, contact):
    api = telia.TeliaAPI(app.config["TELIA_USERNAME"], app.config["TELIA_PASSWORD"])
    api.send_sms(message, [contact])
    api.session.close()

@app.route("/", methods=["POST"])
@check_auth
def index():
    if request.is_json:
        data = request.get_json()
        threading.Thread(target=send_sms, args=(data["message"], data["contact"])).start()
        return "OK"
    else:
        return "Bad request", 400

if __name__ == "__main__":
    app.run()
