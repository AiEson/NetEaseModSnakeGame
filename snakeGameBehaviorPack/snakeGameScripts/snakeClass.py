# -*- coding: utf-8 -*-
# 随机模块
import random
from snakeGameScripts import snakeGameAlgorithm

# Type: Server
class SnakeClass(object):

	# 变量初始化
	# xy是坐标系的原点坐标
	x = 0
	y = 0
	# z是无关变量，因为MC是三维，所以舍弃一个坐标不用，这里的z对应的是MC里的X轴
	z = 0
	HEAD = 0
	RIGHT = 0
	LEFT = 1
	UP = 3
	DOWN = 4
	snakeLength = 3
	score = 3
	direction = RIGHT
	map_width = 20
	map_height = 12
	snake_coords = None
	food = {}
	serverSelf = None
	playerId = None
	playerName = None

	#类的初始化函数
	def __init__(self, data):
		self.x = data["x"]
		self.y = data["y"]
		self.z = data["z"]
		self.serverSelf = data["self"]
		self.playerId = data["id"]
		self.playerName = snakeGameAlgorithm.getPlayerNameById(self.serverSelf, self.playerId)
		startx = random.randint(3, self.map_width - 8) + self.x
		starty = random.randint(2, self.map_height - 2) + self.y
		self.snake_coords = [{'x': startx, 'y': starty},{'x': startx - 1, 'y': starty},{'x': startx - 2, 'y': starty}]
		self.food['x'] = random.randint(0, self.map_width - 1) + self.x
		self.food['y'] = random.randint(0, self.map_height - 1) + self.y

	def snake_is_alive(self):
		tag = True
		if self.snake_coords[self.HEAD]['x'] == -1 + self.x or self.snake_coords[self.HEAD]['x'] == self.map_width + self.x + 1 or self.snake_coords[self.HEAD]['y'] == -1 + self.y or self.snake_coords[self.HEAD]['y'] == self.map_height + self.y:
			tag = False  # 蛇碰壁啦
		for snake_body in self.snake_coords[1:]:
			if snake_body['x'] == self.snake_coords[self.HEAD]['x'] and snake_body['y'] == self.snake_coords[self.HEAD]['y']:
				tag = False  # 蛇碰到自己身体啦
		return tag

	# 先move再draw
	def drawSnake(self):
		data = {}
		data["x"] = self.z
		data["y"] = self.food['y']
		data["z"] = self.food['x']
		data["id"] = 35
		data["aux"] = 1
		data["playerId"] = self.playerId
		snakeGameAlgorithm.setBlock(self.serverSelf, data)
		for coord in self.snake_coords:
			z = coord['x']
			y = coord['y']
			x = self.z
			data = {}
			data["x"] = x
			data["y"] = y
			data["z"] = z
			data["id"] = 35
			data["aux"] = 12
			data["playerId"] = self.playerId
			snakeGameAlgorithm.setBlock(self.serverSelf, data)

	def moveSnake(self):
		if self.direction == self.UP:
			newHead = {'x': self.snake_coords[self.HEAD]['x'], 'y': self.snake_coords[self.HEAD]['y'] + 1}
		elif self.direction == self.DOWN:
			newHead = {'x': self.snake_coords[self.HEAD]['x'], 'y': self.snake_coords[self.HEAD]['y'] - 1}
		elif self.direction == self.LEFT:
			newHead = {'x': self.snake_coords[self.HEAD]['x'] - 1, 'y': self.snake_coords[self.HEAD]['y']}
		elif self.direction == self.RIGHT:
			newHead = {'x': self.snake_coords[self.HEAD]['x'] + 1, 'y': self.snake_coords[self.HEAD]['y']}
		# 插入蛇身数据
		self.snake_coords.insert(0, newHead)


	def snakeIsEatFood(self):
		if self.snake_coords[self.HEAD]['x'] == self.food['x'] and self.snake_coords[self.HEAD]['y'] == self.food['y']:
			randx = random.randint(0, self.map_width - 1) + self.x
			randy = random.randint(0, self.map_height - 1) + self.y
			self.food['x'] = randx
			self.food['y'] = randy
			self.score += 1
		else:
			del self.snake_coords[-1] # 如果没有吃到实物, 就向前移动, 那么尾部一格删掉