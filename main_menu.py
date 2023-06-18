import pygame
import sys
from ui_elements import Button
from game import Game


class MainMenu:
    def play(self):

        game = Game()
        game.run()

    def quit(self):
        pygame.quit()
        sys.exit()

    def __init__(self) -> None:
        pygame.init()
        screen = pygame.display.set_mode((800, 600))
        fontObj = pygame.font.Font('./assets/fonts/Pixeltype.ttf', 100)
        abaroshText = fontObj.render("Abarosh", True, "black")
        abaroshTextRect = abaroshText.get_rect(
            center=(screen.get_width()/2, 100))
        abaroshCover = pygame.image.load("assets/title_image/Abarosh.png")
        w, h = abaroshCover.get_size()
        aspectRatio = float(w)/h
        abaroshCover = pygame.transform.scale(
            abaroshCover, (250, 250/aspectRatio))
        abaroshCoverRect = abaroshCover.get_rect(
            center=(screen.get_width()/2, abaroshTextRect.bottom+100))

        buttons = []
        margin = 50
        play = Button(screen, 400, 20 +
                      abaroshCoverRect.bottom, "PLAY", self.play)
        quit = Button(screen, 400, margin +
                      play.rect.bottom, "QUIT", self.quit)
        buttons.append(play)
        buttons.append(quit)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for button in buttons:
                        button.checkForInput(pygame.mouse.get_pos())

            screen.fill("white")
            screen.blit(abaroshCover, abaroshCoverRect)
            screen.blit(abaroshText, abaroshTextRect)
            for button in buttons:
                button.update()
                button.changeColor(pygame.mouse.get_pos())

            pygame.display.update()
