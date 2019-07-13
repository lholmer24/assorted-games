import pygame
import random
import math
#import nessecary libraries

pygame.init()
#start pygame

win = pygame.display.set_mode((600, 600))

pygame.display.set_caption("Zoom Zoom")

carpic = pygame.image.load('car.png')
bg = pygame.image.load('bg.png')
rockpic = pygame.image.load('rock2.png')
treepic = pygame.image.load('tree.png')
coinpic = pygame.image.load('coin.png')
music = pygame.mixer.music.load("music.mp3")
bulletSound = pygame.mixer.Sound("launch.wav")
hitSound = pygame.mixer.Sound("hit.wav")
#all these take assets and set up the window
pygame.mixer.music.play(-1) # -1 will ensure the song keeps looping

speed = -2
points = 0
highscore = 0
bullets = []
rocks = []
trees = []
coins = []
#create nessecary lists

class player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 3
        self.hitbox = (self.x, self.y + 32, 128, 64)
        #init for player class

    def draw(self, win):
        win.blit(carpic, (car.x, car.y))
        self.hitbox = (self.x, self.y + 32, 128, 64)
        #the draw function

    def hit(self):
        global points
        global bullets
        global rocks
        global trees
        global coins
        global speed
        bullets = []
        rocks = []
        trees = []
        coins = []
        speed = -2
        #very messy hit function

        self.x = 2 # We are resetting the player position
        self.y = 236
        i = 0
        points = 0
        while i < 300:
            pygame.time.delay(10)
            i += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    i = 301
                    pygame.quit()

    def drawscore(self):
        font1 = pygame.font.SysFont('arial', 35)
        text = font1.render(f'Score = {points}', 1, (0,0,0))
        win.blit(text, (10 ,25))

        text2 = font1.render(f'Highscore = {highscore}', 1, (0,0,0))
        win.blit(text2, (310 ,25))
        #this bit prints the score, i dont know why in the player

class projectile(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vel = 8
        #very simple projectiles from the car

    def draw(self, win):
        pygame.draw.circle(win, (250, 10, 10), (self.x, self.y), 10)

class nonbreakob(object):
    def __init__(self, x, width, height, startpos, speed):
        self.x = x
        self.startpos = startpos
        self.y = (self.startpos * 150) + 20
        self.width = width
        self.height = height
        self.vel = speed
        self.hitbox = (self.x, self.y + 5, 160, 120)
        #the rocks class

    def draw(self, win):
        win.blit(rockpic, (self.x, self.y))
        self.hitbox = (self.x, self.y + 5, 170, 120)
        #the draw function for the rock


class breakob(object):
    def __init__(self, x, width, height, startpos, currentTree, speed):
        self.x = x
        self.startpos = startpos
        self.y = (self.startpos * 150) + 20
        self.width = width
        self.height = height
        self.vel = speed
        self.hitbox = (self.x, self.y + 5, 105, 120)
        self.treeindex = currentTree
        #the tree class

    def draw(self, win):
        win.blit(treepic, (self.x, self.y))
        self.hitbox = (self.x, self.y + 5, 105, 120)
        #the draw function

    def hit(self):
        global points
        points += 1000
        hitSound.play()
        storeIndex = self.treeindex
        trees.pop(self.treeindex)
        for tree in trees:
            if tree.treeindex > storeIndex:
                tree.treeindex -= 1
        # the bullets hitting the trees


class roadcoin(object):
    def __init__(self, x, width, height, startpos, currentCoin, speed):
        self.startpos = startpos
        self.x = x
        self.y = (self.startpos * 150) + 20
        self.width = width
        self.height = height
        self.vel = speed
        self.hitbox = (self.x, self.y + 5, 105, 120)
        self.coinindex = currentCoin
        #this makes the coins, names are weird for specification reasons

    def draw(self, win):
        win.blit(coinpic, (self.x, self.y))
        self.hitbox = (self.x, self.y + 5, 105, 120)
        #the draw function

    def hit(self):
        global points
        points += 1000
        storeIndex = self.coinindex
        coins.pop(self.coinindex)
        for coin in coins:
            if coin.coinindex > storeIndex:
                coin.coinindex -= 1
        #this is a seperate hit function for the coins rather than the other obs


car = player(236, 236, 128, 128)

run = True
itemWaitCycle = 200
shootLoop = 0
musicLoop = 0
#setting more variables

def redraw():
    win.blit(bg, (0, 0))
    car.draw(win)
    for rock in rocks:
        rock.draw(win)
    for bullet in bullets:
        bullet.draw(win)
    for tree in trees:
        tree.draw(win)
    for coin in coins:
        coin.draw(win)
    car.drawscore()
    pygame.display.update()
    # this function draws everything



def spawncycle():
    spotlist = [0, 1, 2, 3]
    currentTree = 0
    currentCoin = 0
    #setting some drawing nessecary variables

    for spot in list(range(random.randint(1, 3))):
        pickspot = random.choice(spotlist)

        rocks.append(nonbreakob(600, 128, 128, pickspot, speed))
        spotlist.pop(spotlist.index(pickspot))
        #the rock drawing


    for spot in spotlist:
        if random.randint(0, 1) == 1:
            pickspot = spot

            trees.append(breakob(600, 128, 128, pickspot, currentTree, speed))
            spotlist.pop(spotlist.index(pickspot))
            currentTree += 1
            #the tree spawing

    for spot in spotlist:
        pickspot = spot
        coins.append(roadcoin(600, 128, 128, pickspot,currentCoin, speed))
        currentCoin += 1
        #coin spawing



#mainloop
while run:
    pygame.time.delay(5)
    #seperating frames

    for x in rocks:
        if car.hitbox[1] < x.hitbox[1] + x.hitbox[3] and car.hitbox[1] + car.hitbox[3] > x.hitbox[1]:
            if car.hitbox[0] + car.hitbox[2] > x.hitbox[0] and car.hitbox[0] < x.hitbox[0] + x.hitbox[2]:
                car.hit()
    #rock hit detection
    for x in trees:
        if car.hitbox[1] < x.hitbox[1] + x.hitbox[3] and car.hitbox[1] + car.hitbox[3] > x.hitbox[1]:
            if car.hitbox[0] + car.hitbox[2] > x.hitbox[0] and car.hitbox[0] < x.hitbox[0] + x.hitbox[2]:
                car.hit()
    #tree hit detection
    for coin in coins:
        if car.hitbox[1] < coin.hitbox[1] + coin.hitbox[3] and car.hitbox[1] + car.hitbox[3] > coin.hitbox[1]:
            if car.hitbox[0] + car.hitbox[2] > coin.hitbox[0] and car.hitbox[0] < coin.hitbox[0] + coin.hitbox[2]:
                coin.hit()
    #coin hit detection

    points += 1
    #point incrementation

    if points > 10000:
        speed = math.floor(points * -0.0001) - 1
        print(speed)




    if points >= highscore:
        highscore = points


    if shootLoop > 0:
        shootLoop += 1
    if shootLoop > 80:
        shootLoop = 0
    #stopping shot spam

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    #checking if you close the window

    for bullet in bullets:
        for tree in trees:
            if bullet.y - 5 < tree.hitbox[1] + tree.hitbox[3] and bullet.y + 5 > tree.hitbox[1]:
                if bullet.x + 5 > tree.hitbox[0] and bullet.x - 5 < tree.hitbox[0] + tree.hitbox[2]:
                    tree.hit()
                    bullets.pop(bullets.index(bullet))
    #bullet x tree hit detection

        if bullet.x < 500 and bullet.x > 0:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))
        #deleting bullets when the miss

    for rock in rocks:
        if rock.x > -200:
            rock.x += rock.vel
        else:
            rocks.pop(rocks.index(rock))
    #destroying rocks

    for tree in trees:
        if tree.x > -200:
            tree.x += tree.vel
        else:
            trees.pop(trees.index(tree))
    #destroying trees

    for coin in coins:
        if coin.x > -200:
            coin.x += coin.vel
        else:
            coins.pop(coins.index(coin))
    #destroying coins


    keys = pygame.key.get_pressed()

    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        if car.x >= 0:
            car.x -= car.vel
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        if car.x <= 470:
            car.x += car.vel
    if keys[pygame.K_w] or keys[pygame.K_UP] :
        if car.y >= -30:
            car.y -= car.vel
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        if car.y <= 502:
            car.y += car.vel
    #key presses
    if keys[pygame.K_SPACE] and shootLoop == 0:
        bullets.append(projectile(round(car.x + 128), round(car.y + 64)))
        bulletSound.play()
        shootLoop = 1
    #bullet detection

    if itemWaitCycle < 300:
        itemWaitCycle += 1
    else:
        if len(rocks) == 0 and len(trees) == 0:
            if callable(nonbreakob) and callable(breakob):
                spawncycle()
                itemWaitCycle = 0
    #spawning all the items

    redraw()
    #drawing everything

pygame.quit()
