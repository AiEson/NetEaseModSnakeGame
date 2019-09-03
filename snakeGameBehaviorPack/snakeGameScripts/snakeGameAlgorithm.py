# -*- coding: utf-8 -*-


# Type:Server
# 生成游戏盘需要放在蛇身移动之后
# 循环方法比较笨重，可以使用指令fill填充，指令用法详见下面tp
def GeneratePanel(self, data):
	playerId = data["id"]
	x = data["x"]
	y = data["y"]
	z = data["z"]
	for i in range(13):
		data = {}
		data["x"] = x
		data["y"] = y + i
		data["z"] = z
		data["id"] = 35
		data["aux"] = 15
		data["playerId"] = playerId
		setBlock(self, data)
	for i in range(13):
		data = {}
		data["x"] = x
		data["y"] = y+i
		data["z"] = z + 22
		data["id"] = 35
		data["aux"] = 15
		data["playerId"] = playerId
		setBlock(self, data)
	for i in range(23):
		data = {}
		data["x"] = x
		data["y"] = y
		data["z"] = z + i
		data["id"] = 35
		data["aux"] = 15
		data["playerId"] = playerId
		setBlock(self, data)
	for i in range(23):
		data = {}
		data["x"] = x
		data["y"] = y + 13
		data["z"] = z + i
		data["id"] = 35
		data["aux"] = 15
		data["playerId"] = playerId
		setBlock(self, data)
	for i in range(12):
		for j in range(21):
			data = {}
			data["x"] = x
			data["y"] = y + i + 1
			data["z"] = z + j + 1
			data["id"] = 35
			data["aux"] = 0
			data["playerId"] = playerId
			setBlock(self, data)
# Type:Server
def getPlayerNameById(self, playerId):
	comp = self.CreateComponent(playerId, "Minecraft", "name")
	return str(comp.name)

# Type:Server or Client
# xy分别为（上下角度，左右角度）单位是角度而不是弧度
def setPlayerRot(self, data):
	x = data["x"]
	y = data["y"]
	playerId = data["id"]
	comp = self.CreateComponent(playerId, "Minecraft", "rot")
	comp.rot = (x,y)
	self.NeedsUpdate(comp)

# Type:Server
# 向某玩家聊天框发送信息
def sendMessageToPlayer(self, data):
	message = data["message"]
	playerId = data["id"]
	comp = self.CreateComponent(playerId, "Minecraft", "msg")
	comp.msg = message
	self.NeedsUpdate(comp)

# Type:Server
def tp(self, data):
	playerId = data["id"]
	x = data["x"]
	y = data["y"]
	z = data["z"]
	if playerId != None:
		commandComp = self.CreateComponent(playerId, "Minecraft", "command")
		commandComp.command = ("/tp \"" + getPlayerNameById(self, playerId) + "\" " + str(x) + " " + str(y) + " " + str(z))
		self.NeedsUpdate(commandComp)

# 删除计分板
def delScoreboard(self, playerId):
	if playerId != None:
		commandComp = self.CreateComponent(playerId, "Minecraft", "command")
		commandComp.command = ("/scoreboard objectives remove jfb")
		self.NeedsUpdate(commandComp)

# Type:Server
# 添加计分板
def addScoreboard(self, playerId):
	if playerId != None:
		commandComp = self.CreateComponent(playerId, "Minecraft", "command")
		# 添加id为jfb的计分板
		commandComp.command = ("/scoreboard objectives add jfb dummy §6分数")
		self.NeedsUpdate(commandComp)
		# 显示计分板
		commandComp.command = ("/scoreboard objectives setdisplay sidebar jfb")
		self.NeedsUpdate(commandComp)

# Type:Server
# 添加计分板玩家项目
def addPlayer(self, playerId):
	playerName = getPlayerNameById(self, playerId)
	commandComp = self.CreateComponent(playerId, "Minecraft", "command")
	commandComp.command = ("/scoreboard players add \"" + playerName + "\" jfb 0")
	self.NeedsUpdate(commandComp)

# Type:Server
# 删除计分板玩家项目
def delPlayer(self, playerId):
	playerName = getPlayerNameById(self, playerId)
	commandComp = self.CreateComponent(playerId, "Minecraft", "command")
	commandComp.command = ("/scoreboard players reset \"" + playerName + "\" jfb")
	self.NeedsUpdate(commandComp)

# Type:Server
# 改变玩家分数
# 传入id，分数
def changeScore(self, data):
	playerId = data["id"]
	score = data["score"]
	playerName = getPlayerNameById(self, playerId)
	commandComp = self.CreateComponent(playerId, "Minecraft", "command")
	commandComp.command = ("/scoreboard players set \"" + playerName + "\" jfb " + str(score))
	self.NeedsUpdate(commandComp)

# Type: Server
# 设置方块，传入参数为dict，各参数如下：
# xyz（可不传整数）， 方块id和aux（特殊值），playerId：玩家ID（或创建者ID）
def setBlock(self, data):
	blockId = data["id"]
	aux = data["aux"]
	x = data["x"]
	y = data["y"]
	z = data["z"]
	playerId = data["playerId"]
	#设置某一位置的block
	blockInfoComp = self.CreateComponent(playerId, "Minecraft", "blockInfo")
	newBlock = {
	"pos":(int(x), int(y), int(z)),
	"playerId":playerId,
	"auxdata":aux,
	"blockId":blockId
	}
	blockInfoComp.block = newBlock
	self.NeedsUpdate(blockInfoComp)

# Type:Client
# 获取实体坐标，返回dict
# 返回取值：data["x"]以此类推
# 输入值为实体ID
def GetEntityPos(self, entityId):
	ret = {}
	comp = self.CreateComponent(entityId, "Minecraft", "pos")
	playerPos = comp.pos
	x = playerPos[0]
	y = playerPos[1]
	z = playerPos[2]
	ret["x"] = x
	ret["y"] = y
	ret["z"] = z
	return ret