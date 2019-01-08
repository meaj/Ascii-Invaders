import time
import msvcrt
import os

# Sets the initial positions of the enemies
def setEnemies(enemies):
    position = [0, 2]
    fireOrder = 1
    for enemy in enemies:
        enemy[0] = position[0]
        enemy[1] = position[1]
        if position[1] > 43:
            position[0] += 1
            position[1] = -1
        position[1] += 3
        if enemy[0] == 3:
            enemy[3] = fireOrder
            fireOrder += 1
    return enemies


# Enemies will call this to ensure they can fire
def hasClearShot():
    return False


# Handles firing for player and enemy
def fire(entity,  projectiles):
    if entity[2] == 0:
        entity[2] = 1
        print("fire")
        projectiles[entity[3]] = [entity[0]+entity[4], entity[1], entity[4]]


# Checks for keyboard input for player movement and firing
def getKeypress(player, projectiles):
    press = msvcrt.kbhit()
    if press:
        key = ord(msvcrt.getch())
        if key == 32:
            fire(player, projectiles)
        if key == 77:
            print('right')
            if player[1] < 48:
                player[1] += 1
        if key == 75:
            print('left')
            if player[1] > 1:
                player[1] -= 1


# Resets player position and lowers lives
def killPlayer(iLives, player):
    iLives-=1
    player = [14, 24]
    return iLives, player


# Clears the command prompt
def clear():
    if os.name =='nt':
        _ = os.system('cls')
    else:
        _ = os.system("clear")


# Updates the positions of player and enemies on the game board
def updateBoard(enemies, player, projectiles, gameGrid):
    # wipe board
    gameGrid = [[' ' for i in range(50)] for j in range(15)]

    # update game grid with player position
    gameGrid[player[0]][player[1]] = '^'

    # update gmame grid with all enemy positions
    for enemy in enemies:
        # print("Printing enemy at position: " + str(i) + ":" + str(j))
        gameGrid[enemy[0]][enemy[1]] = 'v'

    for projectile in projectiles:
        if projectile != [-1, -1, 0]:
            gameGrid[projectile[0]][projectile[1]] = '|'

    return gameGrid


# Prints game grid, lives and score
def printBoard(iLives, iScore, gameGrid):
    # Clear screen
    clear()
    # Print each row of the board, starting and ending each one with a ':'
    for row in gameGrid:
        print(":", end='', flush=False)
        for entry in row:
            print(entry, end='', flush=False)
        print(":", end='\n', flush=False)

    # Prints game data and flushes print buffer
    out = ["Score : " + str(iScore),"ASCII INVADERS", "Lives : " +  str(iLives)]
    print("{:<12}{:^26}{:^20}".format(*out))



def main():
    # Main game variables
    iScore = 0
    iLives = 3
    # Player position at default location, with fire state of 0, fire order of 0, and heading of -1
    player = [14, 24, 0, 0, -1]
    # Grid which will contain the game entities
    gameGrid = [['*' for i in range(50)] for j in range(15)]
    # Array of possible projectiles, and their headings
    projectiles = [[-1,-1, 0] for i in range(16)]
    # Array of enemy locations which are set to default positions and fire states of 0 as well as fire order assignment and heading of 1
    enemies = [[-1, -1, 0, 1] for i in range(60)]
    enemies = setEnemies(enemies)

    # Game Loop
    print(enemies)
    while iLives != 0 and iScore < 600:

        # Input Checking
        getKeypress(player, projectiles)
        # Collision Checking

        # Position Checking

        # Updates the Game Grid after position checking
        gameGrid = updateBoard(enemies, player,projectiles,  gameGrid)
        #print(projectiles)
        # Prints Game Grid after updating
        printBoard(iLives, iScore, gameGrid)

        # Sleeps for 1/30th of a second
        time.sleep(.032)
        #iLives = 0


main()