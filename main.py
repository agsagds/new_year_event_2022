from flask import Flask, redirect, url_for, jsonify, request, render_template
import time
import map as mp
import config as cfg
from functools import wraps

app = Flask(__name__)
mp.generate_map()


@app.route("/")
def hello_world():
    return render_template('index.htm', cfg=cfg)


@app.route("/map")
def get_map():
    return jsonify({'houses':mp.houses, 
        'players':list(mp.players.values()), 
        'width':cfg.MAP_WIDTH,
        'height':cfg.MAP_HEIGHT})


@app.route("/reg/<string:name>")
def reg(name: str):
    ip_addr = request.remote_addr
    for k,v in mp.players.items():
        if v.ip==ip_addr:
            v.name = name
            return jsonify(k)
    p_id = str(hash(name+ip_addr+str(time.time_ns())))
    mp.add_player(ip=ip_addr, name=name, id=p_id)
    return jsonify(p_id)


def validate_request(func):
    @wraps(func)
    def inner1(*args, **kwargs):
        if kwargs['id'] not in mp.players:
            return jsonify(cfg.BAD_ID)
        if not mp.can_do_action(kwargs['id']):
            return jsonify(f'P{cfg.REQUEST_REJECTED} must wait {cfg.REQUEST_INTERVAL_MS} ms between your requests')
        mp.last_actions[kwargs['id']]=round(time.time() * 1000)

        result = func(*args, **kwargs)

        return result
    return inner1


@app.route("/about_me/<string:id>")
def about_me(id: str):
    if id not in mp.players:
        return jsonify(cfg.BAD_ID)
    return jsonify(mp.players[id])


@app.route("/place_gift/<string:id>")
@validate_request
def place(id: str):
    return jsonify(mp.gift(p_id=id))


@app.route("/move/<string:id>/<string:direction>")
@validate_request
def move(id: str, direction: str):
    return jsonify(mp.move(p_id=id, dir = direction))


@app.route("/score")
def score():
    playersDTO=[]
    for i in mp.players.values():
        playersDTO.append((i.score, i.name))
    playersDTO.sort()
    return render_template('score.htm', players=playersDTO)


@app.route('/view')
def view():
    return render_template('map.htm', width=cfg.MAP_WIDTH, height=cfg.MAP_HEIGHT)


# Run the application
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')