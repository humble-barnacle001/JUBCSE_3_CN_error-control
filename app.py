from application.channel import channel
from application.cks import cks_verify
from application.lrc import lrc_verify
from application.vrc import vrc_verify
from typing import Dict, Type
from flask import Flask, render_template, send_from_directory, request
from flask.helpers import make_response, url_for
import json
from application.crc import crc_verify

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html", submit="/verify")


@app.before_request
def hook():
    if(request.method == "POST" and request.path == "/verify"):
        if(request.is_json):
            request.error_type, request.channel_data = channel(
                request.get_json()
            )
        else:
            return request.get_data()


@app.route("/verify", methods=["POST"])
def verify():

    client = request.channel_data
    vrc = vrc_verify(client["vrc"]["data"], client["vrc"]["meta"]["parity"])
    lrc = lrc_verify(client["lrc"]["data"], client["lrc"]["meta"]["bits"])
    crc = crc_verify(client["crc"]["data"], client["crc"]["meta"]["poly"])
    cks = cks_verify(client["cks"]["data"], client["cks"]["meta"]["bits"])
    rjson = {
        "vrc": {"time": vrc[0], "success": vrc[1], "data": client["vrc"]["data"]},
        "lrc": {"time": lrc[0], "success": lrc[1], "data": client["lrc"]["data"]},
        "crc": {"time": crc[0], "success": crc[1], "data": client["crc"]["data"]},
        "cks": {"time": cks[0], "success": cks[1], "data": client["cks"]["data"]},
        "error_type": request.error_type
    }
    print(rjson)
    res = make_response(json.dumps(rjson))
    res.headers["Content-Type"] = "application/json"
    return res


@app.errorhandler(Exception)
def page_not_found(e):
    print(e, 'url: %s, path: %s, method: %s' %
          (request.url, request.path, request.method))
    return render_template('404.html', error=e), 404


if __name__ == "__main__":
    from waitress import serve
    import logging
    logger = logging.getLogger('waitress')
    logger.setLevel(logging.DEBUG)
    app.debug = True
    serve(app, host='127.0.0.1', port=5500)
