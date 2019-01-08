"""
Ascii Invaders
 * A minimalist version ofan  arcade classic, Space Invaders, using ascii characters and a terminal window for graphics.
 * By Kevin Moore
"""
import time
import msvcrt
import os


# Sets the initial positions of the enemies
def set_enemies_to_default(list_of_enemies):
    position = [0, 2]
    fire_order = 1
    for enemy in list_of_enemies:
        enemy[0] = position[0]
        enemy[1] = position[1]
        if position[1] > 43:
            position[0] += 1
            position[1] = -1
        position[1] += 3
        if enemy[0] == 3:
            enemy[3] = fire_order
            fire_order += 1
    return list_of_enemies


# Enemies will call this to ensure they can fire
def has_clear_shot():
    return False


# Handles firing for player and enemy
def fire(entity, list_of_projectiles):
    if entity[2] == 0:
        entity[2] = 1
        print("fire")
        list_of_projectiles[entity[3]] = [entity[0] + entity[4], entity[1], entity[4]]


# Checks for keyboard input for player movement and firing
def get_keypress(player_entity, list_of_projectiles):
    keypress = msvcrt.kbhit()
    if keypress:
        key = ord(msvcrt.getch())
        if key == 32:
            fire(player_entity, list_of_projectiles)
        if key == 77:
            print('right')
            if player_entity[1] < 48:
                player_entity[1] += 1
        if key == 75:
            print('left')
            if player_entity[1] > 1:
                player_entity[1] -= 1


# Resets player position and lowers lives
def kill_player(int_lives, player_entity):
    int_lives -= 1
    player_entity = [14, 24, 0, 0, -1]
    return int_lives, player_entity


# Clears the command prompt
def clear():
    if os.name == 'nt':
        _ = os.system('cls')
    else:
        _ = os.system("clear")


# Checks for collisions between entities
def has_collision(entity_one, entity_two):
    if entity_one == entity_two:
        return True
    return False


# Moves the projectiles
def move_projectiles(list_of_projectiles):
    for projectile_entity in list_of_projectiles:
        if -1 < projectile_entity[0] < 15:
            projectile_entity[0] += projectile_entity[2]
        else:
            projectile_entity = [-1, -1, 0]
    return list_of_projectiles


# Moves the enemies
def move_enemies(list_of_enemies, int_direction, int_lives):
    list_of_future_positions = list_of_enemies
    bool_shift_down = False

    # Move all enemies in the current direction
    for temp_entity in list_of_future_positions:
        # If any entity is past either boundary, cancel directional movement and shift down
        if temp_entity[1] + int_direction > 49 or temp_entity[1] + int_direction < -1:
            int_direction *= -1
            bool_shift_down = True
            break
        temp_entity[1] += int_direction

    if bool_shift_down:
        for enemy_entity in list_of_enemies:
            enemy_entity[0] += 1
            # If any entity shifts down off the screen, deduct a life
            if enemy_entity[0] == 14:
                int_lives -=1
                enemy_entity = [-1, -1, 0, 0, 1]
    else:
        list_of_enemies = list_of_future_positions

    print(list_of_enemies)

    return list_of_enemies, int_direction, int_lives


# Updates the positions of player and enemies on the game board
def update_board(list_of_enemies, player_entity, list_of_projectiles, game_grid):
    # wipe board
    game_grid = [[' ' for i in range(50)] for j in range(15)]

    # update game grid with player position
    game_grid[player_entity[0]][player_entity[1]] = '^'

    # update game grid with all enemy positions
    for enemy_entity in list_of_enemies:
        # print("Printing enemy at position: " + str(i) + ":" + str(j))
        if enemy_entity[0] != -1:
            game_grid[enemy_entity[0]][enemy_entity[1]] = 'v'

    # update game grid with all projectile positions
    for projectile_entity in list_of_projectiles:
        if projectile_entity != [-1, -1, 0]:
            game_grid[projectile_entity[0]][projectile_entity[1]] = '|'

    return game_grid


# Prints game grid, lives and score
def print_board(int_lives, int_score, game_grid):
    # Clear screen
    clear()

    # Print each row of the board, starting and ending each one with a ':'
    for row in game_grid:
        print(":", end='', flush=False)
        for entry in row:
            print(entry, end='', flush=False)
        print(":", end='\n', flush=False)

    # Prints game data and flushes print buffer
    out = ["Score : " + str(int_score), "ASCII INVADERS", "Lives : " + str(int_lives)]
    print("{:<12}{:^26}{:^20}".format(*out))


def main():
    # Set console to fit game grid
    os.system('mode con: cols=52 lines=16')

    # Main game variables
    int_score = 0
    int_lives = 3
    int_direction = 1

    # Player entity, has position at default location, with fire state of 0, fire order of 0, and heading of -1
    player_entity = [14, 24, 0, 0, -1]

    # Array of enemy entities, which have locations which are set to default positions
    # and fire states of 0 as well as fire order assignment, and heading of 1
    list_of_enemies = [[-1, -1, 0, 0, 1] for i in range(30)]
    list_of_enemies = set_enemies_to_default(list_of_enemies)

    # Grid which will contain the game entities
    game_grid = [['*' for i in range(50)] for j in range(15)]

    # Array of possible projectile entities, with their locations and their headings
    list_of_projectiles = [[-1, -1, 0] for i in range(16)]

    # Game Loop
    print(list_of_enemies)
    while int_lives != 0 and int_score < 300:

        # Input Checking
        get_keypress(player_entity, list_of_projectiles)

        # Projectile movement
        list_of_projectiles = move_projectiles(list_of_projectiles)

        # Check for enemy collision with player projectile
        for enemy_entity in list_of_enemies:
            if has_collision(enemy_entity, list_of_projectiles[0]):
                int_score += 10
                enemy_entity[0] = [-1, -1, 0, 0, 1]

        # Checks for projectile collision with player
        for projectile_entity in list_of_projectiles:
            if has_collision(player_entity, projectile_entity):
                int_lives, player_entity = kill_player(int_lives, player_entity)

        # Enemy Movement
        list_of_enemies, int_direction, int_lives = move_enemies(list_of_enemies, int_direction, int_lives)

        # Updates the Game Grid after position checking
        game_grid = update_board(list_of_enemies, player_entity, list_of_projectiles, game_grid)

        # Prints Game Grid after updating
        print_board(int_lives, int_score, game_grid)

        # Sleeps for 1/15th of a second
        time.sleep(.064)

        # Used for testing starting frame:
        # int_lives = 0

main()
