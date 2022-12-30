import pygame

#enemies
class enemy(pygame.sprite.Sprite):
    def __init__(self, color, x, y):
        super().__init__()
        file_path = 'Python/images/' + color + '.png'
        self.image = pygame.image.load(file_path).convert_alpha()
        self.rect = self.image.get_rect(topleft =(x, y))

        if color == 'white': self.value = 300
        elif color == 'blue': self.value = 200
        else: self.value = 100

    def update(self, direction):
        self.rect.x += direction

#add in an aextra enemy that floats in the top 
class Extra(pygame.sprite.Sprite):
    def __init__(self, side, screen_width):
        super().__init__()
        self.image = pygame.image.load('Python/images/extra.png').convert_alpha()
        
        if side == 'right':
            x = screen_width + 50
            self.speed = -3
        else:
            x = -50
            self.speed = 3

        self.rect = self.image.get_rect(topleft = (x, 80))
    
    def update(self):
        self.rect.x += self.speed