from models import Point2, House, Player
import config as cfg
import time
import random as rnd

houses = []
players = dict()
last_actions = dict()
moves = {cfg.UP: Point2(0,-cfg.PLAYER_STEP),
     cfg.DOWN: Point2(0,cfg.PLAYER_STEP),
    cfg.LEFT: Point2(-cfg.PLAYER_STEP,0),
    cfg.RIGHT: Point2(cfg.PLAYER_STEP,0)}


def can_do_action(id:str):
    return round(time.time() * 1000) - last_actions[id] > cfg.REQUEST_INTERVAL_MS


def intersect(a: Point2, b: Point2):
    return ((a.x-b.x)**2 + (a.y-b.y)**2) < cfg.HOUSE_RANGE_SUARE


def generate_map():
    global houses, players
    houses = []
    for _i in range(100000):
        if len(houses) == cfg.HOUSES_COUNT:
            break

        house = House(0,0, rnd.randint(cfg.HAPPY_MIN, cfg.HAPPY_MAX))
        for i in range(1000):
            house.x = rnd.randint(0, cfg.MAP_WIDTH)
            house.y = rnd.randint(0, cfg.MAP_HEIGHT)
            f = 1
            for  h in houses:
                if intersect(h, house):
                    f=0
                    break
            if f==1:
                houses.append(house)
                break

    for i in players.keys():
        players[i].x =  rnd.randint(0, cfg.MAP_WIDTH)
        players[i].y =  rnd.randint(0, cfg.MAP_HEIGHT)


def add_player(ip: str, name: str, id: str):
    global players
    p = Player(  x=rnd.randint(0, cfg.MAP_WIDTH),
                    y=rnd.randint(0, cfg.MAP_HEIGHT),
                    name=name,
                    ip=ip,
                    score=0 )
    players[id] = p
    last_actions[id] = 0


def can_place(a: Point2, b: Point2):
    return ((a.x-b.x)**2 + (a.y-b.y)**2) < cfg.GIFT_RANGE_SQUARE


def all_gifted():
    for i in houses:
        if not i.gifted:
            return False
    return True


def gift(p_id: str):
    global houses, players
    already = False
    cnt = 0
    for h in houses:
        if can_place(players[p_id], h):
            if h.gifted:
                already = True
            else:
                players[p_id].score += h.happines
                h.gifted=True
                cnt += 1
    if all_gifted():
        generate_map()
    if cnt>0:
        return cfg.SUCCESS
    if already:
        return cfg.ALREADY_GIFTED
    return cfg.BAD_GIFT_POSITION


def move(p_id: str, dir:str):
    if dir not in moves:
        return cfg.BAD_MOVE
    players[p_id].move(moves[dir])
    return cfg.SUCCESS