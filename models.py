from dataclasses import dataclass

@dataclass
class Point2:
    x: int
    y: int

@dataclass
class House(Point2):
    happines: int
    gifted: bool = False

@dataclass
class Player(Point2):
    name: str
    ip: str
    score: int
