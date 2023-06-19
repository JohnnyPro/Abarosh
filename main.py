from main_menu import MainMenu
from game import Game
from game_over import GameOver

from state import State


State.currentPage = "MAINMENU"
quit = False
while not quit:
    if State.currentPage == "MAINMENU":
        MainMenu()

    elif State.currentPage == "PLAY":
        game = Game()
        game.run()

    elif State.currentPage == "QUIT":
        quit = True

    elif State.currentPage == "GAMEOVER":
        GameOver()
