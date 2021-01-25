from flask import Flask, jsonify, session, redirect, render_template, url_for
from functools import wraps
import mpd
import psutil
from time import sleep
import sys

app = Flask(__name__)
# app.config.from_pyfile('config.py')

# TODO: load streams configuration from environment file
hostname = "http://work.search4ce.app.de.corp.thales"
# our local mpd streams on the map

streams = {
    "cybertisch1": {
        "name": "Cybertisch 1",
        "host": "localhost",
        "port": 6600,
        "streamurl": f"{hostname}:28000",
    },
    "cybertisch2": {
        "name": "Cybertisch 2",
        "host": "localhost",
        "port": 6601,
        "streamurl": f"{hostname}:28001",
    },
    "cyberklo": {
        "name": "Cyberklo",
        "host": "localhost",
        "port": 6602,
        "streamurl": f"{hostname}:28002",
    },
}
radios = {
    "groovesalad": {
        "name": "Groovesalad",
        "url": "http://ice2.somafm.com/groovesalad-128-mp3",
    },
    "gsclassic": {
        "name": "Groovesalad Classic",
        "url": "http://ice2.somafm.com/gsclassic-128-mp3",
    },
    "swr3": {
        "name": "SWR 3",
        "url": "https://swr-swr3-live.cast.addradio.de/swr/swr3/live/mp3/128/stream.mp3",
    },
    "iloveradio": {
        "name": "I love Radio",
        "url": "http://streams.ilovemusic.de/iloveradio1.mp3",
    },
    "ilovedance": {
        "name": "I love Dance",
        "url": "http://streams.ilovemusic.de/iloveradio2.mp3",
    },
    "ilovechill": {
        "name": "I love Music and Chill",
        "url": "http://streams.ilovemusic.de/iloveradio10.mp3",
    },
}

from contextlib import contextmanager


@contextmanager
def MPD(stream):
    try:
        client = mpd.MPDClient()
        client.connect(stream["host"], stream["port"])
        yield client
    finally:
        client.close()


# TODO: this only works if mpd and appserver run on the same host
def conns_mpd(stream):
    streamport = int(stream["streamurl"].split(":")[-1])
    for conn in psutil.net_connections(kind='tcp'):
        if conn.status == 'ESTABLISHED' and conn.laddr.port == streamport:
            yield conn

def details_mpd(stream):
    try:
        with MPD(stream) as client:
            ret = client.status()
            if ret["state"] == "play":
                ret.update(client.currentsong())
            ret["listeners"] = len(list(conns_mpd(stream)))
            print(list(conns_mpd(stream)))
            return ret
    except:
        return {"state": "ERROR!"}


def stop_mpd(stream):
    with MPD(stream) as client:
        client.clear()


# volume not available for streams

#def volume_mpd(stream, vol):
#    if not (0 < vol < 100):
#        raise ValueError("volume must be between 0 and 100")
#    with MPD(stream) as client:
#        client.setvol(vol)

#@app.route(
#    "/stream/<streamid>/volume/<int:vol>"
#    ,methods=["POST","GET"]
#)
#def volume_stream(streamid, vol:int):
#    volume_mpd(streams[streamid], vol)
#    # return to /streams/streamid
#    return redirect(url_for("stream_view",streamid=streamid))


def play_mpd(stream, radio):
    with MPD(stream) as client:
        print(f"clearing {stream['name']}")
        client.clear()
        print(f"Starting {radio['name']}({radio['url']}) on {stream['name']}")
        client.add(radio["url"])
        client.play()


@app.route("/stream/<streamid>")
def stream_view(streamid):
    stream = streams[streamid]
    stream["status"] = details_mpd(stream)
    return render_template(
        "radio.html", streamid=streamid, stream=stream, radios=radios
    )


@app.route("/stream/<streamid>/url")
def stream_url(streamid):
    return redirect(streams[streamid]["streamurl"], code=307)


@app.route(
    "/stream/<streamid>/stop"
    ,methods=["POST","GET"]
)
def stop_stream(streamid):
    stop_mpd(streams[streamid])
    return redirect(url_for("stream_view",streamid=streamid))



@app.route("/stream/<streamid>/json")
@app.route("/stream/<streamid>/status")
def status_stream(streamid):
    stream = streams[streamid]
    stream["status"] = details_mpd(stream)
    return jsonify(stream)


@app.route(
    "/stream/<streamid>/play/<radioid>"
    ,methods=["POST","GET"]
)
def start_stream(streamid, radioid):
    play_mpd(streams[streamid], radios[radioid])
    # return to /streams/streamid
    sleep(1) # wait for the new stream to be started by mpd
    return redirect(url_for("stream_view",streamid=streamid))

@app.route(
    "/stream/<streamid>/custom"
    ,methods=["POST","GET"]
)
def custom_stream(streamid):
    """
    start a stream with a custom, user provided url
    request data must contain: { "url": <path-to-url> }
    """
    radio = {"name": "User Provided Stream"}
    radio.update(request.json())
    play_mpd(streams[streamid], radio)
    sleep(1) # wait for the new stream to be started by mpd
    return redirect(url_for("stream_view",streamid=streamid))


@app.route("/")
@app.route("/streams")
def index():
    for ident, stream in streams.items():
        streams[ident]["status"] = details_mpd(stream)
    return render_template("overview.html", streams=streams)


@app.route("/streams/json")
def all_streams_json():
    for ident, stream in streams.items():
        streams[ident]["status"] = details_mpd(stream)
    return jsonify(streams)


@app.route("/radios/json")
def all_radios_json():
    return jsonify(radios)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
