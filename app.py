import os
import threading

from flask import (
    Flask,
    request
)
from flask_basicauth import BasicAuth
import telia

app = Flask(__name__)
app.config.from_object("config")
basic_auth = BasicAuth(app)

def send_sms(message, contact):
    api = telia.TeliaAPI(app.config["TELIA_USERNAME"], app.config["TELIA_PASSWORD"])
    api.send_sms(message, [contact])
    api.session.close()

@app.route("/", methods=["POST"])
@basic_auth.required
def index():
    if request.is_json:
        data = request.get_json()
        threading.Thread(target=send_sms, args=(data["message"], data["contact"])).start()
        return "OK"
    else:
        return "FAIL"

if __name__ == "__main__":
    app.run()
