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


#--------------------------
#globals
#--------------------------
map = [] #currently 1d, needs to be 2d possibly?
gameType = 0
numArrows = 0
numWumpi = 0
up_down = 0 #going down by default



#sets the type of wumpi (moving/stationary), # of arrows, and # of wumpi
def setParams(type, arrows, wumpi):
    gameType = type
    numArrows = arrows
    numWumpi = wumpi
    return 0





#MAIN MOVEMENT FUNCTION
#logic: Learning the board left to right while scanning up and down the y axis until bottom/top right corner is reached
def getMove(sensor):
    percepts = sensor #list of percepts that needs to be parsed


#if sensor is clear in desired direction, move to desired square and return this, otherwise send to appropriate danger function (what about percepts that don't matter? i.e wumpus to the right, but we are moving down)
#if we reach bottom, move right once, change up_down to up (1)
#if we reach top, move righ once, change up_down to down (0)
#if we reach bottom/top far right corner with no gold, do the same thing but from right to left until you find the gold.

    return 0 # should return a string back to driver to indicate each move



#in the case of a pit, the main movement function sends us here in order to try and get to the next desired tile, takes over for main movement function until it has reached this
def pit():
    return 0



#In the case of a wumpus, mmain movement function sends us here in order to try and kill it.
def wumpus():
    return 0




def escape():
    return 0
