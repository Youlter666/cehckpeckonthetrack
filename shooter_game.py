from pygame import *
from random import randint
from time import time as tm 


mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')



img_back = "galaxy.jpg" #фон игры
img_hero = "rocket.png" #герой
img_enemy = "ufo.png"


class GameSprite(sprite.Sprite):
    
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)


        
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
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
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    
    def fire(self):
        bullets.add(Bullet('rocket.png', self.rect.centerx, self.rect.centery, 10, 20, 20))
    
class Enemy(GameSprite):
    def update(self):
        if self.rect.y + self.speed > 500:
            self.rect.y = 10
            count_lose += 1

        else:
            self.rect.y += self.speed

class Bullet(GameSprite):
    def update(self):
        if self.rect.y <0:
            self.kill()
        else:
            self.rect.y -= self.speed

enemy_group = sprite.Group()
for i in range(6):
    enemy_group.add(Enemy('ufo.png', randint(10, 600), 10, 50, 50, 10))

bullets = sprite.Group()
count = 0

win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))


ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)


fontWin = font.Font(None, 60)
fontLose = font.Font(None, 60)

font.init()
font1 = font.Font(None, 33)

font_reload = font.Font(None, 33)
text_reload = font_reload.render('РРРРРР', True, (255, 0, 0))


count = 0 
count_lose = 0 

finish = False

run = True
num_fire = 0
reload_timer = None 
while run:
  
    for e in event.get():
        if e.type == QUIT:
           run = False      
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire > 5:
                    time_now = tm ()
                    if time_now - reload_timer > 2:
                        num_fire = 0

                else:
                    ship.fire()
                    num_fire += 1 
                    if num_fire > 5: 
                        reload_timer = tm()



    if not finish:
        window.blit(background,(0,0))
        collides = sprite.groupcollide(enemy_group, bullets, True, True)
        for m in collides:
            enemy_group.add(Enemy('ufo.png', randint(10, 600), 10, 20, 20, 10))
            count += 1
            if count > 10:
                finish = True
        text1= font1.render(f'Уничтожены: {count}', True, (100, 200, 100))
        text2= font1.render(f'Пропущенны: {count_lose}', True, (100, 200, 100))

        enemy_group.update()
        enemy_group.draw(window)


        bullets.update()
        bullets.draw(window)


        window.blit(text1,(10, 10))
        window.blit(text2,(10, 75))
        
 


        
        ship.update()
        ship.reset()
        if num_fire > 5: 
            window.blit(text_reload, (ship.rect.centerx, ship.rect.centery))
    


    else:
        text_win = fontWin('лаки', True, (0, 255, 0))
        window.blit(text_win, (300, 300))

    display.update()
    enemy_group.update()
    time.delay(50)
