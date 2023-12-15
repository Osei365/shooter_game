from pygame import *

her_img = 'rocket.png'
back_img = 'galaxy.jpg'

class GameSprite(sprite.Sprite):

    def __init__(self, img, player_x, player_y, width, height, player_speed):
        sprite.Sprite.__init__(self)

        self.image = transform.scale(image.load(img), (width, height))
        self.speed = player_speed

        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):

    def update(self):
        keys = key.get_pressed()

        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        elif keys[K_RIGHT] and self.rect.x < 600:
            self.rect.x += self.speed
init()
window = display.set_mode((700, 500))
display.set_caption('shooter game')
background = transform.scale(image.load(back_img), (700, 500))

player = Player(her_img, 310, 400, 80, 100, 10)

finish = False

run = True
while run:

    for e in event.get():
        if e.type == QUIT:
            run = False

    if not finish:
        window.blit(background, (0, 0))

        player.update()

        player.reset()

        display.update()

    time.delay(50)