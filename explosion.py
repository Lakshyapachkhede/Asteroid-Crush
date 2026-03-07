import pygame

class Explosion:

    def __init__(self, pos, frames):
        self.frames = frames
        self.frame_index = 0
        self.image = self.frames[self.frame_index]

        self.rect = self.image.get_rect(center=pos)

        self.timer = 0
        self.animation_speed = 15
        self.finished = False

    def update(self, dt):

        self.timer += self.animation_speed * dt

        if self.timer >= 1:
            self.timer = 0
            self.frame_index += 1

            if self.frame_index >= len(self.frames):
                self.finished = True
            else:
                self.image = self.frames[self.frame_index]

    def draw(self, window):
        window.blit(self.image, self.rect)