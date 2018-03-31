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

import random

def printBrd(brd):
    """ Outputs the board represented by 'brd' to the screen"""
    print(brd[0],"|",brd[1],"|",brd[2], sep="")
    print("-----")
    print(brd[3],"|",brd[4],"|",brd[5], sep="")
    print("-----")
    print(brd[6],"|",brd[7],"|",brd[8], sep="")

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


# ========================
# MAIN PROGRAM STARTS HERE
# ========================

#set up a blank board and an empty gamelist
board="         "
GameList={}
printBrd("012345678")

#this is the main gaim loop. Break from the loop with the game if NOT "No result yet (N)" ie: when there is a result
while True:
    board=humanMove(board)
    GameList[board]=0
    #printBrd(board)
    if isGameWon(board)!="N":
        break
    
    #board=getOMove(board)
    board=random.choice(nextMoves(board))
    GameList[board]=0
    printBrd(board)
    if isGameWon(board)!="N":
        break
    
#when the game is over, declare the winner
printBrd(board)
gameResult = isGameWon(board)
if gameResult=="D":
    print("The game was a draw")
else:
    print(gameResult, "wins!")

#If the game was not a draw, assign votes to the GameList
#Each move by the winning player gets one vote
if isGameWon(board) != "D":
    #work out whether to start with a "1" (player one won) or a "0" (player 2 won)
    if isGameWon(board) == "X":
        vote=1
    else:
        vote=0
    # then toggle between "1" and "O" along the moves in the GameList
    for i in GameList:
        GameList[i]=vote
        vote=(vote+1)%2

#Print out the GameList, showing votes
print("GameList:")
for i in GameList:
    print(i," : ",GameList[i])

