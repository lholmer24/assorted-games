import pygame
from random import randint
#importing nessecary libraries

pygame.init()
win = pygame.display.set_mode((600, 600))
pygame.display.set_caption("Pong")
bg = pygame.image.load('bg.png')
blip = pygame.mixer.Sound("blip.wav")
lowblip = pygame.mixer.Sound("lowblip.wav")
point = pygame.mixer.Sound("point.wav")
#start pygame and set variables

points1 = 0
points2 = 0

class paddle(object):
	def __init__(self, x, y, upkey, downkey):
		self.x = x
		self.y = y
		self.upkey = upkey
		self.downkey = downkey
		self.width = 30
		self.height = 130
		self.vel = 4
		#create the paddle object

	def draw(self, win):
		pygame.draw.rect(win, (255, 255, 255), (self.x, self.y, self.width, self.height,), 0)
		#the function for drawing the paddle object

paddle1 = paddle(10, 235, pygame.K_w, pygame.K_s)
paddle2 = paddle(560, 235, pygame.K_UP, pygame.K_DOWN)
#create the two paddles

class ball(object):
	def __init__(self, x, y, vel):
		self.x = x
		self.y = y 
		self.xvel = vel
		self.yvel = vel
		self.xmult = 1
		self.ymult = 1
		self.size = 30
		#creating a ball class

	def draw(self, win):
		pygame.draw.rect(win, (255, 255, 255), (self.x, self.y, self.size, self.size), 0)
		#drawing the ball class

	def collide(self, paddle1, paddle2):
		if self.x < 0 or self.x > 600 - self.size:
		#detect side collision
			self.x = randint(200, 400)
			self.y = randint(100 , 500)
			paddle1.y = 235
			paddle2.y = 235
			if randint(0, 1):
				self.xmult = self.xmult * -1
			if randint(0, 1):
				self.ymult = self.ymult * -1
			self.xvel = randint(3, 5)
			self.yvel = randint(3, 5)
			point.play()
			pygame.time.delay(500)
			return 1
			#reset and randomise location
		
		if self.y < 0 or self.y + self.size > 600:
			self.ymult = self.ymult * -1
			self.yvel = randint(3, 5)
			lowblip.play()
			if self.y > 300:
					self.y -= 10
			else:
					self.y += 10
		#top/bottom collision

	def paddlecollide(self, paddle):
		if self.x < paddle.x + paddle.width and self.x + self.size > paddle.x:
			if self.y < paddle.y + paddle.height and self.y > paddle.y:
				self.xmult = self.xmult * -1
				self.xvel = randint(3, 5)
				blip.play()
				if self.x > 300:
					self.x -= 10
				else:
					self.x += 10
				#detects collision with the paddles

	def drawscore(self):
		font1 = pygame.font.SysFont('arial', 35)
		text1 = font1.render(f'{points1}', 1, (255, 255, 255))
		win.blit(text1, (200, 10))

		text2 = font1.render(f'{points2}', 1, (255, 255, 255))
		win.blit(text2, (400, 10))

ball1 = ball(300, 200, 4)
#create the ball

def redraw():
	win.blit(bg, (0, 0))
	paddle1.draw(win)
	paddle2.draw(win)
	ball1.draw(win)
	ball1.drawscore()
	pygame.display.update()
	#redraw the items and display them



#this is the mainloop
run = True
paused = False
pauseloop = 0
while run:
	pygame.time.delay(5)
	pauseloop += 1
	#seperate frames

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
	#allows you to close the app

	keys = pygame.key.get_pressed()
	if keys[paddle1.upkey] and paddle1.y > 0:
		paddle1.y -= paddle1.vel
	if keys[paddle1.downkey] and paddle1.y < 600 - paddle1.height:
		paddle1.y += paddle1.vel
	if keys[paddle2.upkey] and paddle2.y > 0:
		paddle2.y -= paddle2.vel
	if keys[paddle2.downkey] and paddle2.y < 600 - paddle2.height:
		paddle2.y += paddle2.vel
	if keys[pygame.K_SPACE] and pauseloop > 10:
		paused = not paused
		pauseloop = 0
	if keys[pygame.K_r]:
		points1 = 0
		points2 = 0
		#check key input and move paddles


	ball1.paddlecollide(paddle1)
	ball1.paddlecollide(paddle2)
	if ball1.x >= 300:
		if ball1.collide(paddle1, paddle2):
			points1 += 1
	elif ball1.x < 300:
		if ball1.collide(paddle1, paddle2):
			points2 += 1
	if not paused:
		ball1.x += ball1.xvel * ball1.xmult
		ball1.y += ball1.yvel * ball1.ymult
	#Check collision and move the ball

	redraw()
	#call the redraw function

pygame.quit()
#end the game when the loop closes