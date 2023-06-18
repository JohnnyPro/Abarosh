import pygame
pygame.init()
fontObj = pygame.font.Font('./assets/fonts/Pixeltype.ttf', 50)


class Button():
    def __init__(self, screen, x_pos, y_pos, text_input, callback):
        self.screen = screen
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.callback = callback
        width = 150
        height = 50
        self.normalCol = (50, 50, 50, 0)
        self.highlightCol = (50, 50, 50, 120)
        self.text_input = text_input
        self.button = pygame.Surface((width, height))
        self.button.fill(self.normalCol)
        self.button.set_alpha(self.normalCol[-1])

        self.rect = self.button.get_rect(center=(self.x_pos, self.y_pos))
        self.text = fontObj.render(self.text_input, True, "white")
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self):
        self.screen.blit(self.button, self.rect)
        self.screen.blit(self.text, self.text_rect)

    def checkForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.callback()

    def textColChange(self, backToNormal=False):
        if backToNormal:
            self.text = fontObj.render(self.text_input, True, "white")
            return
        self.text = fontObj.render(self.text_input, True, "red")

    def changeColor(self, position, hovered=False):
        if hovered or position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):

            # self.button.fill(self.highlightCol)
            # self.button.set_alpha(self.highlightCol[-1])
            return True
        else:
            self.textColChange(True)
            # self.button.fill(self.normalCol)
            # self.button.set_alpha(self.normalCol[-1])
            return False
