import pygame

class Button():
    def __init__(self, color, x, y, width, height, text = ""):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
    
    def draw(self, win, outline = None):
        if outline:
            pygame.draw.rect(win, outline, (self.x, self.y, self.width, self.height), 2)