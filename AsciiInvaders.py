"""
Ascii Invaders
 * A minimalist version of an arcade classic, Space Invaders, using ascii characters and a terminal window for graphics
 * Copyright (C) 2019 Meaj

 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.

 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.

 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import os
import pdb

from GameVariables import GameVariables


def main():
    #pdb.set_trace()

    # Set console to fit game grid
    os.system('mode con: cols=52 lines=20')

    # Display variables
    bool_loaded = True
    bool_started = False
    bool_quit = False

    # Initial game variables
    game_vars = GameVariables()

    while not bool_quit:
        # Resets game for replay
        if not bool_loaded:
            game_vars = GameVariables()
            bool_loaded = True

        # Start menu loop
        if not bool_started:
            game_vars.enter_menu()
            game_vars.update_board()
            while game_vars.is_in_menu():
                game_vars.print_game_start()
                game_vars.get_keypress()
                if game_vars.is_selection_confirmed():
                    if game_vars.is_replay_selected():
                        bool_started = True
                        break
                    else:
                        bool_quit = True
                        game_vars.exit_menu()
                game_vars.advance_frame()

        # Game Loop
        if not bool_quit:
            while game_vars.is_playing():
                # Input Checking every frame
                game_vars.get_keypress()
                # Projectile movement every three frames
                game_vars.move_projectiles()
                # Check for collisions
                game_vars.check_collisions()
                # Enemy Movement once every 15 frames
                game_vars.move_enemies()
                # Updates the Game Grid after position checking once per frame
                game_vars.update_board()
                # Prints Game Grid after updating once per frame
                game_vars.print_board()
                # Timing Calculations, should cause loop to run roughly once every 30th of a second
                game_vars.advance_frame()

            game_vars.enter_menu()
            while game_vars.is_in_menu():
                # Exits or resets the game
                game_vars.print_game_over()
                game_vars.get_keypress()
                if game_vars.is_selection_confirmed():
                    if game_vars.is_replay_selected():
                        bool_loaded = False
                        del game_vars
                        break
                    else:
                        bool_quit = True
                        game_vars.exit_menu()
                game_vars.advance_frame()


main()
