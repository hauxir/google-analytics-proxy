import requests

from flask import Flask, Response, request
from flask_cors import CORS
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)

CORS(app)


GOOGLE_ANALYTICS_HOST = "www.google-analytics.com"
GOOGLE_ANALYTICS_ROOT = f"https://{GOOGLE_ANALYTICS_HOST}"


@app.route("/", methods=["GET"])
@app.route("/analytics.js", methods=["GET"])
def root():
    host = request.host
    headers = dict(request.headers)
    headers["Host"] = GOOGLE_ANALYTICS_HOST
    req = requests.get(
        f"{GOOGLE_ANALYTICS_ROOT}/analytics.js",
        headers=headers,
        stream=True,
        verify=False,
    )
    content = req.content.decode("utf-8")
    content = content.replace('/collect"', '/shoebill"')
    content = content.replace(GOOGLE_ANALYTICS_HOST, host)
    return Response(content, content_type=req.headers.get("content-type"))


@app.route("/shoebill", methods=["GET"])
@app.route("/collect", methods=["GET"])
def collect():
    args = dict(request.args)
    headers = dict(request.headers)
    headers["Host"] = GOOGLE_ANALYTICS_HOST
    args["uip"] = request.remote_addr
    req = requests.get(
        f"{GOOGLE_ANALYTICS_ROOT}/collect",
        params=args,
        headers=headers,
        stream=True,
        verify=False,
    )
    return Response(
        req.iter_content(chunk_size=10 * 1024),
        content_type=req.headers.get("content-type"),
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, threaded=True)
