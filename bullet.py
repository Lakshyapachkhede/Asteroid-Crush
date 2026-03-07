import pygame
import random

class Bullet:
    def __init__(self, x, y, direction):
        self.image = pygame.image.load(f"./assets/img/bullets/{random.randint(11, 20)}.png").convert_alpha()
        self.image = pygame.transform.smoothscale(self.image,(self.image.get_width() // 5, self.image.get_height() // 5))
        self.rect = pygame.rect.Rect(x, y, self.image.get_width(), self.image.get_height())
        self.direction =  pygame.Vector2(direction).normalize()
        self.angle = pygame.Vector2(1, 0).angle_to(direction)

        self.image = pygame.transform.rotate(self.image, -self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.speed = 800
        self.hitbox = self.rect.inflate(-20, -20)





    def move(self, dt):
        self.rect.centerx += self.direction.x * self.speed * dt
        self.rect.centery += self.direction.y * self.speed * dt




    def draw(self, window):
        window.blit(self.image, self.rect)
    


    def update(self, window, dt):
        self.move(dt)
        self.draw(window)

        

    
        