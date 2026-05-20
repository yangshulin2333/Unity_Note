## A. 基础架构测试

你应该能回答：

1. **ServerScriptService 里一般放什么？**
2. **ReplicatedStorage 里一般放什么？**
3. **StarterGui 和 PlayerGui 有什么区别？**
4. **LocalScript 为什么不能直接改服务端数据？**
5. **RemoteEvent 是为了解决什么问题？**
6. **ModuleScript 和普通 Script 的区别是什么？**
7. **Config 表为什么适合放装备、商店、资源配置？**

如果你这里能说出 60%，说明你不是零基础了。

回答：
1. ServerScriptService 里具体一般放**server服务**：比如bootstrap 初始化入口，初始化system 下的各个模块。**system服务**：具体的游戏功能，比如传送，采集，选择主公。**service服务**：所有的校验机制都在这里，以及对接 clint那边通过RemoteEvent函数请求过来的内容做出具体的回复，都是在service里。
2. ReplicatedStorage 里一般放 一些公共存储的服务，比如公共的包**package**，里面的代码可以被任何地方调用，不影响游戏逻辑。还有就是share文件夹，再向下细分就是一些constants游戏常量，config配置表。 也可以放一个remote文件夹，但remote函数是通过 remoteManager代码读取constans里的remoteConstants自动创建出来的。
3. StaterGui内的东西会在游戏运行开始后都复制到PlayerGui内，其他的就不知道了
4. **LocalScript 为什么不能直接改服务端数据？** 这个没具体了解过，不知道
5. **RemoteEvent 是为了解决什么问题？** 为了解决服务端与客户端通讯的问题。主要是为了防止玩家修改服务端数据，防止外挂
6. ModuleScript 是模块化代码，Script是服务端代码，我一般写某个功能的时候用ModuleScript，这个也没具体了解过
7. **Config 表为什么适合放装备、商店、资源配置？** 一方面是防止拼写出错，另一方面方便维护修改
   
   以上内容，都是我目前脑子里的东西，我借助任何外物

## B. 项目链路测试

如果让我看着项目结构目录我大概是能说出来的，如果直接让我现在说我的回答则是：
玩家 点击购买UI按钮后，首先点击的是MainHud上的按钮。后台会先到starterPlayerScript 客户端下单mainMenu那个moduleScript 里找到按钮路径，然后进行绑定按钮。 然后被初始化，接着触发回调函数mouse1click。到shopController内，然后远程通信ShopSystem模块进行验证，验证通过则购买成功

以上内容都是我目前脑子里的东西，我借助任何外物，包括：
```
玩家点击 Shop UI  
↓  
LocalScript 读取按钮对应 itemId  
↓  
通过 RemoteEvent 发请求到服务端  
↓  
服务端检查玩家金币是否足够  
↓  
服务端读取 ShopConfig / EquipmentConfig  
↓  
扣金币  
↓  
把装备加入玩家 Inventory 数据  
↓  
通知客户端刷新 HUD / 背包 UI
```

我也没看过。然后就是看完后你这些流程我就又想到了shopGui里的 物品模版，config里的shopconfig。

## C. Debug 测试

遇到报错：
```lua
attempt to index nil with 'WaitForChild'
```

我想到的就是 系统没有找到WaitForChild 后面的 文件，有可能是拼音打错了
