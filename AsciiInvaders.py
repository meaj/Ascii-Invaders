"""
Ascii Invaders
 * A minimalist version of an arcade classic, Space Invaders, using ascii characters and a terminal window for graphics
 * By Kevin Moore
"""
import os

from GameVariables import GameVariables


def main():
    # Set console to fit game grid
    os.system('mode con: cols=52 lines=20')

    # Display variables
    bool_loaded = True
    bool_quit = False
    str_play = "PLAY"
    str_exit = "EXIT"

    while not bool_quit:
        game_vars = GameVariables()
        bool_quit = False

        # Start menu loop
        game_vars.enter_menu()
        game_vars.update_board()
        while game_vars.is_in_menu():
            game_vars.print_game_start()
            game_vars.get_keypress()
            if game_vars.get_confirm():
                if game_vars.get_replay():
                    break
                else:
                    bool_quit = True
                    game_vars.exit_menu()
            game_vars.advance_frame()

        if not bool_loaded and not bool_quit:
            game_vars = GameVariables()
            bool_loaded = True

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
                if game_vars.get_confirm():
                    if game_vars.get_replay():
                        bool_loaded = False
                        del game_vars
                        break
                    else:
                        bool_quit = True
                        game_vars.exit_menu()
                game_vars.advance_frame()




main()
