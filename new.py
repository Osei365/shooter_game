#Create your own shooter

from pygame import *
from random import randint


mixer.init()
# mixer.music.load('space.ogg')
# mixer.music.play()

fire_sound = mixer.Sound('fire.ogg')

back_img = 'galaxy.jpg'

score = 0
lost = 0
goal = 40
max_lost = 3
life = 3

class GameSprite(sprite.Sprite):

    def __init__(self, img, x, y, width, height, speed):

        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(img), (width, height))
        self.speed = speed
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        elif keys[K_RIGHT] and self.rect.x < 620:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost

        if self.rect.y > game_height:
            self.rect.x = randint(80, game_width - 80)
            self.rect.y = 0
            lost = lost + 1

class Bullet(GameSprite):

    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

init()
game_width = 700
game_height = 500
window = display.set_mode((game_width, game_height))
display.set_caption('Shooting game')
background = transform.scale(image.load(back_img), (700, 500))

player = Player('rocket.png', 310, 400, 80, 100, 10)
begin_limit = 1
end_limit = 5
enemies = sprite.Group()
for i in range(6):
    enemy = Enemy('ufo.png', randint(80, game_width - 80), -40, 80, 50, randint(begin_limit, end_limit))
    enemies.add(enemy)

asteroids = sprite.Group()
for i in range(3):
    asteroid = Enemy('asteroid.png', randint(30, game_width - 30), -40, 80, 50, randint(begin_limit, end_limit))
    asteroids.add(asteroid)

bullets = sprite.Group()

font.init()

font1 = font.SysFont('Arial', 80)
win = font1.render('WIN!!', True, (255, 255, 255))
lose = font1.render('YOU LOSE!!', True, (180, 0, 0))
font2 = font.SysFont('Arial', 36)
finish = False
run = True
while run:

    for e in event.get():
        if e.type == QUIT:
            run = False

        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                player.fire()

    if not finish:
        window.blit(background, (0, 0))

        
        player.update()
        enemies.update()
        asteroids.update()
        bullets.update()

        player.reset()

        enemies.draw(window)
        bullets.draw(window)
        asteroids.draw(window)

        collides = sprite.groupcollide(enemies, bullets, True, True)
        for c in collides:
            score = score + 1
            enemy = Enemy('ufo.png', randint(80, game_width - 80), -40, 80, 50, randint(begin_limit, end_limit))
            enemies.add(enemy)

        if sprite.spritecollide(player, enemies, False) or sprite.spritecollide(player, asteroids, False):
            sprite.spritecollide(player, enemies, True)
            sprite.spritecollide(player, asteroids, True)
            life = life - 1

        if life == 0 or lost >= max_lost:
            finish = True
            window.blit(lose, (200, 200))

        if score >= goal:
            finish = True
            window.blit(win, (200, 200))

        text_score = font2.render('Score: ' + str(score), 1, (255, 255, 255))
        window.blit(text_score, (10, 20))

        text_loss = font2.render('Missed: ' + str(lost), 1, (255, 255, 255))
        window.blit(text_loss, (10, 50))

        if life == 3:
            life_color = (0, 150, 0)
        if life == 2:
            life_color = (150, 150, 0)
        if life == 1:
            life_color = (150, 0, 0)
        text_life = font1.render(str(life), 1, life_color)
        window.blit(text_life, (650, 10))
        display.update()

    else:
        finish = False
        score = 0
        lost = 0
        life = 3
        for enemy in enemies:
            enemy.kill()
        for bullet in bullets:
            bullet.kill()
        for asteroid in asteroids:
            asteroid.kill()

        time.delay(3000)
        for i in range(6):
            enemy = Enemy('ufo.png', randint(80, game_width - 80), -40, 80, 50, randint(begin_limit, end_limit))
            enemies.add(enemy)
        for i in range(3):
            asteroid = Enemy('asteroid.png', randint(30, game_width - 30), -40, 80, 50, randint(begin_limit, end_limit))
            asteroids.add(asteroid)

        

    time.delay(50)

