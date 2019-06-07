"""
Ascii Invaders - GameVariables
 * A class containing the major variables and functions used in Ascii Invaders
 * Copyright (C) 2019 Meaj
"""
import random
import msvcrt
import copy
import os
import time

from Entities import Entity, VehicleEntity
from playsound import playsound


class GameVariables:
    def __init__(self, frame_count=0, int_score=0, int_lives=3, int_direction=1):
            # Timing Variables
            self.frame_count = frame_count
            self.start = time.clock()

            self.bool_frame_sound = False
            self.bool_end_sound = False

            # Main game variables
            self.int_score = int_score
            self.int_lives = int_lives
            self.int_direction = int_direction

            # Grid which will contain the game entities
            self.game_grid = [['*' for i in range(50)] for j in range(15)]

            # Game Entity Creation
            # Each item displayed on the game grid is an instance of the Entity class. Some Entities, such as
            # projectiles, move within bounds and collide with other entities. VehicleEntities are a special instance
            # of Entity that can also enter a state called "firing" which allows them to begin the movement of the
            # projectile associated with it's fire_order. VehicleEntites with no fire_order cannot fire and are
            # typically blocked by another VehicleEntity

            # Player entity, has position at default location, with fire state of False, fire order 0, and heading of -1
            self.player_entity = VehicleEntity(True, 14, 24, False, 0, -1)

            # Array of enemy entities, which have locations which are set to default positions
            # and fire states of 0 as well as fire order assignment, and heading of 1
            self.list_of_enemies = [VehicleEntity() for i in range(30)]
            self.set_enemies_to_default()

            # Array of possible projectile entities, with their locations and their headings
            self.list_of_projectiles = [Entity(False, -1, -1, 0) for i in range(16)]

            self.selection = [">PLAY<", " QUIT "]
            self.confirm_selection = False
            self.in_menu = False

    # Sets the initial positions of the enemies
    def set_enemies_to_default(self):
        position = [0, 2]
        fire_order = 1
        for enemy in self.list_of_enemies:
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

    # Verifies that the space below an enemy is not occupied so that they can fire
    def enable_fire(self, entity):
        for enemy in self.list_of_enemies:
            if enemy.get_coordinates_array() == [entity.get_x() - 1, entity.get_y()]:
                enemy.set_fire_order(entity.get_fire_order())
                enemy.set_heading(entity.get_heading())

    # Preforms random firing and checks for changes to firing order
    def update_firing_order(self):
        random.seed()
        for enemy in self.list_of_enemies:
            if enemy.get_fire_order() != -1 and random.randint(1, 15) == enemy.get_fire_order():
                self.fire(enemy)

    # Handles firing for player and enemy
    def fire(self, entity):
        if not entity.firing:
            if not self.bool_frame_sound:
                playsound("sounds\shoot.wav", False)
                self.bool_frame_sound = True
            entity.toggle_fired()
            self.list_of_projectiles[entity.fire_order].set_all_values(True, entity.x_pos + entity.heading,
                                                                       entity.y_pos, entity.heading)

    # Sets the in_menu variable to true in order to enter menus
    def enter_menu(self):
        self.in_menu = True

    # Sets the in_menu variable and selection confirmation variables to false to exit menus
    def exit_menu(self):
        self.confirm_selection = False
        self.in_menu = False

    # Returns true if the player is in a menu
    def is_in_menu(self):
        return self.in_menu

    # Checks for player selection confirmation (Enter key press) in menu screens
    def is_selection_confirmed(self):
        return self.confirm_selection

    # Returns true if the player has selected to play or replay, false if the player wants to quit
    def is_replay_selected(self):
        if self.selection == [">PLAY<", " QUIT "]:
            return True
        else:
            return False

    # Checks for keyboard input for player movement and firing
    def get_keypress(self):
        keypress = msvcrt.kbhit()
        if keypress:
            pos = self.player_entity.get_y()
            key = ord(msvcrt.getch())
            if key == 32:
                self.fire(self.player_entity)
            if key == 13:
                if self.in_menu:
                    self.confirm_selection = True
            if key == 77:
                if self.in_menu:
                    self.selection = [" PLAY ", ">QUIT<"]
                if pos < 49:
                    self.player_entity.set_y(pos + 1)
            if key == 75:
                if self.in_menu:
                    self.selection = [">PLAY<", " QUIT "]
                if pos > 0:
                    self.player_entity.set_y(pos - 1)

    # Resets player position and lowers lives
    def kill_player(self):
        self.int_lives -= 1
        playsound("sounds\player_killed.wav", True)
        self.player_entity.set_all_values(True, 14, 24, False, 0, -1)

    @staticmethod
    # Checks for collisions between entities
    def has_collision(entity_one, entity_two):
        if entity_one.get_x() == entity_two.get_x() and entity_one.get_y() == entity_two.get_y():
            return True
        return False

    # Moves the projectiles
    def move_projectiles(self):
        if self.frame_count % 3 == 0:
            int_count = 0
            for projectile_entity in self.list_of_projectiles:
                pos = projectile_entity.get_x()
                # If projectile is in bounds, move it in the appropriate direction
                if 0 < pos < 14:
                    projectile_entity.set_x(pos + projectile_entity.get_heading())
                # If out of bounds, allow entity to fire again
                else:
                    # Check for appropriate entity to reload
                    if int_count == 0:
                        self.player_entity.reload()
                    else:
                        for enemy in self.list_of_enemies:
                            if enemy.get_fire_order() == int_count:
                                enemy.reload()
                    projectile_entity.disable()
                int_count += 1

    # Moves the enemies
    def move_enemies(self):
        if self.frame_count % 15 == 0:
            list_of_future_positions = copy.deepcopy(self.list_of_enemies)
            bool_shift_down = False

            # Move all enemies in the current direction
            for temp_entity in list_of_future_positions:
                if not temp_entity.is_active():
                    continue
                pos = temp_entity.get_y() + self.int_direction
                # If any entity is past either boundary, cancel directional movement and shift down
                if pos >= 50 or pos < 0:
                    self.int_direction *= -1
                    bool_shift_down = True
                    break
                else:
                    temp_entity.set_y(pos)

            # If an enemy has hit the wall, we cancel left/right movement and shift all entities down
            if bool_shift_down:
                for enemy_entity in self.list_of_enemies:
                    if not enemy_entity.is_active():
                        continue
                    enemy_entity.shift_down()
                    # If any entity shifts down off the screen, deduct a life
                    if enemy_entity.get_x() == 14:
                        self.int_lives -= 1
                        enemy_entity.disable()
            else:
                self.list_of_enemies = list_of_future_positions

            playsound("sounds\invader_move.wav", False)
            self.update_firing_order()
            if self.int_lives < 1:
                self.int_lives = 0

    # Preforms projectile collision checks for player and enemies
    def check_collisions(self):
        # Check for enemy collision with player projectile
        for enemy_entity in self.list_of_enemies:
            if enemy_entity.is_active():
                if self.has_collision(enemy_entity, self.list_of_projectiles[0]):
                    self.player_entity.reload()
                    self.list_of_projectiles[0].disable()
                    self.enable_fire(enemy_entity)
                    enemy_entity.disable()
                    playsound("sounds\invader_killed.wav", False)
                    self.int_score += 10

        # Checks for projectile collision with player
        int_count = 0
        for projectile_entity in self.list_of_projectiles:
            if self.has_collision(self.player_entity, projectile_entity):
                for enemy in self.list_of_enemies:
                    if enemy.get_fire_order() == int_count:
                        enemy.reload()
                        self.list_of_projectiles[int_count].disable()
                        self.kill_player()
            int_count += 1

    # Updates the positions of player and enemies on the game board
    def update_board(self):
        # wipe board
        del self.game_grid
        self.game_grid = [[' ' for i in range(50)] for j in range(15)]

        # update game grid with player position
        self.game_grid[self.player_entity.get_x()][self.player_entity.get_y()] = '^'

        # update game grid with all enemy positions
        for enemy_entity in self.list_of_enemies:
            if enemy_entity.is_active():
                self.game_grid[enemy_entity.get_x()][enemy_entity.get_y()] = 'v'

        # update game grid with all projectile positions
        for projectile_entity in self.list_of_projectiles:
            if projectile_entity.is_active():
                self.game_grid[projectile_entity.get_x()][projectile_entity.get_y()] = '|'

    # Prints game grid, lives and score
    def print_board(self):
        # Construct board string out of each entry of each row of the board, starting and ending each row with a ':'
        board_string = ""
        for row in self.game_grid:
            board_string += ":"
            for entry in row:
                board_string += entry
            board_string += ":\n"

        # Prints game data
        out = [board_string, "Score : " + str(self.int_score), "ASCII INVADERS", "Lives : " + str(self.int_lives)]
        os.system('cls')
        print("{}{:<12}{:^26}{:^20}".format(*out))

    # Prints the start menu
    def print_game_start(self):
        self.confirm_selection = False
        board_string = ""
        count = 0
        for row in self.game_grid:
            if count == 6:
                board_string += ":{:^50}:\n".format("ASCII INVADERS")
            elif count == 8:
                replay_string = self.selection
                board_string += ":{:>25}{:<25}:\n".format(*replay_string)
            else:
                board_string += ":"
                for entry in row:
                    board_string += entry
                board_string += ":\n"
            count += 1
        os.system('cls')
        print(board_string)

    # Prints the game over menu
    def print_game_over(self):
        if self.int_lives == 0 and not self.bool_end_sound:
            playsound("sounds\player_killed.wav", True)
            self.bool_end_sound = True
        self.confirm_selection = False
        board_string = ""
        count = 0
        for row in self.game_grid:
            if count == 6:
                board_string += ":{:^50}:\n".format("GAME OVER")
            elif count == 7:
                final_score = self.get_final_score()
                score_string = "FINAL SCORE : " + str(final_score)
                board_string += ":{:^50}:".format(score_string)
            elif count == 8:
                replay_string = self.selection
                board_string += ":{:>25}{:<25}:\n".format(*replay_string)
            else:
                board_string += ":"
                for entry in row:
                    board_string += entry
                board_string += ":\n"
            count += 1
        os.system('cls')
        print(board_string)

    # Returns true if the player is in game
    def is_playing(self):
        return self.int_lives > 0 and self.int_score < 300

    # Returns the final score which is calculated from the score plus 100 points for each life the player has remaining
    def get_final_score(self):
        return self.int_score + self.int_lives * 100

    # Smooths out framerate to slightly more than 30 fps
    def advance_frame(self):
        self.frame_count += 1
        delay = (1/60) - (time.clock() - self.start)
        if delay < 0:
            delay = 0
        time.sleep(delay)
        self.start = time.clock()
        self.bool_frame_sound = False
