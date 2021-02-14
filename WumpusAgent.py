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
# B - breeze
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
#import HuntTheWumpus        Had to comment this out because it caused the code to have an error (something to do with circular imports) - Mason

#TODO
# 1. Ask about the other inputs we have to check (numWumpi)
# 2. More efficient logic? (poke - holing?) since we have a limited number of moves we need to worry about efficiency 
#
#
#
#
#
#
#
#


#--------------------------
#globals
#--------------------------
map = [] #currently 1d, needs to be 2d possibly?
gameType = 0
numArrows = 0
numWumpi = 0
up = False #going down or south by default
left = False #moving right or west by default
moves = [] #list of all made moves by the agent
#htw = HuntTheWumpus()
north = False #global variable for telling if we are moving north, or south
east = True #Global variables for telling if we are moving east, or west
shootcount = 0
possiblecorner = False #used to check if we have reached a coerner of the cave. If bumpcheck is true, then possibleCorner is set true. if on the next turn bumpcheck is true again, then we have hit a corner


#sets the type of wumpi (moving/stationary), # of arrows, and # of wumpi: used for re-setting the game in the driver code
def setParams(type, arrows, wumpi):

    try: #Should check to make sure that the inputs for the parameters are valid (integers), turns out Alan took care of the int() 
        gameType = int(type)
    except ValueError:
        gameType = 1
        print("Game type invalid, defaulting to 1.")
    
    if gameType > 2 or gameType < 1:
        gameType = 1
        print("Game type invalid, defaulting to 1.")

    try: 
        numArrows = int(arrows)
    except ValueError:
        numArrows = 1
        print("Number of arrows invalid, defaulting to 1.")
    
    try: 
        numWumpi = int(wumpi)                                    #????????????Do we need to check for anything else? ex. that this isnt too large? idk since we don't know size of cave
    except ValueError:
        numWumpi = 1
        print("Number of wumpi invalid, defaulting to 1.")

    return 0 


#Q: Should we make these global variables? then we could just check them whenever without making a funciton call. -Mason
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
# G - glitter -- incomplete
# S - stench  --  incomplete
# C - scream  --  incomplete
# B - breeze  --  incomplete
# U - bump  --  incomplete




#logic A: Learning the board left to right while scanning up and down the y axis until bottom/top right corner is reached
#if sensor is clear in desired direction, move to desired square and return this, otherwise send to appropriate danger function (what about percepts that don't matter? i.e wumpus to the right, but we are moving down)
#if we reach bottom, move right once, change up_down to up (1)
#if we reach top, move righ once, change up_down to down (0)
#if we reach bottom/top far right corner with no gold, do the same thing but from right to left until you find the gold.


#Logic B: Poke-holing, where instead of scanning everything since we have a limited # of moves

#main purpose - move and check if there is gold, 
def getMove(sensor):
    percepts = list(sensor) #Creates a list out of input percepts 
    print(percepts)
    move = ''#move performed by the agent this turn


    for p in percepts:  
         if p == 'G':
             return foundGold(p, percepts)
    
    for p in percepts:  
        if p == 'S':#if there is a wumpus in an adjacent square
            shootcount = shootcount + 1#add to shootcount for each shot
            return wumpus(numArrows, shootcount)

    for p in percepts:  
         if p == 'C':#if wumpus is hit then reset shootcount
            shootcount = 0

    for p in percepts: 
        if p == 'B':#If the current percept is a pit
            return pit(p, percepts) 

    for p in percepts: 
        if p == 'U': #If there is 
            return edge(p, percepts, vertical(moves[-1])) #may need to include map?


    #bumpcheck clear, move vertically and add move to moves list

    return 'S' # should return a valid string back to driver to indicate each move, right now it just spams south





#in the case that there is a G in the percept list, we come here to try to work out getting it. Once we are done here, we trigger escape()
#params: some info (may need more) from the main nav function to help it make its decision, it should also have access to the global map
def foundGold(p, percepts): 
    currentPercept = p
    perceptList = percepts

    return 0





#in the case of an edge, the main movement function sends us here in order to try and get to the next desired tile, takes over for main movement function until it has reached this
def edge(p, percepts, verticalVal):
    currentPercept = p
    perceptList = percepts
    vertical = verticalVal

    if p != 'U': #bumpcheck clear, move vertically and add move to moves list
            posssibleCorner= False
            move = northOrSouth(up)
            moves.append(move)
            return move
        
    elif p == 'U' and vertical(moves[-1]): #move horizontally because we have hit the top or bottom of cave
            move = eastOrWest(left)
            up = not up
            moves.append(move)
            return move

    elif p == 'U' and possiblecorner:#if we have hit a corner, switch horizontal direction, call escape
            possiblecorner == False
            eastOrWest = not eastOrWest
            return escape()

    elif p == 'U' and not vertical(moves[-1]): #move vertically because we have just moved one space horizontally after hitting the side of cave
            move = northOrSouth(up)
            moves.append(move)
            return move 
            
      #  elif p == 'U' and 
   #may need more movement commands 


    return 0 #this needs to be a movement command string, or never reached






#in the case of a pit, the main movement function sends us here in order to try and get to the next desired tile, takes over for main movement function until it has reached this
def pit(p, percepts):
    currentPercept = p
    perceptList = percepts

    return 0





#In the case of a wumpus, mmain movement function sends us here in order to try and kill it.
def wumpus(numArrows, count):
    
    if numArrows > 0 and count == 0:
        numArrows = numArrows- 1
        return('SN')
    if numArrows > 0 and count == 1:
        numArrows = numArrows- 1
        return('SE')
    if numArrows > 0 and count == 2:
        numArrows = numArrows- 1
        return('SS')
    if numArrows > 0 and count == 3:
        numArrows = numArrows- 1
        return('SW')
    else:
        print('Error in WumpasAgent.wumpus()')
        return ''
    
    




def escape():
    return 0
