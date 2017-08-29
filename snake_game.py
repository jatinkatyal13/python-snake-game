class coord(object):
	def __init__(self, x, y):
		self.x = x
		self.y = y
	def __str__(self):
		return "%d - %d" % (self.x, self.y)

def gotoxy(x, y):
	print ("%c[%d;%df" % (0x1B, y, x), end='')

class _Getch:
	def __init__(self):
		import tty, sys
	def __call__(self):
		import sys, tty, termios
		fd = sys.stdin.fileno()
		old_settings = termios.tcgetattr(fd)
		try:
			tty.setraw(sys.stdin.fileno())
			ch = sys.stdin.read(1)
		finally:
			termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
		return ch
getch = _Getch()

snake = [coord(4, 5), coord(4, 6), coord(4, 7)]
height = 20
width = 40
points = 0

def set_food():
	global food
	import random
	c = coord(random.randint(3, width-2), random.randint(3, height-2))
	while any(c.x == temp.x and c.y == temp.y for temp in snake):
		c = coord(random.randint(3, width-2), random.randint(3, height-2))
	food = c

def draw():
	for i in range(0, width+2):
		print('*', end='')
	print('')
	for j in range(0, height):
		print('*', end='')
		for i in range(0, width): print(' ', end='')
		print('*', end='')
		print('')
	for i in range(0, width+2):
		print('*', end='')	

import os
os.system("clear")

draw()
set_food()
while True:
	temp = coord(snake[0].x, snake[0].y)

	if temp.x == food.x and temp.y == food.y:
		set_food()
		points += 1
		snake.append(snake[-1])

	for s in snake:
		gotoxy(s.x, s.y)
		print("@")
	gotoxy(food.x, food.y)
	print("a")
	gotoxy(60,10)
	print("Points: %d" % (points))

	ch = getch()	
	if ch == 'a':
		if not (temp.x < 3 or (snake[1].y == temp.y and temp.x > snake[1].x)):
			temp.x -= 1
	elif ch == 'd':
		if not (temp.x > width or (snake[1].y == temp.y and temp.x < snake[1].x)):
			temp.x += 1
	elif ch == 'w':
		if not (temp.y < 3 or (snake[1].x == temp.x and snake[1].y < temp.y)):
			temp.y -= 1
	elif ch == 's':
		if not (temp.y > height or (snake[1].x == temp.x and snake[1].y > temp.y)):
			temp.y += 1
	elif ch == 'q':
		break
	if not (temp.x == snake[0].x and temp.y == snake[0].y):
		snake = [temp] + snake
		gotoxy(snake[-1].x, snake[-1].y)
		print(' ')
		snake.pop()