import pygame
from player import Player
from settings import *
from asteroid import Asteroid
import random
from explosion import Explosion

class Game:
    def __init__(self):
        icon = pygame.image.load("icon.ico")
        pygame.display.set_icon(icon)
        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(GAME_NAME)
        self.player = Player(0)
        self.asteroids = []
        self.run = False
        self.clock = pygame.time.Clock()
        self.bg_img = pygame.transform.scale(pygame.image.load("./assets/img/bg.png").convert_alpha(), (WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.mouse.set_visible(False)
        self.state = GAME_STATE_MENU

        # score

        self.font = pygame.font.Font("./assets/font/font.otf", 32)

        self.score = 0
        self.asteroids_destroyed = 0
        self.survival_time = 0

        # sounds
        pygame.mixer.init()

        self.explosion_sound = pygame.mixer.Sound("./assets/sound/explosion.ogg")

        pygame.mixer.music.load("./assets/sound/bg.mp3")
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play(-1) 

        #explosion animation
        self.explosion_frames = []

        sheet = pygame.image.load("./assets/img/explosion.png").convert_alpha()

        frame_w = 32
        frame_h = 32

        for i in range(8):
            frame = sheet.subsurface((i * frame_w, 0, frame_w, frame_h))
            frame = pygame.transform.scale(frame, (80, 80)) 

            self.explosion_frames.append(frame)

        self.explosions = []

        self.ships_img = [] # for menu only
        self.ship_rects = []

        for i in range(0, 13):
            img = pygame.image.load(f"./assets/img/ships/Spaceship_{i}.png").convert_alpha()
            img = pygame.transform.smoothscale(img ,(img.get_width() // 5, img.get_height() // 5))
            self.ships_img.append(img)

        self.selected_ship = -1

        self.high_score = self.load_high_score()
        self.new_high_score = False

    def load_high_score(self):
        try:
            with open("highscore.txt", "r") as f:
                return int(f.read())
        except:
            return 0
        
    def save_high_score(self):
        with open("highscore.txt", "w") as f:
            f.write(str(self.high_score))

    def reset_game(self):

        # reset player
        self.player = Player(self.selected_ship)

        # clear entities
        self.asteroids.clear()
        self.explosions.clear()

        # reset score values
        self.score = 0
        self.asteroids_destroyed = 0
        self.survival_time = 0

        # restart gameplay
        self.state = GAME_STATE_LOOP
        self.new_high_score = False


    def loop(self):
        self.run = True

        while self.run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.run = False

                    elif event.key == pygame.K_RETURN and self.state == GAME_STATE_OVER:
                        self.reset_game()


                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.state == GAME_STATE_MENU:
                    
                    mouse_pos = pygame.mouse.get_pos()

                    for i, rect in enumerate(self.ship_rects):

                        if rect.collidepoint(mouse_pos):

                            self.player = Player(i)
                            self.selected_ship = i
                            self.state = GAME_STATE_LOOP

            dt = self.clock.tick(60) / 1000 



            if self.state == GAME_STATE_MENU:

                self.window.blit(self.bg_img, (0,0))
            
                heading_text = self.font.render(GAME_NAME, True, (255,255,255))

                self.window.blit(heading_text, (WINDOW_WIDTH // 2 - heading_text.get_width() //2, 60))

                developer_text = self.font.render(DEVELOPER, True, (255,255,255))

                self.window.blit(developer_text, (WINDOW_WIDTH - developer_text.get_width() - 20, WINDOW_HEIGHT - developer_text.get_height() - 20))

                self.ship_rects.clear()

                cols = 5
                spacing = 20

                start_x = (WINDOW_WIDTH - (cols * CELL_W + (cols-1)*spacing)) // 2
                start_y = 200

                for i, img in enumerate(self.ships_img):

                    row = i // cols
                    col = i % cols

                    cell_x = start_x + col * (CELL_W + spacing)
                    cell_y = start_y + row * (CELL_H + spacing)

                    cell_rect = pygame.Rect(cell_x, cell_y, CELL_W, CELL_H)

                    # center the ship inside the cell
                    img_rect = img.get_rect(center=cell_rect.center)

                    self.window.blit(img, img_rect)

                    # store clickable rect (cell area, not image)
                    self.ship_rects.append(cell_rect)

                    mouse_pos = pygame.mouse.get_pos()

                    pygame.draw.circle(self.window, (255, 0, 0), mouse_pos, 10, 4)

                    if cell_rect.collidepoint(mouse_pos):
                        pygame.draw.rect(self.window, (255,255,255), cell_rect, 2)




            if (self.state == GAME_STATE_LOOP):

                self.window.blit(self.bg_img, (0,0))

                self.survival_time += dt
                self.score = int(self.survival_time) + self.asteroids_destroyed * 10

            
                if random.random() < 0.03:   
                    self.asteroids.append(Asteroid(self.player.rect.center))



                for asteroid in self.asteroids[:]:
                    if(asteroid.rect.right < -100 or asteroid.rect.left > WINDOW_WIDTH + 100  or asteroid.rect.top > WINDOW_HEIGHT + 100 or asteroid.rect.bottom < -100):
                        self.asteroids.remove(asteroid)
                        continue
                    asteroid.update(self.window, dt)

                self.player.update(self.window, dt)


                for explosion in self.explosions[:]:

                    explosion.update(dt)
                    explosion.draw(self.window)

                    if explosion.finished:
                        self.explosions.remove(explosion)

                self.check_collision()
                self.draw_hud()

            if (self.state == GAME_STATE_OVER):

                over_text = self.font.render("GAME OVER", True, (255,0,0))
                restart_text = self.font.render("Press ENTER to Restart", True, (255,255,255))

                self.window.blit(over_text,
                    (WINDOW_WIDTH//2 - over_text.get_width()//2,
                    WINDOW_HEIGHT//2 - 40))

                self.window.blit(restart_text,
                    (WINDOW_WIDTH//2 - restart_text.get_width()//2,
                    WINDOW_HEIGHT//2 + 10))
                
                developer_text = self.font.render(DEVELOPER, True, (255,255,255))

                self.window.blit(developer_text, (WINDOW_WIDTH - developer_text.get_width() - 20, WINDOW_HEIGHT - developer_text.get_height() - 20))

                if(self.new_high_score):
                    new_high_score_text = self.font.render("NEW HIGH SCORE", True, (255,255,0))
                    self.window.blit(new_high_score_text, (WINDOW_WIDTH//2 - new_high_score_text.get_width()//2, WINDOW_HEIGHT // 2 + 60))


            pygame.display.flip()

    def draw_hud(self):
        score_text = self.font.render(f"Score: {self.score}", True, (255,255,255))
        kills_text = self.font.render(f"Asteroids: {self.asteroids_destroyed}", True, (255,255,255))
        time_text = self.font.render(f"Time: {int(self.survival_time)}", True, (255,255,255))

        if(self.player.health <= 40):
            health_text_color = (255,0,0)
        else:
            health_text_color = (255,255,255)

            
        health_text = self.font.render(f"Health: {int(self.player.health)}", True, health_text_color)

        self.window.blit(score_text, (20,20))
        self.window.blit(kills_text, (20,60))
        self.window.blit(time_text, (WINDOW_WIDTH - time_text.get_width() - 20, 20))
        self.window.blit(health_text, (WINDOW_WIDTH - health_text.get_width() - 20, 60))

    def check_collision(self):



        for i, asteroid in enumerate(self.asteroids):
            for a in self.asteroids[i+1:]:

                asteroid1_hitbox = asteroid.rect.inflate(-30, -30)
                asteroid2_hitbox = a.rect.inflate(-30, -30)

                if asteroid1_hitbox.colliderect(asteroid2_hitbox):
                
                    asteroid.direction = -asteroid.direction
                    a.direction = -a.direction

                
        for asteroid in self.asteroids[:]:
            for bullet in self.player.bullets[:]:

                asteroid_hitbox = asteroid.rect.inflate(-30, -30)
                bullet_hitbox = bullet.rect.inflate(-10, -10)

                if asteroid_hitbox.colliderect(bullet_hitbox):
                    asteroid.health -= 15
                    self.player.bullets.remove(bullet)

                    if(asteroid.health <= 0):
                        self.explosion_sound.play()
                        self.asteroids_destroyed += 1
                        self.explosions.append(Explosion(asteroid.rect.center, self.explosion_frames))
                        self.asteroids.remove(asteroid)
                        break


 

            for asteroid in self.asteroids[:]:
                asteroid_hitbox = asteroid.rect.inflate(-30, -30)
                player_hitbox = self.player.rect.inflate(-30, -30)

                if asteroid_hitbox.colliderect(player_hitbox):
                    time_now = pygame.time.get_ticks()
                    if time_now - self.player.last_hit_time > self.player.hit_cooldown:

                        self.player.last_hit_time = time_now
                        self.player.health -= random.randint(10, 20)
                        
                        player_pos = pygame.Vector2(self.player.rect.center)

                        asteroid_pos = pygame.Vector2(asteroid.rect.center)

                        knock_dir = (player_pos - asteroid_pos).normalize()

                        self.player.rect.centerx += knock_dir.x * 40
                        self.player.rect.centery += knock_dir.y * 40

                        if self.player.health <= 0:
                            self.player.health = 0

                            if self.score > self.high_score:
                                self.high_score = self.score
                                self.save_high_score()
                                self.new_high_score = True

                            self.state = GAME_STATE_OVER
