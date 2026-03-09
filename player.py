import pygame
import random
from bullet import Bullet
from settings import *

class Player:    
    def __init__(self, ship_no):
        self.image = pygame.image.load(f"./assets/img/ships/Spaceship_{ship_no}.png").convert_alpha()
        self.original_image = pygame.transform.smoothscale(self.image,(self.image.get_width() // 5, self.image.get_height() // 5))
        self.aim_image = pygame.transform.smoothscale(pygame.image.load(f"./assets/img/aim.png").convert_alpha(), (64, 64))
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.rect.centerx = WINDOW_WIDTH // 2
        self.rect.centery = WINDOW_HEIGHT // 2
        self.direction = pygame.Vector2(0, 0)
        self.speed = 200
        self.angle = 0.0
       

        self.bullet_last_time = 0
        self.shot_gap_time = 100
        self.bullets = []

        self.health = 100

        self.last_hit_time = 0
        self.hit_cooldown = 1000   
        



    def input(self):
        keys = pygame.key.get_pressed()
        self.direction.x = (keys[pygame.K_d] or keys[pygame.K_RIGHT]) - (keys[pygame.K_a] or keys[pygame.K_LEFT])
        self.direction.y = (keys[pygame.K_s] or keys[pygame.K_DOWN]) - (keys[pygame.K_w] or keys[pygame.K_UP])
        if self.direction.length() > 0:
            self.direction = self.direction.normalize()

        mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
        player_pos = pygame.Vector2(self.rect.center)

        direction = mouse_pos - player_pos
        self.angle = pygame.Vector2(0, -1).angle_to(direction)

        self.image = pygame.transform.rotate(self.original_image, -self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

        mouse_keys = pygame.mouse.get_pressed()
        time_now = pygame.time.get_ticks()

        if(mouse_keys[0] and ( time_now - self.bullet_last_time ) > self.shot_gap_time):
            self.bullet_last_time = time_now
            self.bullets.append(Bullet(self.rect.centerx, self.rect.centery, direction))



    def move(self, dt):
        self.rect.centerx += self.direction.x * self.speed * dt
        self.rect.centery += self.direction.y * self.speed * dt

        self.rect.centerx = max(0, min(WINDOW_WIDTH, self.rect.centerx))
        self.rect.centery = max(0, min(WINDOW_HEIGHT, self.rect.centery))

    def draw(self, window):
        time_now = pygame.time.get_ticks()

        if time_now - self.last_hit_time < self.hit_cooldown:
            if (time_now // 100) % 2 == 0:
                return

        window.blit(self.image, self.rect)

        mouse_pos = pygame.mouse.get_pos()
        aim_rect = self.aim_image.get_rect(center=mouse_pos)

        window.blit(self.aim_image, aim_rect)


        




    def update(self, window, dt):
        for b in self.bullets[:]:
            if(b.rect.x > WINDOW_WIDTH or b.rect.x < 0 or b.rect.y > WINDOW_HEIGHT or b.rect.y < 0):
                self.bullets.remove(b)
                continue
            b.update(window, dt)

        self.input()
        self.move(dt)
        self.draw(window)
