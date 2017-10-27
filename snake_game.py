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
		global fd
		global old_settings
		fd = sys.stdin.fileno()
		old_settings = termios.tcgetattr(fd)
		try:
			tty.setraw(sys.stdin.fileno())
			ch = sys.stdin.read(1)
		finally:
			termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
		return ch

def end_game():
	global fd
	global old_settings
	global points
	global i
	global m
	import termios
	termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

	import os
	os.system("clear")
	gotoxy(0, 0)
	print("Game Ends ! Final Score is : %d" % (points))

	i.stop()
	m.stop()
	import sys
	sys.exit(0)


getch = _Getch()

snake = [coord(4, 5), coord(4, 6), coord(4, 7)]
height = 20
width = 40
points = 0
ch = 'd'
food = coord(10,10)

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

import time

def move():
	global snake
	global ch
	global points
	global food
	global height
	global width
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
		end_game()
		return 
	if any(temp.x == x.x and temp.y == x.y for x in snake):
		end_game()
		return
	if not (temp.x == snake[0].x and temp.y == snake[0].y):
		snake = [temp] + snake
		gotoxy(snake[-1].x, snake[-1].y)
		print(' ')
		snake.pop()
	time.sleep(0.1)

import threading
c = threading.Condition()

class inp(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.running = True

	def run(self):
		global ch
		while True and self.running:
			temp = getch()
			if temp in ['s', 'w'] and ch in ['s', 'w']:
				continue
			elif temp in ['a', 'd'] and ch in ['a', 'd']:
				continue
			ch = temp

	def stop(self):
		self.running = False
			

class main(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.running = True

	def run(self):
		while True and self.running:
			move()

	def stop(self):
		self.running = False

if __name__ == '__main__':
	import os
	os.system("clear")

	draw()
	set_food()

	global i
	global m
	
	i = inp()
	m = main()

	i.start()
	m.start()

	i.join()
	m.join()