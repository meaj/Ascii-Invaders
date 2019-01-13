"""
Ascii Invaders
 * A minimalist version of an arcade classic, Space Invaders, using ascii characters and a terminal window for graphics
 * By Kevin Moore
"""
import time
import random
import msvcrt
import copy
import os


# A class which represents the projectile entities
class Entity:
    def __init__(self, active=False,  x_pos=-1, y_pos=-1, heading=0):
        self.active = active
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.heading = heading

    def set_all_values(self, active=False, x_pos=-1, y_pos=-1, heading=0):
        self.active = active
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.heading = heading

    def set_coordinates(self, x_val, y_val):
        self.x_pos = x_val
        self.y_pos = y_val

    def set_x(self, x_val):
        self.x_pos = x_val

    def set_y(self, y_val):
        self.y_pos = y_val

    def set_heading(self, heading):
        self.heading = heading

    def get_heading(self):
        return self.heading

    def get_x(self):
        return self.x_pos

    def get_y(self):
        return self.y_pos

    def set_active(self, active):
        self.active = active

    def is_active(self):
        return self.active

    def disable(self):
        self.active = False
        self.x_pos = -1
        self.y_pos = -1
        self.heading = 0


# A class which represents the player and enemy entities, it inherits from the Entity class
class VehicleEntity(Entity):
    def __init__(self, active=False, x_pos=-1, y_pos=-1, firing=False, fire_order=-1, heading=0):
        super().__init__(active, x_pos, y_pos, heading)
        self.firing = firing
        self.fire_order = fire_order

    def set_all_values(self, active=False, x_pos=-1, y_pos=-1, firing=False, fire_order=-1, heading=0):
        super().set_all_values(active, x_pos, y_pos, heading)
        self.firing = firing
        self.fire_order = fire_order

    def set_fire_order(self, fire_order):
        self.fire_order = fire_order

    def get_fire_order(self):
        return self.fire_order

    def get_coordinates_array(self):
        coordinates = [self.x_pos, self.y_pos]
        return coordinates

    def shift_down(self):
        self.x_pos += 1

    def toggle_fired(self):
        self.firing = not self.firing

    def reload(self):
        self.firing = False

    def disable(self):
        super().disable()
        self.firing = False
        self.fire_order = -1


# Clears the window
def clear():
    if os.name == 'nt':
        _ = os.system('cls')
    else:
        _ = os.system("clear")


# Sets the initial positions of the enemies
def set_enemies_to_default(list_of_enemies):
    position = [0, 2]
    fire_order = 1
    for enemy in list_of_enemies:
        enemy.set_coordinates(position[0], position[1])
        if position[1] > 43:
            position[0] += 1
            position[1] = -1
        position[1] += 3
        if enemy.get_x() == 1:
            enemy.set_fire_order(fire_order)
            enemy.set_heading(1)
            fire_order += 1
        enemy.set_active(True)
    return list_of_enemies


# Verifies that the space below an enemy is not occupied so that they can fire
def enable_fire(entity, list_of_enemies):
    for enemy in list_of_enemies:
        if enemy.get_coordinates_array() == [entity.get_x() - 1, entity.get_y()]:
            enemy.set_fire_order(entity.get_fire_order())
            enemy.set_heading(entity.get_heading())
    return list_of_enemies


def update_firing_order(list_of_enemies, list_of_projectiles):
    random.seed()
    for enemy in list_of_enemies:
        if enemy.get_fire_order() != -1 and random.randint(1, 15) == enemy.get_fire_order():
            fire(enemy, list_of_projectiles)
    return list_of_enemies, list_of_projectiles


# Handles firing for player and enemy
def fire(entity, list_of_projectiles):
    if not entity.firing:
        entity.toggle_fired()
        list_of_projectiles[entity.fire_order].set_all_values(True, entity.x_pos + entity.heading,
                                                              entity.y_pos, entity.heading)


# Checks for keyboard input for player movement and firing
def get_keypress(player_entity, list_of_projectiles):
    keypress = msvcrt.kbhit()
    if keypress:
        pos = player_entity.get_y()
        key = ord(msvcrt.getch())
        if key == 32:
            fire(player_entity, list_of_projectiles)
        if key == 77:
            if pos < 48:
                player_entity.set_y(pos+1)
        if key == 75:
            if pos > 1:
                player_entity.set_y(pos-1)


# Resets player position and lowers lives
def kill_player(int_lives, player_entity):
    int_lives -= 1
    player_entity.set_all_values(True, 14, 24, False, 0, -1)
    return int_lives, player_entity


# Checks for collisions between entities
def has_collision(entity_one, entity_two):
    if entity_one.get_x() == entity_two.get_x() and entity_one.get_y() == entity_two.get_y():
        return True
    return False


# Moves the projectiles
def move_projectiles(list_of_projectiles, list_of_enemies, player_entity):
    int_count = 0
    for projectile_entity in list_of_projectiles:
        pos = projectile_entity.get_x()
        # If projectile is in bounds, move it in the appropriate direction
        if 0 < pos < 14:
            projectile_entity.set_x(pos + projectile_entity.get_heading())
        # If out of bounds, allow entity to fire again
        else:
            # Check for appropriate entity to reload
            if int_count == 0:
                player_entity.reload()
            else:
                for enemy in list_of_enemies:
                    if enemy.get_fire_order() == int_count:
                        enemy.reload()
            projectile_entity.disable()
        int_count += 1

    return list_of_projectiles


# Moves the enemies
def move_enemies(list_of_enemies, int_direction, int_lives):
    list_of_future_positions = copy.deepcopy(list_of_enemies)
    bool_shift_down = False

    # Move all enemies in the current direction
    for temp_entity in list_of_future_positions:
        if not temp_entity.is_active():
            continue
        pos = temp_entity.get_y() + int_direction
        # If any entity is past either boundary, cancel directional movement and shift down
        if pos >= 50 or pos < 0:
            int_direction *= -1
            bool_shift_down = True
            break
        else:
            temp_entity.set_y(pos)

    # If an enemy has hit the wall, we cancel left/right movement and shift all entities down
    if bool_shift_down:
        for enemy_entity in list_of_enemies:
            if not enemy_entity.is_active():
                continue
            enemy_entity.shift_down()
            # If any entity shifts down off the screen, deduct a life
            if enemy_entity.get_x() == 14:
                int_lives -= 1
                enemy_entity.disable()
    else:
        list_of_enemies = list_of_future_positions

    return list_of_enemies, int_direction, int_lives


# Updates the positions of player and enemies on the game board
def update_board(list_of_enemies, player_entity, list_of_projectiles, game_grid):
    # wipe board
    del game_grid
    game_grid = [[' ' for i in range(50)] for j in range(15)]

    # update game grid with player position
    game_grid[player_entity.get_x()][player_entity.get_y()] = '^'

    # update game grid with all enemy positions
    for enemy_entity in list_of_enemies:
        if enemy_entity.is_active():
            game_grid[enemy_entity.get_x()][enemy_entity.get_y()] = 'v'

    # update game grid with all projectile positions
    for projectile_entity in list_of_projectiles:
        if projectile_entity.is_active():
            game_grid[projectile_entity.get_x()][projectile_entity.get_y()] = '|'

    return game_grid


# Prints game grid, lives and score
def print_board(int_lives, int_score, game_grid):
    # Construct board string out of each entry of each row of the board, starting and ending each row with a ':'
    board_string = ""
    for row in game_grid:
        board_string += ":"
        for entry in row:
            board_string += entry
        board_string += ":\n"

    # Prints game data
    out = [board_string, "Score : " + str(int_score), "ASCII INVADERS", "Lives : " + str(int_lives)]
    clear()
    print("{}{:<12}{:^26}{:^20}".format(*out))


def main():
    # Set console to fit game grid
    os.system('mode con: cols=52 lines=20')

    # Display variables
    bool_loaded = False
    bool_in_menu = True
    bool_quit = False
    str_play = "PLAY"
    str_exit = "EXIT"

    while not bool_quit:
        # Game Entity Creation
        # Each item displayed on the game grid is an instance of the Entity class. Some Entities, such as projectiles,
        # move within bounds and collide with other entities. VehicleEntities are a special instance of Entity that can
        # enter a state called "firing" which allows them to begin the movement of the projectile associated with it's
        # fire_order. VehicleEntites with no fire_order cannot fire and are typically blocked by another VehicleEntity
        if not bool_loaded:
            # Timing Variables
            frame_count = 0

            # Main game variables
            int_score = 0
            int_lives = 3
            int_direction = 1

            # Grid which will contain the game entities
            game_grid = [['*' for i in range(50)] for j in range(15)]

            # Player entity, has position at default location, with fire state of False, fire order 0, and heading of -1
            player_entity = VehicleEntity(True, 14, 24, False, 0, -1)

            # Array of enemy entities, which have locations which are set to default positions
            # and fire states of 0 as well as fire order assignment, and heading of 1
            list_of_enemies = [VehicleEntity() for i in range(30)]
            list_of_enemies = set_enemies_to_default(list_of_enemies)

            # Array of possible projectile entities, with their locations and their headings
            list_of_projectiles = [Entity(False, -1, -1, 0) for i in range(16)]

            # Signal that entities have been created
            bool_loaded = True

        # Game Loop
        start = time.clock()
        while bool_loaded and int_lives > 0 and int_score < 300:

            # Input Checking every frame
            get_keypress(player_entity, list_of_projectiles)

            # Projectile movement every three frames
            if frame_count % 3 == 0:
                list_of_projectiles = move_projectiles(list_of_projectiles, list_of_enemies, player_entity)

            # Check for enemy collision with player projectile once per frame
            for enemy_entity in list_of_enemies:
                if enemy_entity.is_active():
                    if has_collision(enemy_entity, list_of_projectiles[0]):
                        player_entity.reload()
                        list_of_projectiles[0].disable()
                        list_of_enemies = enable_fire(enemy_entity, list_of_enemies)
                        enemy_entity.disable()
                        int_score += 10

            # Checks for projectile collision with player once per frame
            int_count = 0
            for projectile_entity in list_of_projectiles:
                if has_collision(player_entity, projectile_entity):
                    for enemy in list_of_enemies:
                        if enemy.get_fire_order() == int_count:
                            enemy.reload()
                            list_of_projectiles[int_count].disable()
                            int_lives, player_entity = kill_player(int_lives, player_entity)
                int_count += 1

            # Enemy Movement once every 15 frames
            if frame_count % 15 == 0:
                list_of_enemies, int_direction, int_lives = move_enemies(list_of_enemies, int_direction, int_lives)
                list_of_enemies, list_of_projectiles = update_firing_order(list_of_enemies, list_of_projectiles)
                if int_lives < 1:
                    int_lives = 0

            # Updates the Game Grid after position checking once per frame
            game_grid = update_board(list_of_enemies, player_entity, list_of_projectiles, game_grid)

            # Prints Game Grid after updating once per frame
            print_board(int_lives, int_score, game_grid)

            # Timing Calculations, should cause loop to run roughly once every 30th of a second
            frame_count += 1
            delay = 0.032323232 - (time.clock() - start)
            if delay < 0:
                delay = 0
            time.sleep(delay)
            start = time.clock()

        # Exits or resets the game
        print("Game Over")
        str_replay = input("Enter Q to quit, or any other key to play again\n")
        if str_replay.lower() == "q":
            bool_quit = True
        else:
            bool_loaded = False
            del game_grid
            del player_entity
            for enemy in list_of_enemies:
                del enemy
            for projectile in list_of_projectiles:
                del projectile


main()
