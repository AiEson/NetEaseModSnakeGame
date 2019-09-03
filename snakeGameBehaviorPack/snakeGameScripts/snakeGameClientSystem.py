# -*- coding: utf-8 -*-

from snakeGameScripts import snakeGameFinalValuable
from snakeGameScripts import snakeGameAlgorithm

# 获取客户端引擎API模块
import client.extraClientApi as clientApi

# 获取客户端system的基类ClientSystem
ClientSystem = clientApi.GetClientSystemCls()

#mainMod中注册的Client类
class snakeGameClientSystem(ClientSystem):

    # 按键按下，松开
    ing = 1
    ed = 0

    #客户端System初始化
    def __init__(self, namespace, systemName):
        # 首先初始化TutorialClientSystem的基类ClientSystem
        super(snakeGameClientSystem, self).__init__(namespace, systemName)
        print("==== SnakeGameClientSystem Init ====")
        self.playerId = clientApi.GetLocalPlayerId()
        # 在下方直接调用FinalValuable里会报错
        self.OnKeyPressStr = snakeGameFinalValuable.OnKeyPress
        # wasd你懂的，这是键值
        self.W = "87"
        self.A = "65"
        self.S = "83"
        self.D = "68"
        self.ListenEvent()
    # 监听函数，用于定义和监听函数。函数名称除了强调的其他都是自取的，这个函数也是。
    def ListenEvent(self):
        self.ListenForEvent(clientApi.GetEngineNamespace(), clientApi.GetEngineSystemName(), "OnClientPlayerStartMove", self, self.OnKeyPress)
        self.DefineEvent(self.OnKeyPressStr)

    def OnKeyPress(self):
        key = clientApi.GetInputVector()
        # 向服务端发送数据
        toSer = self.CreateEventData()
        toSer["id"] = self.playerId
        if key[1] > 0:
            toSer["key"] = self.W
        elif key[1] < 0:
            toSer["key"] = self.S
        elif key[0] > 0:
            toSer["key"] = self.A
        elif key[0] < 0:
            toSer["key"] = self.D
        self.NotifyToServer(self.OnKeyPressStr, toSer)

    def OnScriptTickClient(self):
        pass

    # 函数名为Destroy才会被调用，在这个System被引擎回收的时候会调这个函数来销毁一些内容
    def Destroy(self):
        pass