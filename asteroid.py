import pygame
import random
from settings import *

class Asteroid:
    def __init__(self, player_pos):
        self.image = pygame.image.load(f"./assets/img/asteriods/Asteroid_{random.randint(1, 5)}.png").convert_alpha()
        self.image = pygame.transform.smoothscale(self.image,(self.image.get_width() // 5, self.image.get_height() // 5))
        # self.image = pygame.transform.rotate(self.image, random.randint(0, 360))
        
        self.rect = self.image.get_rect()

        side = random.choice(["top","bottom","left","right"])

        if side == "top":
            self.rect.center = (random.randint(0, WINDOW_WIDTH), -50)
        elif side == "bottom":
            self.rect.center = (random.randint(0, WINDOW_WIDTH), WINDOW_HEIGHT + 50)
        elif side == "left":
            self.rect.center = (-50, random.randint(0, WINDOW_HEIGHT))
        else:
            self.rect.center = (WINDOW_WIDTH + 50, random.randint(0, WINDOW_HEIGHT))

        player_pos = pygame.Vector2(player_pos)
        asteroid_pos = pygame.Vector2(self.rect.center)

        self.direction = (player_pos - asteroid_pos).normalize()
        self.speed = random.randint(100, 200)
        self.hitbox = self.rect.inflate(50, 50)
        self.health = 30

    def move(self, dt):
        self.rect.centerx += self.direction.x * self.speed * dt
        self.rect.centery += self.direction.y * self.speed * dt

    def draw(self, window):
        window.blit(self.image, self.rect)
      


    def update(self, window, dt):
        self.move(dt)
        self.draw(window)

        

    
        