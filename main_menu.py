import pygame
import sys
from ui_elements import Button
from state import State
from pygame import mixer


class MainMenu:
    def play(self):
        mixer.music.stop()
        State.currentPage = "PLAY"

    def quit(self):
        mixer.music.stop()

        State.currentPage = "QUIT"

    def __init__(self) -> None:
        pygame.init()

        screen = pygame.display.set_mode((800, 600))

        fontObj = pygame.font.Font('./assets/fonts/Pixeltype.ttf', 100)
        cursorFont = pygame.font.SysFont("cambria", 35)

        mixer.init()
        mixer.music.load('assets/audio/titleScreenMusic.wav')
        mixer.music.set_volume(0.2)
        mixer.music.play(-1)

        abaroshText = fontObj.render("Abarosh", True, "white")
        abaroshTextRect = abaroshText.get_rect(
            center=(screen.get_width()/2, 100))

        abaroshCover = pygame.image.load("assets/title_image/Abarosh.png")
        w, h = abaroshCover.get_size()
        aspectRatio = float(w)/h
        abaroshCover = pygame.transform.scale(
            abaroshCover, (250, 250/aspectRatio))
        abaroshCoverRect = abaroshCover.get_rect(
            center=(screen.get_width()/2, abaroshTextRect.bottom+130))

        buttons = []
        margin = 30
        play = Button(screen, 400,
                      abaroshCoverRect.bottom, "PLAY", self.play)
        quit = Button(screen, 400, margin +
                      play.rect.bottom, "QUIT", self.quit)
        buttons.append(play)
        buttons.append(quit)

        offsetX = 15
        offsetY = 8
        cursor = cursorFont.render(">", True, "white")
        cursorRect = cursor.get_rect(
            center=(play.rect.left+offsetX, play.rect.centery-offsetY))
        hoveredIdx = 0

        while State.currentPage == "MAINMENU":

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for button in buttons:
                        button.checkForInput(pygame.mouse.get_pos())
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        hoveredIdx += 1
                        if hoveredIdx >= len(buttons):
                            hoveredIdx = 0
                    if event.key == pygame.K_UP:
                        hoveredIdx -= 1
                        if hoveredIdx < 0:
                            hoveredIdx = len(buttons) - 1

                    if event.key == pygame.K_RETURN:
                        buttons[hoveredIdx].callback()

            screen.fill("black")
            screen.blit(abaroshCover, abaroshCoverRect)
            screen.blit(abaroshText, abaroshTextRect)

            for i, button in enumerate(buttons):
                button.update()
                if (button.changeColor(pygame.mouse.get_pos())):
                    hoveredIdx = i

            hoveredButton = buttons[hoveredIdx]
            cursorRect = cursor.get_rect(
                center=(hoveredButton.rect.left+offsetX, hoveredButton.rect.centery-offsetY))
            hoveredButton.textColChange()
            screen.blit(cursor, cursorRect)

            pygame.display.update()
