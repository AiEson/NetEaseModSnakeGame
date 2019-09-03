#-*- coding: utf-8 -*-
#绑定类import
from common.mod import Mod
#import服务端API模块
import server.extraServerApi as serverApi
#import客户端API模块
import client.extraClientApi as clientApi

from snakeGameScripts import snakeGameFinalValuable

#绑定MOD类，识别这个类是MOD的入口类
@Mod.Binding(name = snakeGameFinalValuable.ModName, version = snakeGameFinalValuable.ModVersion)
class ParticleSpriteMod(object):

    #类的初始化函数
    def __init__(self):
        print("==========init MOD===========")

    # InitServer绑定的函数作为服务端脚本初始化的入口函数，通常是用来注册服务端系统system和组件component
    @Mod.InitServer()
    def ParticleSpriteServerInit(self):
        print("==========init server=========")
        # 函数可以将System注册到服务端引擎中，实例的创建和销毁交给引擎处理。第一个参数是MOD名称，第二个是System名称，第三个是自定义MOD System类的路径
        serverApi.RegisterSystem(snakeGameFinalValuable.ModName, snakeGameFinalValuable.ServerName, "snakeGameScripts.snakeGameServerSystem.snakeGameServerSystem")

    # DestroyServer绑定的函数作为服务端脚本退出的时候执行的析构函数，通常用来反注册一些内容,可为空
    @Mod.DestroyServer()
    def ParticleSpriteServerDestroy(self):
        print("===== destroy mod server =====")

    @Mod.InitClient()
    def ParticleSpriteClientInit(self):
        print("=======init client==========")
        # 函数可以将System注册到客户端引擎中，实例的创建和销毁交给引擎处理。第一个参数是MOD名称，第二个是System名称，第三个是自定义MOD System类的路径
        serverApi.RegisterSystem(snakeGameFinalValuable.ModName, snakeGameFinalValuable.ClientName, "snakeGameScripts.snakeGameClientSystem.snakeGameClientSystem")

    # DestroyClient绑定的函数作为客户端脚本退出的时候执行的析构函数，通常用来反注册一些内容,可为空
    @Mod.DestroyClient()
    def ParticleSpriteClientDestroy(self):
        print("===== destroy mod client =====")

