from abc import ABC
import pygame


class GameButton(ABC):
    # content parameter can be text or image
    def __init__(self, x, y, width, height, content, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.content = content
        self.color = color

    def is_over(self, pos):
        if self.x < pos[0] < self.x + self.width:
            if self.y < pos[1] < self.y + self.height:
                return True
        return False

    def draw(self, win):
        pass


class EndGameButton(GameButton):
    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont('comicsans', 40)
        text = font.render(self.content, 1, (0, 0, 0))
        win.blit(text, (int(self.x + self.width/2 - text.get_width()/2),
                        int(self.y + self.height/2 - text.get_height()/2)))


class FigureButton(GameButton):
    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 3)
        img = pygame.image.load(self.content)
        win.blit(img, (self.x + 7, self.y + 7))
