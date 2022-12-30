from re import X
from tkinter import Y
import pygame, sys
from player import player
import obstacles 
from Enemy import enemy, Extra
from random import choice, randint
from EnemySpell import EnemySpell

class Game:
    def __init__(self):
        #Player setup
        player_sprite = player((screen_width / 2, screen_height), screen_width, 5)
        self.player = pygame.sprite.GroupSingle(player_sprite)

        #health and score setup
        self.lives = 3
        self.lives_surface = pygame.image.load('Python/images/lives.png').convert_alpha()
        self.live_x_start_pos = screen_width - (self.lives_surface.get_size()[0] * 2 + 20)
        self.score = 0 
        self.font = pygame.font.Font('Python/Font/Pixeled.ttf', 20)

        #obstacle setup
        self.shape = obstacles.shape
        self.block_size = 6
        self.blocks = pygame.sprite.Group()
        self.obstacles_amount = 4
        self.obstacles_x_positions = [num * (screen_width / self.obstacles_amount) for num in range(self.obstacles_amount)]
        self.create_multiple_obstacles(*self.obstacles_x_positions, x_start = screen_width / 15, y_start= 490)

        #enemy setup
        self.enemies = pygame.sprite.Group()
        self.enemy_spell = pygame.sprite.Group()
        self.enemy_setup(rows = 6, cols = 8)
        self.enemy_direction = 1

        #extra enemy
        self.extra = pygame.sprite.GroupSingle()
        self.extra_spawn_time = randint(400, 800)
        
    def create_obstacles(self, x_start, y_start, offset_x):
        for row_index, row in enumerate(self.shape):
            for col_index, col in enumerate(row):
                if col =="x":
                    x = x_start + col_index * self.block_size + offset_x
                    y = y_start + row_index * self.block_size
                    block = obstacles.block(self.block_size, (196, 0, 255), x, y)
                    self.blocks.add(block)

    def create_multiple_obstacles(self, *offset, x_start, y_start):
        for offset_x in offset:
            self.create_obstacles(x_start, y_start, offset_x)

    def enemy_setup(self, rows, cols, x_distance = 60, y_distance = 48, x_offset = 70, y_offset = 100):
        for row_index, row in enumerate(range(rows)):
            for col_index, col in enumerate(range(cols)):
                x = col_index * x_distance + x_offset
                y = row_index * y_distance + y_offset

                if row_index == 0: enemy_sprite = enemy('white', x, y)
                elif row_index <= 2: enemy_sprite = enemy('blue', x, y)
                else: enemy_sprite = enemy('green', x, y)
                
                self.enemies.add(enemy_sprite)

    def enemy_position_checker(self):
        all_enemies = self.enemies.sprites()
        for enemy in all_enemies:
            if enemy.rect.right >= screen_width:
                 self.enemy_direction = -1
                 self.enemy_move_down(2)
            elif enemy.rect.left <= 0:
                self.enemy_direction = 1
                self.enemy_move_down(2)

    def enemy_move_down(self, distance):
        if self.enemies:
            for enemy in self.enemies.sprites():
                enemy.rect.y += distance

    def enemy_shoots(self):
        if self.enemies.sprites():
            random_enemy = choice(self.enemies.sprites())
            spell_sprite = EnemySpell(random_enemy.rect.center, 6, screen_height)
            self.enemy_spell.add(spell_sprite)

    def extra_alien_timer(self):
        self.extra_spawn_time -= 1
        if self.extra_spawn_time <= 0:
            self.extra.add(Extra(choice(['right', 'left']), screen_width))
            self.extra_spawn_time = randint(400, 800)

    def collision_checks(self):
        #player spells
        if self.player.sprite.spells:
            for Spell in self.player.sprite.spells:
                #obstacle collisions
                if pygame.sprite.spritecollide(Spell, self.blocks, True):
                   #kill stops the spell from running straight through the object
                    Spell.kill()

                #enemy collisions
                enemies_hit = pygame.sprite.spritecollide(Spell, self.enemies, True)
                if enemies_hit:
                    for enemy in enemies_hit:
                        self.score += enemy.value
                    Spell.kill()
                
                #extra collision
                if pygame.sprite.spritecollide(Spell, self.extra, True):
                    self.score += 500
                    Spell.kill()
                    
        
        #Enemy spells
        if self.enemy_spell:
            for enemy_spells in self.enemy_spell:
                #obstacle collision
                if pygame.sprite.spritecollide(enemy_spells, self.blocks, True):
                    enemy_spells.kill()
                
                #player collision
                if pygame.sprite.spritecollide(enemy_spells, self.player, False):
                    enemy_spells.kill()
                    self.lives -= 1
                    if self.lives <= 0:
                        pygame.quit()
                        sys.exit()

        #Enemies
        if self.enemies:
            for enemy in self.enemies:
                pygame.sprite.spritecollide(enemy, self.blocks, True)

                if pygame.sprite.spritecollide(enemy, self.player, False):
                    pygame.quit()
                    sys.exit()       

    def display_lives(self):
        #shows when you lose lives
        for live in range(self.lives - 1):
            x = self.live_x_start_pos + (live * (self.lives_surface.get_size()[0] + 10))
            screen.blit(self.lives_surface, (x, 8))

    def display_score(self):
        score_surface = self.font.render(f'score: {self.score}', False, 'white')
        score_rect = score_surface.get_rect(topleft = (10,-10))
        screen.blit(score_surface, score_rect)

    def run(self):
        self.player.update()
        self.enemies.update(self.enemy_direction)
        self.enemy_position_checker()
        self.enemy_spell.update()
        self.extra_alien_timer()
        self.extra.update()
        self.collision_checks()

        self.player.sprite.spells.draw(screen)
        self.player.draw(screen)
        self.blocks.draw(screen)
        self.enemies.draw(screen)
        self.enemy_spell.draw(screen)
        self.extra.draw(screen)
        self.display_lives()
        self.display_score()
   

if __name__ == '__main__':
    pygame.init()
    screen_width = 600
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_width))
    clock = pygame.time.Clock()
    game = Game()

#timer to prevent enemy_shoots from shoot all the time
    ENEMYSPELL = pygame.USEREVENT + 1
    pygame.time.set_timer(ENEMYSPELL, 800)


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
             pygame.quit()
             sys.exit()
            if event.type == ENEMYSPELL:
                game.enemy_shoots()

        screen.fill((241,145,155))
        #game logic
        game.run()

        pygame.display.flip()
        clock.tick(60)