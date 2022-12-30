import pygame
from Spell import Spell

class player(pygame.sprite.Sprite):
    def __init__(self, pos, constraint, speed):
        super().__init__()
        self.image = pygame.image.load('Python/images/player.png').convert_alpha() 
        self.rect = self.image.get_rect(midbottom = pos)
        self.speed = speed
        self.max_x_constraint = constraint
        self.ready = True
        self.spell_time = 0
        self.spell_cooldown = 600


        self.spells = pygame.sprite.Group()

    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        elif keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        
        if keys[pygame.K_SPACE] and self.ready:
            self.shoot_spell()
            self.ready = False
            self.spell_time = pygame.time.get_ticks()

    def recharge(self):
        if not self.ready:
            current_time = pygame.time.get_ticks()
            if current_time - self.spell_time >= self.spell_cooldown:
                self.ready = True

    def constraint(self):
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= self.max_x_constraint:
            self.rect.right = self.max_x_constraint
        
    def shoot_spell(self):
        self.spells.add(Spell(self.rect.center, -8, self.rect.bottom ))
        


    def update(self):
        self.get_input()
        self.constraint()
        self.recharge()
        self.spells.update()