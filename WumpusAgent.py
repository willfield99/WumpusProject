import random

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
# 3. Mapping function / way to keep track of moves


#--------------------------
#globals
#--------------------------
#map = [] #currently 1d, needs to be 2d possibly?
from WumpusRoom import Room
from random import randint

gameType = 0
numArrows = 0
numWumpi = 0
up = False #going down or south by default
left = False #moving right or west by default
moves = [''] #list of all made moves by the agent- first item is null so that getcurrent move returns the entrance the first time its called


north = False #global variable for telling if we are moving north, or south 0 - Moving South, 1 - Moving North
east = True #Global variables for telling if we are moving east, or west: 0 - moving west, 1 - moving east
prev = ['X', 'X', 'X']
case = 0
shootcount = 0
possiblecorner = False #used to check if we have reached a coerner of the cave. If bumpcheck is true, then possibleCorner is set true. if on the next turn bumpcheck is true again, then we have hit a corner



#sets the type of wumpi (moving/stationary), # of arrows, and # of wumpi
def setParams(type, arrows, wumpi):
    global gameType
    global numArrows
    global numWumpi

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
        numWumpi = int(wumpi)                                   
    except ValueError:
        numWumpi = 1
        print("Number of wumpi invalid, defaulting to 1.")

    return ""
 


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

#create a dict to use as a map
#Each room object will have a tuple coordinate as a key. Room objects will contain the data that we know about the room and can be updated to reflect newfound info
startroom = Room(0, 0, False, 0, 0, 0)#first room added to our map-will be updated 
#this is our agents knowledge map. it starts out with the entrance room
map = {(0,0): startroom}
# setting the key of the current room

currentRoom = map[(startroom.getX(), startroom.getY())] 


def getCurrentRoom(prevroomx, prevroomy, move):#takes in coordinates of prevroom to return key coordinates of newroom
    if move == 'N':
        return (prevroomx, prevroomy +1)
    if move == 'S':
        return (prevroomx, prevroomy -1)
    if move == 'E':
        return (prevroomx -1, prevroomy)
    if move == 'W':
        return (prevroomx +1, prevroomy)
    else:
        return(prevroomx, prevroomy)

def addRooms(currentRoomX, currentRoomY, percepts):#after each directional move made by the agent, we check if we need to add new rooms to our map. Then we update the data associated with our rooms based on the percept list
    x = currentRoomX
    y = currentRoomY
    if not (currentRoomX -1, currentRoomY) in map:
        map[(currentRoomX -1, currentRoomY)] = Room(currentRoomX -1, currentRoomY, False, 0, 0, 0)
    if not (currentRoomX +1, currentRoomY) in map:
        map[(currentRoomX +1, currentRoomY)] = Room(currentRoomX +1, currentRoomY, False, 0, 0, 0)
    if not (currentRoomX, currentRoomY -1) in map:
        map[(currentRoomX, currentRoomY -1)] = Room(currentRoomX, currentRoomY -1, False, 0, 0, 0)
    if not (currentRoomX, currentRoomY +1) in map:
        map[(currentRoomX, currentRoomY +1)] = Room(currentRoomX, currentRoomY +1, False, 0, 0, 0)
    
    if 'S' in percepts:
        map[(currentRoomX -1, currentRoomY)].setStench(1)
        map[(currentRoomX +1, currentRoomY)].setStench(1)
        map[(currentRoomX, currentRoomY -1)].setStench(1)
        map[(currentRoomX, currentRoomY +1)].setStench(1)
    
    if 'B' in percepts:
        map[(currentRoomX -1, currentRoomY)].setBreeze(1)
        map[(currentRoomX +1, currentRoomY)].setBreeze(1)
        map[(currentRoomX, currentRoomY -1)].setBreeze(1)
        map[(currentRoomX, currentRoomY +1)].setBreeze(1)


    


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
    global north
    global east
    global moves
    global prev
    global case
    #global map
    
    #print(currentRoom)
    #room = getCurrentRoom(currentRoom.getX(), currentRoom.getY(), moves[-1])#getting current rooms coordinates. for the first room this is (0,0)
    
    #addRooms(map[room].getX(), map[room].getY(), percepts)#adds the 4 rooms adjacent to our current room to the map
    #currentRoom = room
    #print(currentRoom)#printing the room that we are in- this line is just for testing purposes


    if case == 99: #if we have found the gold, we need to escape
        return escape(percepts)

    if 'G' in percepts:   
         #escape() #escape does nothing rn
         prev.append('G')
         return 0 #to stop and at least show we are here
    
    if case == 20:
        return wumpus()

    if 'S' in percepts:  
        #if there is a wumpus in an adjacent square
        prev.append('S')
        return wumpus()
        

    if 'C' in percepts:  
        print("C in percepts")
        shootcount = 0
        prev.append('C')
        if north == False:
            return 'S'
        else:
            return 'N'
    
   # if 'B' in percepts and 'U' in percepts: #if we are at a pit and an edge at the same time
   #     prev.append('B')

   #     return 'N'
    if case != 0:
       return pit(percepts)
        
    if 'B' in percepts:#If the current percept is a pit
        print("B in percepts")
        prev.append('B')
        return pit(percepts) 

    if 'U' in percepts: 
        print("U in percepts")
        prev.append('U')
        return edge(percepts) 


    #bumpcheck clear, move vertically and add move to moves list

    if north == True: #have a 2% chance of randomly moving to the east/west to help with getting stuck
        if random.randint(0,100) < 2:
            if east == True:
                return 'E'
            else:
                return 'W'
        
        else:
            moves.append('N')
            prev.append('O')
            return 'N'

    if north == False:
        if random.randint(0,100) < 2:
            if east == True:
                return 'E'
            else:
                return 'W'
        
        else:
            moves.append('S')
            prev.append('O')
            return 'S'


        

#in the case that there is a G in the percept list, we come here to try to work out getting it. Once we are done here, we trigger escape()
#params: some info (may need more) from the main nav function to help it make its decision, it should also have access to the global map
def foundGold(p, percepts): 
    currentPercept = p
    perceptList = percepts
    global case

    case = 99 #case for if we have the gold, signaling that we need to escape

    return 'G'





#in the case of an edge, the main movement function sends us here in order to try and get to the next desired tile, takes over for main movement function until it has reached this
#NOTE: We should be able to use the global variable north to tell if we've been previously moving north or south.
#NOTE  For example if we have been moving down, and hit an edge, we can simply check the value of north. If north is false we see that we have been moving down. Then we can change it to true then turn so that it represents that we are now going up. 
def edge(percepts):
    #currentPercept = p
    perceptList = percepts
    global north #important to include these in order to edit global variables
    global east
    global moves
    global prev
    global map
    print("In edge case")

#cases: 
# HIT BOTTOM MOVING DOWN / RIGHT
# 1. moving down (north = False) && moving right (east = True) && last move NOT move right (east): set north to true, return move right, 
# 1.a moving down (north = False) && moving right (east = True) && last move WAS move right (east) : return move down   - case for if we are at the step after we have hit the top (our last move was move right), so we simply return go down

#HIT BOTTOM MOVING DOWN / LEFT
# 2. moving down (north = False) && moving left (east = False) && last move NOT move left: set north to true, return move left
# 2a. moving down (north = False) && moving left (east = False) && last move WAS move left: return move down

#HIT TOP MOVING UP / RIGHT
# 3. moving up(north = True) && moving right (east = True) && last move NOT move right: set north to False, return move right
# 3a. moving up(north = True) && moving right (east = True) && last move WAS move right: return move up - case for if we have just previously hit the bottom and moved right, so we want to simply go up

#HIT TOP MOVING UP / LEFT
# 4.)  moving up(north = True) && moving left (east = False) && last move NOT move left: set north to False, return move left
# 4a.)  moving up(north = True) && moving left (east = False) && last move WAS move left: return move up

#HIT CORNER - Good Question

#if we are jammed in a corner, simply change east/west
    if prev[-1] == 'U' and prev[-2] == 'O' and prev[-3] == 'U' and prev[-4] == 'O' or prev[-1] == 'U' and prev[-2] == 'U' and prev[-3] == 'U':
        if east == True:
            east = False
            print("hereeeeeeeee")
            return 'W'
        if east == False:
            east = True
           # prev.append('X')
            return 'E'


    #1 hit bottom moving right
    if north == False and east == True and moves[-1] != 'E':
        north = True
        moves.append('E')
        return 'E'

    #1a hit top, but just moved left
    if north == False and east == True and moves[-1] == 'E':
        moves.append('S')
        return 'S'

    #2 hit bottom moving left
    if north == False and east == False and moves[-1] != 'W':
        north = True
        moves.append('W')
        return 'W'

    #2a hit top, but just moved right
    if north == False and east == False and moves[-1] == 'W':
        moves.append('S')
        return 'S'

    #3
    if north == True and east == True and moves[-1] != 'E':
        north = False
        moves.append('E')
        return 'E'

    #3a
    if north == True and east == True and moves[-1] == 'E':
        moves.append('N')
        return 'N'

    #4
    if north == True and east == False and moves[-1] != 'W':
        north = False
        moves.append('W')
        return 'W'

    #4a
    if north == True and east == False and moves[-1] == 'W':
        moves.append('N')
        return 'N'


    return 0 #this needs to be a movement command string, or never reached






#in the case of a pit, the main movement function sends us here in order to try and get to the next desired tile, takes over for main movement function until it has reached this
def pit(percepts):
    #currentPercept = p
    perceptList = percepts
    global moves
    global case
    global north
    global east
    print("In pit case")

    if case != 0:
        if case == 1 or case == 3: #moving down to the right, we previously saw a pit and moved backwards ( indicated by case), now we continue east
            case = 5
            return 'E'
        
        if case == 2 or case == 4: #moving down to the left, we saw a pit, moved backwards (case), and now we continue west
            case = 5
            return 'W'

        if case == 5: #if we just dodged a pit, we want to ignore it because we may see it again
            case = 0
            if north == True:
                return 'N'
            else:
                return 'S'


    if north == False:

        if east == True:
            case = 1
            north = True
            return 'N'
        if east == False:
            case = 2
            north = True
            return 'N'


    if north == True:

        if east == True:
            case = 3
            north = False
            return 'S'
        if east == False:
            case = 4
            north = False
            return 'S'







#In the case of a wumpus, mmain movement function sends us here in order to try and kill it. Based on the current movement, it shoots in the two squares that the wumpus could possibly be in
def wumpus():
    #count = randint(0,3)
    global numArrows
    global north
    global east
    global case


    if numArrows == 0: #if we are out of arrows, just keep moving and hope for the best
        if north == False:
            case = 0
            return 'S'
        else:
            case = 0
            return 'N'


    if case == 20: #if we are dealing with a case where we just shot once...
        if north == True:
            case = 0
            numArrows = numArrows - 1
            return "SN" #finish off the second possible wumpus with the second shot
        else:
            case = 0
            numArrows = numArrows - 1
            return 'SS'


    if east == True: #if we are moving to the right
        case = 20 #case for if we need to shoot another arrow up/down next turn
        numArrows = numArrows - 1
        return 'SE' #shoot to the right

    if east == False: #or if we are moving to the left
        case = 20 #case for if we need to shoot another arrow up/down next turn
        numArrows = numArrows - 1
        return 'SW' #shoot to the left



    # if numArrows > 0 and count == 0:
    #     numArrows = numArrows- 1
    #     return('SN')
    # if numArrows > 0 and count == 1:
    #     numArrows = numArrows- 1
    #     return('SE')
    # if numArrows > 0 and count == 2:
    #     numArrows = numArrows- 1
    #     return('SS')
    # if numArrows > 0 and count == 3:
    #     numArrows = numArrows- 1
    #     return('SW')
    # else:
    #     if north == True:
    #          return 'N'
    #     else:
    #         return 'S' #temporary
        #return 'G' causes an infinite loop because we don't move, changed it to 'S' temporarily
    
    


def escape(percepts):
    perceptList = percepts #list of percepts for deciding what to do once we are here. You could call any function from here.
    #s = map[(currentRoom.getX, currentRoom.getY -1)]
    #n = map[(currentRoom.getX, currentRoom.getY +1)]
    #w = map[(currentRoom.getX +1, currentRoom.getY)]
    #e = map[(currentRoom.getX +1, currentRoom.getY)]
    return 0 #temporary, will count as invalid percept but at least we know we got the gold
