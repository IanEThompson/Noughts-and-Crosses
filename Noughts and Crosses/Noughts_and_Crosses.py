#
#   Noughts and Crosses Game
#   ========================
#
#   Ian Thompson 2018
#   0414270210  ianmelandkids@gmail.com
#   
#   Plays noughts and crosses. Currently between two players
#   but will eventually be between a human and a "learning" computer
#
#   The board is represented by a string of exactly nine characters.
#   Each character represents a particular position on the board:
#
#       0|1|2
#       -----
#       3|4|5
#       -----
#       6|7|8
#
#   Each character can be "X" or "O" or " " (unoccupied)
#   So the board:
#   
#       X|X|O
#       -----
#       X| |O
#       -----
#       O|X|
#
#   Would be written as: "XXOX OOX " 

import random       #for choosing random moves
import collections  #gamelist needs to be an ordered dictionary

def printBrd(brd):
    """ Outputs the board represented by 'brd' to the screen"""
    print(brd[0],"|",brd[1],"|",brd[2], sep="")
    print("-----")
    print(brd[3],"|",brd[4],"|",brd[5], sep="")
    print("-----")
    print(brd[6],"|",brd[7],"|",brd[8], sep="")

def humanMove(brd):
    """ Gets the human's next move using the screen and keyboard """
    #determine which player is moving (assume X always moves first)
    if brd.count("O") == brd.count("X"):
        player="X"
    else:
        player="O"

    newBrd=""
    validMove=False
    while not validMove:
        print("You are ", player)
        strMove = input("What is your move? (0-8): ")
        move=int(strMove[0])
        if move<0 or move>8 or brd[move] != " ":
            print("Invalid move")
        else:
            validMove=True
            for i in range(0,9):
                if i == move:
                    newBrd=newBrd + player
                else:
                    newBrd = newBrd + brd[i]
    return newBrd

def isGameWon(brd):
    """ Check to see if the game has been won:
        Returns winner: 'X', 'O' or 'D' (Draw) or 'N' (no result yet)
        Rotates a copy of the board 3 times looking for: three on the top row, three on the middle row, three diagonal
    """
    #look for a winning combination by either X or O by checking for 3 patterns, with various rotations
    for r in range(0,4):
        for i in "OX":
            if brd[0]==i and brd[1]==i and brd[2]==i:
                return i
            elif brd[0]==i and brd[4]==i and brd[8]==i:
                return i
            elif brd[3]==i and brd[4]==i and brd[5]==i:
                return i
        brd=tfRotate(brd)
    
    #no winner, so check for a draw (board has no empty spaces)
    if brd[:9].count(" ")==0:
        return "D"

    #If there's no winner, and no draw, the game is still underway:
    return "N"

def nextMoves(brd):
    """ Creates a list of all possible next moves
        Assumes "X" always goes first when determining whose turn it is
    """
    if brd.count("O") == brd.count("X"):
        player="X"
    else:
        player="O"

    nextMoveList=[]
    for i in range(0,9):
        if brd[i]==" ":
            newBrd=""
            for j in range(0,9):
                if j == i:
                    newBrd=newBrd + player
                else:
                    newBrd = newBrd + brd[j]
            nextMoveList.append(newBrd)
    return nextMoveList

def tfRotate(brd):
    """ Returns a string representing the board rotated once clockwise """
    newBrd=brd[6] + brd[3] + brd[0] + brd[7] + brd[4] + brd[1] + brd[8]+ brd[5] + brd[2]
    return newBrd

def tfUnrotate(brd):
    """ Returns a string representing the board rotated once anti-clockwise """
    newBrd=brd[2] + brd[5] + brd[8] + brd[1] + brd[4] + brd[7] + brd[0]+ brd[3] + brd[6]
    return newBrd

def tfFlip(brd):
    """ Returns a string representing the board flipped (refelcted) about the diagonal"""
    newBrd=brd[0] + brd[3] + brd[6] + brd[1] + brd[4] + brd[7] + brd[2]+ brd[5] + brd[8]
    return newBrd

def tfToggle(brd):
    """ Returns a string representing the board with O and X toggled"""
    newBrd=""
    for digit in brd:
        if digit == 'X':
            newBrd=newBrd + "O"
        elif digit == 'O':
            newBrd=newBrd + "X"
        else:
            newBrd=newBrd + " "
    return newBrd

def tfInt(brd):
    """Returns the board as an int with
        empty = 0
            O = 1
            X = 2
    """
    newBrd=""
    for digit in brd:
        if digit == 'X':
            newBrd=newBrd + "2"
        elif digit == 'O':
            newBrd=newBrd + "1"
        else:
            newBrd=newBrd + " "
    return newBrd

def rootBoard(brd):
    """ Returns a string representing a unique 'root' board for the given board
    """
    rootScore=0     #the "score" of the highest scoring board
    seqCount=0      #track the number of transforms so far
    tfBrd=brd       #the board after the latest transform

    tfSequence="rrrrfrrrr"
    
    #execute the next transform in the sequence
    for tf in list(tfSequence):
        if tf=="r":
            tfBrd=tfRotate(tfBrd)
        elif tf=="f":
            tfBrd=tfFlip(tfBrd)

        #score the transformed board by converting it into an integer
        Score = int(tfBrd.replace("X","2").replace("O","1").replace(" ","0"))
        #remember the best scoring board AND the number of transforms required to get to it
        if Score > rootScore:
            rootScore = Score
            rootBrd = tfBrd
    return rootBrd

def findBestMove(brd):
    maxVotes=0
    bestMove=random.choice(nextMoves(board))
    
    if brd.count("O")<brd.count("X"):                           #if it's O's move
        for m in nextMoves(brd):
            if rootBoard(m) in O_Experience:                    #look for the best move in the experience list
                if O_Experience[rootBoard(m)] > maxVotes:
                    bestMove=m
                    maxVotes = O_Experience[rootBoard(m)]
        return bestMove

    if brd.count("X")==brd.count("O"):                           #if it's X's move
        for m in nextMoves(brd):
            if rootBoard(m) in X_Experience:                     #look for the best move in the experience list
                if X_Experience[rootBoard(m)] > maxVotes:
                    bestMove=m
                    maxVotes = X_Experience[rootBoard(m)]
        return bestMove



def learnFromGame(Game):
    """ Remembers the moves that lead to a win in the Xexperience or Oexperience dictionaries
    """
    global X_Experience     #use the global experience list for the X player
    global O_Experience     #use the global experience list for the O player
    
    lastBrd = next(reversed(Game))                      #get the last board in the Game to check the result
    Winner = isGameWon(lastBrd)
    
    if Winner == "D":                                   #If the game was a draw, do nothing!
        return

    if Winner == "X":
        for g in Game:
            if g.count("X")>g.count("O"):               #every move of X's was good!
                if g in X_Experience:
                    X_Experience[g]=X_Experience[g]+1   #if the move is known, increment vote
                else:
                    X_Experience[g]=1                   #else add it into the experience with vote=1
            
            else:                                       #every move of O's was bad!
                if g in O_Experience:
                    O_Experience[g]=O_Experience[g]-1   #if the move is known, decrement vote
                else:
                    O_Experience[g]=-1                  #else add it into the experience with vote=-11


    if Winner == "O":
        for g in Game:
            if g.count("O")==g.count("X"):               #every move of O's was good!
                if g in O_Experience:
                    O_Experience[g]=O_Experience[g]+1   #if the move is known, increment vote
                else:
                    O_Experience[g]=1                   #else add it into the experience with vote=1
            
            else:                                       #every move of X's was bad!
                if g in X_Experience:
                    X_Experience[g]=X_Experience[g]-1   #if the move is known, decrement vote
                else:
                    X_Experience[g]=-1                  #else add it into the experience with vote=-11

def printExperience():

    #Print out X_Experience, showing votes
    print("X Experience:")
    for x in X_Experience:
        print(x," : ",X_Experience[x])

    #Print out O_Experience, showing votes
    print("O Experience:")
    for x in O_Experience:
        print(x," : ",O_Experience[x])
    print("")


# ========================
# MAIN PROGRAM STARTS HERE
# ========================

X_Experience={}
O_Experience={}
computersTurn=False

#play games over and over
while True:

    #Initialise the game
    board="         "
    GameList=collections.OrderedDict()
    printBrd("012345678")
    
    if computersTurn:
        print("\nMy turn to go first!")

    #this is the main gaim loop. Break from the loop with the game if NOT "No result yet (N)" ie: when there is a result
    while True:
        
        if computersTurn:
            board=findBestMove(board)       #find the best move (based on experience)
            printBrd(board)                 #display the move
            computersTurn=False             #computers turn is over

        else:
            board=humanMove(board)          #get the human's move
            computersTurn=True              #human's move is over

        GameList[rootBoard(board)]=0        #record the move (for analysis later)
        if isGameWon(board)!="N":           #check to see if the game is over
            break    
    
    #when the game is over, declare the winner
    print("")
    gameResult = isGameWon(board)
    if gameResult=="D":
        print("The game was a draw")
    else:
        if computersTurn==True:              #if the human won, the board still needs to be displayed
            printBrd(board)
        print(gameResult, "wins!")

    print("")
    learnFromGame(GameList)                 #remember all the moves from the game for next time!

    #printExperience()                       #display the experience lists (optional)