from flask import Flask, jsonify, session, redirect, render_template
from functools import wraps
import mpd


app = Flask(__name__)
#app.config.from_pyfile('config.py')
hostname = "http://radio.jobby";
# our local mpd streams on the map

streams = {
        "cybertisch1": {
            "name": "Cybertisch 1",
            "host": "localhost",
            "port": 6600,
            "streamurl": "http://localhost:8000"
        },
        "cybertisch2": {
            "name": "Cybertisch 2",
            "host": "localhost",
            "port": 6601,
            "streamurl": "http://localhost:8001"
        }
}
radios = {
    "groovesalad": {
        "name": "Groovesalad",
        "url": "http://ice2.somafm.com/groovesalad-128-mp3"
    },
    "swr3": {
        "name": "SWR 3",
        "url": "https://swr-swr3-live.cast.addradio.de/swr/swr3/live/mp3/128/stream.mp3"
    }
}

from contextlib import contextmanager
@contextmanager
def MPD(stream):
    try:
        client = mpd.MPDClient()
        client.connect(stream["host"],stream["port"] )
        yield client
    finally:
        client.close()

def details_mpd(stream):
    try:
        with MPD(stream) as client:
            ret = client.status()
            if ret['state']== 'play':
                ret.update(client.currentsong())
            return ret
    except:
        return { "state": "ERROR!" }

def stop_mpd(stream):
    with MPD(stream) as client:
        client.clear()

def volume_mpd(stream,vol):
    if not (0 < vol < 100):
        raise ValueError("volume must be between 0 and 100")
    with MPD(stream) as client:
        client.volume(vol)

def play_mpd(stream,radio):
    with MPD(stream) as client:
        print(f"clearing {stream['name']}")
        client.clear()
        print(f"Starting {radio['name']}({radio['url']}) on {stream['name']}")
        client.add(radio['url'])
        client.play()

@app.route('/stream/<streamid>')
def stream_view(streamid):
    stream = streams[streamid]
    stream['status'] = details_mpd(stream)
    return render_template("radio.html",stream=stream)

@app.route('/stream/<streamid>/url')
def stream_url(streamid):
    return redirect(streams[streamid]["streamurl"],code=307)

@app.route('/stream/<streamid>/stop'
        #,methods=["POST"])
        )
def stop_stream(streamid):
    stop_mpd(streams[streamid])
    return jsonify({"status": "ok"})

@app.route('/stream/<streamid>/volume/<vol>'
        #,methods=["POST"])
        )
def volume_stream(streamid,vol):
    volume_mpd(streams[streamid],vol)
    return jsonify({"status": "ok"})

@app.route('/stream/<streamid>/json')
@app.route('/stream/<streamid>/status')
def status_stream(streamid):
    stream = streams[streamid]
    stream["status"] = details_mpd(stream)
    return jsonify(stream)

@app.route('/stream/<streamid>/play/<radioid>'
        #,methods=["POST"])
        )
def start_stream(streamid,radioid):
    play_mpd(streams[streamid],radios[radioid])
    return jsonify({"status": "ok"})

@app.route('/stream/<streamid>/custom'
        #,methods=["POST"])
        )
def custom_stream(streamid):
    """
    start a stream with a custom, user provided url
    request data must contain: { "url": <path-to-url> }
    """
    radio = { "name": "User Provided Stream" }
    radio.update(request.json())
    play_mpd(streams[streamid],radio)
    return jsonify({"status": "ok"})

@app.route('/')
def index():
    for ident,stream in streams.items():
            streams[ident]["status"] = details_mpd(stream)
    return render_template("overview.html",streams=streams)

@app.route('/streams/json')
def all_streams_json():
    for ident,stream in streams.items():
            streams[ident]["status"] = details_mpd(stream)
    return jsonify(streams)

@app.route('/radios/json')
def all_radios_json():
    return jsonify(radios)

if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0")
