import pygame
pygame.init()
fontObj = pygame.font.Font('./assets/fonts/Pixeltype.ttf', 50)


class Button():
    def __init__(self, screen, x_pos, y_pos, text_input, callback):
        self.screen = screen
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.callback = callback
        width = 400
        height = 80
        self.normalCol = (50, 50, 50, 200)
        self.highlightCol = (80, 80, 80, 200)
        self.text_input = text_input
        self.rect = pygame.Rect(
            x_pos-(width/2), y_pos-(height/2), width, height)
        self.button = pygame.Surface((width, height))
        self.button.fill(self.normalCol)
        self.rect = self.button.get_rect(center=(self.x_pos, self.y_pos))
        self.text = fontObj.render(self.text_input, True, "white")
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self):
        self.screen.blit(self.button, self.rect)
        self.screen.blit(self.text, self.text_rect)

    def checkForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.callback()

    def changeColor(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.text = fontObj.render(self.text_input, True, "red")
            self.button.fill(self.highlightCol)
        else:
            self.text = fontObj.render(self.text_input, True, "white")
            self.button.fill(self.normalCol)
