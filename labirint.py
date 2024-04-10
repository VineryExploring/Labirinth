from pygame import *

class GameSprite(sprite.Sprite):

    def __init__(self, picture, w, h, x, y):
        super().__init__()
        self.image = transform.scale(image.load(picture),(w, h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def reset(self):
        window.blit(self.image,(self.rect.x, self.rect.y))

class Player(GameSprite):
    def __init__(self,picture,w,h,x,y, x_speed, y_speed):
        GameSprite.__init__(self, picture,w,h,x,y)
        self.x_speed = x_speed
        self.y_speed = y_speed

    def update(self):
        if player.rect.x <= win_width - 80 and player.x_speed > 0 or player.rect.x >= 0 and player.x_speed < 0 :
            self.rect.x += self.x_speed
        platforms_touched = sprite.spritecollide(self, barriers, False)
        
        if self.x_speed >0:
            for p in platforms_touched:
                self.rect.right = min(self.rect.right, p.rect.left)

        elif self.x_speed <0:
            for p in platforms_touched:
                self.rect.left = max(self.rect.left, p.rect.right)      
        
        if player.rect.y <= win_height - 80 and player.y_speed > 0 or player.rect.y >= 0 and player.y_speed <0:
            self.rect.y += self.y_speed
        platforms_touched = sprite.spritecollide(self, barriers, False)
        
        if self.y_speed >0:
            for p in platforms_touched:
                self.rect.bottom = min(self.rect.bottom, p.rect.top)

        elif self.y_speed <0:
            for p in platforms_touched:
                self.rect.top = max(self.rect.top, p.rect.bottom)

    def fire(self):
        bullet = Bullet("bullet.png", 15, 20, self.rect.right, self.rect.centery, 15)
        bullets.add(bullet)


class Enemy(GameSprite):
    def __init__(self, picture,w,h,x,y, speed):
        GameSprite.__init__(self,picture,w,h,x,y)
        self.speed = speed

    def update(self):
        if self.rect.x <= 470:
            self.direction = "right"

        if self.rect.x >= win_width - 85:
            self.direction = "left"

        if self.direction == "left":
            self.rect.x -= self.speed

        else:
            self.rect.x += self.speed

class Bullet(GameSprite):
    def __init__(self, picture,w,h,x,y, speed):
        GameSprite.__init__(self, picture,w,h,x,y)
        self.speed = speed

    def update(self):
        self.rect.x += self.speed
        if self.rect.x > win_width + 10:
            self.kill()
            

#-----------
x = 0
y = 0

win_height = 500
win_width = 700
#------------

window = display.set_mode((win_width, win_height))
display.set_caption('Лабиринт')

picture = image.load('background.png')
background = transform.scale(picture, (win_width, win_height))
#------------

barriers = sprite.Group()
bullets = sprite.Group()
enemies = sprite.Group()

wall_1 = GameSprite("platform_h.png", 300, 50, 115, 250)
wall_2 = GameSprite("platform_v.png", 300, 50, 230,100)
wall_3 = GameSprite("platform_v.png",50,400,370,100)

barriers.add(wall_1)
barriers.add(wall_2)
barriers.add(wall_3)

final = GameSprite("exit.png",80,80, 600, 400) 
enemy1 = Enemy("enemy.png", 80,80, 615, 250, 5)
enemy2 = Enemy("enemy.png", 80,80, 615, 350, 5)

player = Player('hero.png',80,80,5,400, 0, 0)

enemies.add(enemy1)
enemies.add(enemy2)


run = True
finish = False
while run:
    time.delay(50)

    for e in event.get():
        if e.type == QUIT:
            run = False   

        elif e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                player.rect.x = 5
                player.rect.y = win_height - 80
                finish = False

                enemies.add(enemy1)
                enemies.add(enemy2)
                enemy1.rect.x = 615
                enemy2.rect.x = 615 

                                       
            if e.key == K_UP:
                player.y_speed = -5

            if e.key == K_DOWN:
                player.y_speed = 5

            if e.key == K_RIGHT:
                player.x_speed = 5

            if e.key == K_LEFT:
                player.x_speed = -5

        elif e.type == KEYUP:
            if e.key == K_UP:
                player.y_speed = 0

            if e.key == K_DOWN:
                player.y_speed = 0

            if e.key == K_RIGHT:
                player.x_speed = 0

            if e.key == K_LEFT:
                player.x_speed = 0


            if e.key == K_SPACE:
                player.fire()

    if not finish: 
        
        window.blit(background, (x,y))

        player.update()
        enemies.update()
        bullets.update()

        barriers.draw(window)
        
        final.reset()
        
        enemies.draw(window)
        bullets.draw(window)
        
        player.reset()
        
        sprite.groupcollide(enemies, bullets, True, True)
        sprite.groupcollide(barriers, bullets, False, True)
        if sprite.collide_rect(player, final):
            finish = True
            win = transform.scale(image.load("thumb_1.jpg"), (700,500))

            window.fill((255,255,255))
            window.blit(win,(0,0))

        if sprite.spritecollide(player, enemies, True, False):
            finish = True
            win = transform.scale(image.load("game-over_1.png"), (700,500))

            window.fill((255, 255, 255)) 
            window.blit(win, (0,0))
            
    
    display.update()