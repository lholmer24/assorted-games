import pygame
import time
from random import randint
#importing nessecary libraries

scale = int(input("Please select your borad size (Under 12 x 12 is recommended): "))
#sets the amount of tiles

pygame.init()
win = pygame.display.set_mode((scale * 60, scale * 60))
pygame.display.set_caption("Minesweeper")
unopened_img = pygame.image.load("unopened.png")
empty_img = pygame.image.load("empty.png")
n1_img = pygame.image.load("1.png")
n2_img = pygame.image.load("2.png")
n3_img = pygame.image.load("3.png")
n4_img = pygame.image.load("4.png")
n5_img = pygame.image.load("5.png")
n6_img = pygame.image.load("6.png")
n7_img = pygame.image.load("7.png")
mine_img = pygame.image.load("mine.png")
flag_img = pygame.image.load("flag.png")
victory_img = pygame.image.load("victory.png")
loss_img = pygame.image.load("loss.png")
#load files and open the window

n_list = [n1_img, n2_img, n3_img, n4_img, n5_img, n6_img, n7_img]
#create an ordered list of the numbers

class square(object):
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.img = unopened_img
		self.mine = False
		self.adjacentmines = 0
		#create the object for each of the tiles

	def draw(self, win):
		win.blit(self.img, (self.x  * 60, self.y * 60))
		#draw the tile

	def flagged(self):
		if self.img == flag_img:
			self.img = unopened_img
		elif self.img == unopened_img:
			self.img = flag_img
		#flag / unflag tiles


	def cascade(self):
		if self.img == empty_img:
			for item2 in squares:
				if item2.x == item.x - 1 and item2.y == item.y - 1:
					if not item2.mine:
						item2.clicked()
				if item2.x == item.x - 1 and item2.y == item.y:
					if not item2.mine:
						item2.clicked()
				if item2.x == item.x - 1 and item2.y == item.y + 1:
					if not item2.mine:
						item2.clicked()
				if item2.x == item.x  and item2.y == item.y - 1:
					if not item2.mine:
						item2.clicked()
				if item2.x == item.x  and item2.y == item.y + 1:
					if not item2.mine:
						item2.clicked()
				if item2.x == item.x + 1 and item2.y == item.y - 1:
					if not item2.mine:
						item2.clicked()
				if item2.x == item.x + 1 and item2.y == item.y:
					if not item2.mine:
						item2.clicked()
				if item2.x == item.x + 1 and item2.y == item.y + 1:
					if not item2.mine:
						item2.clicked()
		#cascade the opening of large empty areas

	def clicked(self):
		if self.img == unopened_img:
			if self.mine:
				self.img = mine_img
			elif self.adjacentmines > 0:
				self.img = n_list[self.adjacentmines - 1]
			else:
				self.img = empty_img
		#appropriately change when clicked


squares = []
for x in list(range(scale)):
	for y in list(range(scale)):
		squares.append(square(x, y))
#create all the tiles


def startgame():
	for item in squares:
		item.mine = False
		item.img = unopened_img
	mines_to_place = scale
	while mines_to_place > 0:
		tempx = randint(0, scale - 1)
		tempy = randint(0, scale - 1)
		for item in squares:
			if item.x == tempx and item.y == tempy and not item.mine:
				item.mine = True
				mines_to_place -= 1
	#randomly place the mines

	for item in squares:
		tempadjmines = 0
		for item2 in squares:
			if item2.x == item.x - 1 and item2.y == item.y - 1 and item2.mine:
				tempadjmines += 1
			if item2.x == item.x - 1 and item2.y == item.y and item2.mine:
				tempadjmines += 1
			if item2.x == item.x - 1 and item2.y == item.y + 1 and item2.mine:
				tempadjmines += 1
			if item2.x == item.x  and item2.y == item.y - 1 and item2.mine:
				tempadjmines += 1
			if item2.x == item.x  and item2.y == item.y + 1 and item2.mine:
				tempadjmines += 1
			if item2.x == item.x + 1 and item2.y == item.y - 1 and item2.mine:
				tempadjmines += 1
			if item2.x == item.x + 1 and item2.y == item.y and item2.mine:
				tempadjmines += 1
			if item2.x == item.x + 1 and item2.y == item.y + 1 and item2.mine:
				tempadjmines += 1
		item.adjacentmines = tempadjmines
	#calculate the number for a tiles

def redraw():
	for item in squares:
		item.draw(win)
	pygame.display.update()
#the redraw function, not nessecary here but good for larger programs

run = True
startgame()
#mainloop
while run:
	pygame.time.delay(5)
	#seperate frames
	for item in squares:
		if item.img == empty_img:
			item.cascade()
		elif item.img == mine_img:
			for item2 in squares:
				item2.img = loss_img
				redraw()	
			pygame.time.delay(5000)
			startgame()
	#initiate cascade or game end yourself


	ev = pygame.event.get()

	for event in ev:
		if event.type == pygame.QUIT:
			run = False
	#close the game appropriately
		if event.type == pygame.MOUSEBUTTONUP:
			pos = pygame.mouse.get_pos()
			for item in squares:
				newrect = pygame.Rect(item.x * 60, item.y * 60, 60, 60)
				if newrect.collidepoint(pos):
					if event.button == 1:
						item.clicked()
					#detect life clicks
					elif event.button == 3:
						item.flagged()
					#detect right clicks
	correct = 0
	for item in squares:
		if item.mine:
			if item.img == flag_img:
				correct += 1
		if not item.mine:
			if item.img != unopened_img:
				correct += 1
	if correct == scale * scale:
		for item in squares:
			item.img = victory_img
			redraw()
		pygame.time.delay(5000)
		startgame()



	redraw()
	#calls the redraw function from earlier

pygame.quit()
#cloase the program if the loop is broken