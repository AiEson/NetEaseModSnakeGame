# -*- coding: utf-8 -*-
# 随机模块
import random
from snakeGameScripts import snakeGameFinalValuable
from snakeGameScripts import snakeGameAlgorithm
from snakeGameScripts.snakeClass import SnakeClass
# 获取引擎服务端API的模块
import server.extraServerApi as serverApi
# 获取引擎服务端System的基类，System都要继承于ServerSystem来调用相关函数
ServerSystem = serverApi.GetServerSystemCls()
LevelId = serverApi.GetLevelId()

#modMain中注册的类
class snakeGameServerSystem(ServerSystem):

	# wasd你懂的，这是键值
	W = "87"
	A = "65"
	S = "83"
	D = "68"

	#玩家状态声明，准备和未准备
	ready = True
	notReady = False

	# 相关命令
	playerReady = "准备"
	playerNotReady = "取消准备"
	start = "开始游戏"

	# 引入多人模块
	# 所有加入游戏玩家的字典
	allPlayer = {}
	# 所有准备的玩家的字典
	readyPlayer = {}
	# 玩家状态总阀值
	play = False

	#ServerSystem的初始化函数
	def __init__(self, namespace, systemName):
		super(snakeGameServerSystem, self).__init__(namespace, systemName)
		print("===== Server Listen =====")
		# 房主玩家
		self.playerHost = None
		self.ListenEvent()
		self.tk = 6
		self.tick = 0

	def ListenEvent(self):
		self.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "ServerChatEvent", self, self.OnServerChat)
		self.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "OnScriptTickServer", self, self.OnServerTick)
		self.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "AddServerPlayerEvent", self, self.OnPlayerJoin)
		self.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "DelServerPlayerEvent", self, self.OnPlayerExit)
		self.ListenForEvent(snakeGameFinalValuable.ModName, snakeGameFinalValuable.ClientName, snakeGameFinalValuable.OnKeyPress, self, self.OnKeyPress)

	# 监听玩家退出游戏
	def OnPlayerExit(self, data):
		playerId = data["id"]
		print("玩家加入啦！ID为：" + playerId)
		del self.allPlayer[playerId]

	# 监听玩家加入游戏
	def OnPlayerJoin(self, data):
		playerId = data["id"]
		# 如果所有玩家字典长度为0，则第一个肯定是房主
		if len(self.allPlayer) == 0:
			self.playerHost = playerId
		
		print("玩家加入啦！ID为：" + playerId)
		self.allPlayer[playerId] = self.notReady

	# 重设所有玩家状态
	def resetAllPlayer(self):
		for i in self.allPlayer.keys():
			self.allPlayer[i] = self.notReady

	def OnKeyPress(self, data):
		if self.play:
			key = data["key"]
			playerId = data["id"]
			for playerId2, snakeClass in self.readyPlayer.items():
				print(key)
				if playerId == playerId2:
					if key == self.W and snakeClass.direction != snakeClass.DOWN:
						snakeClass.direction = snakeClass.UP
					elif key == self.A and snakeClass.direction != snakeClass.RIGHT:
						snakeClass.direction = snakeClass.LEFT
					elif key == self.S and snakeClass.direction != snakeClass.UP:
						snakeClass.direction = snakeClass.DOWN
					elif key == self.D and snakeClass.direction != snakeClass.LEFT:
						snakeClass.direction = snakeClass.RIGHT

	def OnServerChat(self, dataa):
		playerId = dataa["playerId"]
		message = dataa["message"]
		if message == self.playerReady:
			if self.allPlayer[playerId] == self.notReady:
				self.allPlayer[playerId] = self.ready
				dt1 = {}
				dt1["message"] = "已准备"
				dt1["id"] = playerId
				snakeGameAlgorithm.sendMessageToPlayer(self, dt1)
			else:
				dt2 = {}
				dt2["message"] = "已准备，请勿重复准备"
				dt2["id"] = playerId
				snakeGameAlgorithm.sendMessageToPlayer(self, dt2)
		if message == self.start:
			if playerId == self.playerHost:
				i = 0
				for playerId, status in self.allPlayer.items():
					if self.allPlayer[playerId] == self.ready:
						i += 1
						data = {}
						data["id"] = playerId
						# 两个有关变量，x对应z轴，y对应y轴
						data["x"] = 1
						data["y"] = 6
						data["z"] = i * 13
						data["self"] = self
						self.play = True
						self.readyPlayer[playerId] = SnakeClass(data)
						snakeGameAlgorithm.addScoreboard(self, playerId)
						snakeGameAlgorithm.addPlayer(self, playerId)
			else:
				dt = {}
				dt["message"] = "您当前不是房主，请通知房主开始游戏"
				dt["id"] = playerId
				snakeGameAlgorithm.sendMessageToPlayer(self, dt)

	def OnServerTick(self):
		if self.play:
			for playerId, snakeClass in self.readyPlayer.items():
				data = {}
				data["id"] = playerId
				data["x"] = snakeClass.z-12
				data["y"] = 10
				data["z"] = 11
				snakeGameAlgorithm.tp(self, data)

				dataa = {}
				dataa["x"] = 0
				dataa["y"] = -90
				dataa["id"] = playerId
				snakeGameAlgorithm.setPlayerRot(self, dataa)

			self.tick += 1
			if self.tick == self.tk:
				self.tick = 0
				for playerId, snakeClass in self.readyPlayer.items():
					dataaa = {}
					dataaa["id"] = playerId
					dataaa["x"] = snakeClass.z
					dataaa["y"] = 5
					dataaa["z"] = 0
					snakeClass.moveSnake()
					snakeGameAlgorithm.GeneratePanel(self, dataaa)
					if snakeClass.snake_is_alive():
						snakeClass.snakeIsEatFood()
						snakeClass.drawSnake()
					else:
						# snakeGameAlgorithm.delScoreboard(self, playerId)
						del self.readyPlayer[playerId]
						if len(self.readyPlayer) == 0:
							self.play = False
							self.resetAllPlayer()
							snakeGameAlgorithm.delScoreboard(self, self.playerHost)
					scoreData = {}
					scoreData["id"] = playerId
					scoreData["score"] = snakeClass.score
					snakeGameAlgorithm.changeScore(self, scoreData)


	def Destroy(self):
		pass
