import os
import threading

from flask import (
    Flask,
    request
)
from flask_basicauth import BasicAuth
import telia

app = Flask(__name__)
app.config["BASIC_AUTH_USERNAME"] = os.environ.get("BASIC_AUTH_USERNAME")
app.config["BASIC_AUTH_PASSWORD"] = os.environ.get("BASIC_AUTH_PASSWORD")
app.config["TELIA_CONFIG"] = os.environ.get("TELIA_CONFIG")
basic_auth = BasicAuth(app)

def send_sms(message, contact):
    api = telia.TeliaAPI(app.config["TELIA_CONFIG"])
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
