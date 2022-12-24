from dataclasses import dataclass
import config as cfg

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
    def move(self, p: Point2):
        self.x = max(0, min(self.x+p.x, cfg.MAP_WIDTH))
        self.y = max(0, min(self.y+p.y, cfg.MAP_HEIGHT))
