#WumpusAgent.py
#Agent for Wumpus World Project
# Mason Humphrey, 
#2/7/2021

#This agent aims to guide an explorer through a cave littered with pits and wumpi in search for endless riches
#Takes in percepts from driver, returns appropriate action



#For movement function recieve percepts (each defined)
# Stench - the Wumpus is in a directly adjacent square (not diagonal).
# Breeze - there is a pit in a directly adjacent square (not diagonal).
# Glitter - the gold is in the current square
# Bump - you walked in to a wall of the dungeon
# Scream - the Wumpus was killed! 
# S - stench
# G - glitter
# U - bump
# C - scream 

#For movement function return a string indicating
 #N - move north
 #S - move south
 #E - move east
 #W - move west
 #SN - shoot north
 #SS - shoot south
 #SE - shoot east
 #SW - shoot west
 #G - grab gold
 #C - climb out 
#
import HuntTheWumpus

#--------------------------
#globals
#--------------------------
map = [] #currently 1d, needs to be 2d possibly?
gameType = 0
numArrows = 0
numWumpi = 0
up = False #going down or south by default
left= False: #moving right or west by default
moves = [] #list of all made moves by the agent
htw = HuntTheWumpus()


#sets the type of wumpi (moving/stationary), # of arrows, and # of wumpi
def setParams(type, arrows, wumpi):
    gameType = type
    numArrows = arrows
    numWumpi = wumpi
    return 0


def eastOrWest(east):#tells move functions whether to move east or west based off of the status of the left variable
    if(east):
        return 'E'
    else:
        return 'W'

def northOrSouth(north):#checks if agent is moving north or south
    if(north):
        return 'N'
    else:
        return 'S'

def vertical(s): #chekcs if last move was vertical. if it was not then its horizontal
    if s == 'N' or s == 'S':
        return True
    elif s == 'E' or s == 'W':
        return False


#MAIN MOVEMENT FUNCTION
#logic: Learning the board left to right while scanning up and down the y axis until bottom/top right corner is reached
def getMove(sensor):
    percepts = sensor #list of percepts that needs to be parsed
    move = ''#move performed by the agent this turn

    for p in percepts: 
        if p != 'U': #bumpcheck clear, move vertically and add move to moves list
            move = northOrSouth(up)
            moves.append(move)
            return move
        
        elif p == 'U' and vertical(moves[-1]): #move horizontally because we have hit the top or bottom of cave
            move = eastOrWest(left)
            up = not up
            moves.append(move)
            return move

        elif p == 'U' and not vertical(moves[-1]): #move vertically because we have just moved one space horizontally after hitting the top or bottom of cave
            move = northOrSouth(up)
            moves.append(move)
            return move
        
        

        


        

#if sensor is clear in desired direction, move to desired square and return this, otherwise send to appropriate danger function (what about percepts that don't matter? i.e wumpus to the right, but we are moving down)
#if we reach bottom, move right once, change up_down to up (1)
#if we reach top, move righ once, change up_down to down (0)
#if we reach bottom/top far right corner with no gold, do the same thing but from right to left until you find the gold.

    return 0 # should return a string back to driver to indicate each move



#in the case of a pit, the main movement function sends us here in order to try and get to the next desired tile, takes over for main movement function until it has reached this
def pit():
    return 0



#In the case of a wumpus, mmain movement function sends us here in order to try and kill it.
def wumpus(numArrows):
    if numArrows > 0:
        numArrows = numArrows- 1
        kill = htw.screamCheck(htw.playerx, htw.playery, htw.l, 'n')
    if not kill and numArrows > 0:
        numArrows = numArrows- 1
        kill = htw.screamCheck(htw.playerx, htw.playery, htw.l, 'e')
    if not kill and numArrows > 0:
        numArrows = numArrows- 1
        kill = htw.screamCheck(htw.playerx, htw.playery, htw.l, 's')
    if not kill and numArrows > 0:
        numArrows = numArrows- 1
        kill = htw.screamCheck(htw.playerx, htw.playery, htw.l, 'w')
    return 0




def escape():
    return 0
