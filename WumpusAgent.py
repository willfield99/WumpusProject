#Wumpus Agent

wumpus = HuntTheWumpus()

class Agent(object):
    def __init__(self, x= '',y= '', w= wumpus):
        self.x= wumpus.playerx
        self.y= wumpus.playery
        self.w = wumpus
        