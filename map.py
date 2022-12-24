from models import Point2, House, Player
import config as cfg
import typing
import random as rnd

houses = []
players = dict()


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


def can_place(a: Point2, b: Point2):
    return ((a.x-b.x)**2 + (a.y-b.y)**2) < cfg.GIFT_RANGE


def gift(p_id: str):
    global houses, players
    for h in houses:
        if can_place(players[p_id], h):
            if h.gifted:
                return cfg.ALREADY_GIFTED
            players[p_id].score += h.happines 
            return cfg.SUCCESS
    return cfg.BAD_GIFT_POSITION
