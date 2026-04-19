好，现在正式进入第 2 阶段。

这一阶段的目标不是做玩法，而是让你的项目从“空骨架”变成“能初始化、能共享配置、能自动创建 Remotes 的活工程”。

这一步我们只做 4 件事：

1. 写共享常量
    
2. 写基础配置
    
3. 写 `RemoteManager`
    
4. 写 `ServerBootstrap` 最小启动流程
    

你照着一步一步做就行。先不要自己加料。

---

# 第 2 阶段你做完后，应该达到什么效果

当你点 Roblox Studio 的“运行”后，应该看到：

- 服务端启动成功
    
- `ServerBootstrap` 运行
    
- `RemoteManager` 自动创建需要的 `RemoteEvent`
    
- Output 打印出明确日志
    
- `ReplicatedStorage > Remotes > Events` 里真的出现事件对象
    

也就是说，这一阶段的“验收标准”不是界面好看，而是：

**项目启动时，基础共享层和网络层已经活了。**

---

# 第 0 步：先理解这一阶段在学什么

你这一步其实是在学 Roblox 全栈开发里最基础的工程习惯：

### 1. 常量

把不会轻易改的名字统一放一起。  
比如阵营名、Remote 名、资源类型。

### 2. 配置

把经常会调整的数值统一放一起。  
比如主城出生点名、默认等级、默认资源。

### 3. 管理器

把一类重复工作统一管理。  
比如 Remote 自动创建。

### 4. 启动脚本

让服务器启动时按顺序把项目初始化起来。

你以后系统越来越多，如果没有这一步，后面会很乱。

---

# 第 1 步：先写 `GameConstants`

路径：

```text
ReplicatedStorage
└─ Shared
   └─ Constants
      └─ GameConstants
```

请打开 `GameConstants`，把里面原来的内容删掉，替换成这个：

```lua
local GameConstants = {}

-- 阵营名称
GameConstants.Factions = {
	Wei = "Wei",
	Shu = "Shu",
	Wu = "Wu",
}

-- 资源类型
GameConstants.ResourceTypes = {
	Gold = "Gold",
	Wood = "Wood",
	Stone = "Stone",
}

-- 默认玩家数据
GameConstants.DefaultPlayerData = {
	HasSelectedLord = false,
	Faction = nil,
	LordId = nil,

	Level = 1,
	Exp = 0,

	Gold = 0,
	Wood = 0,
	Stone = 0,
}

return GameConstants
```

---

## 这一段你要理解什么

### 1. 为什么 `local GameConstants = {}`

这是在创建一个表。  
你可以把它理解成一个“总盒子”。

后面我们往这个盒子里塞：

- 阵营
    
- 资源类型
    
- 默认数据
    

### 2. 为什么最后一定要 `return GameConstants`

因为 `ModuleScript` 的核心作用，就是“返回一个值给别人用”。

别人 `require(GameConstants)` 后，拿到的就是这个表。

### 3. 为什么阵营要写成：

```lua
Wei = "Wei"
```

而不是直接到处手写 `"Wei"`？

因为以后如果你到处手写字符串，很容易：

- 拼错
    
- 大小写不统一
    
- 改名时改漏
    

统一常量后，就能写成：

```lua
GameConstants.Factions.Wei
```

这比手写 `"Wei"` 稳很多。

---

# 第 2 步：写 `RemoteNames`

路径：

```text
ReplicatedStorage
└─ Shared
   └─ Constants
      └─ RemoteNames
```

把内容替换成：

```lua
local RemoteNames = {}

RemoteNames.Events = {
	SelectLordRequest = "SelectLordRequest",
	ResourceCollectRequest = "ResourceCollectRequest",
	TeleportRequest = "TeleportRequest",
	DungeonRequest = "DungeonRequest",
}

RemoteNames.Functions = {
	-- 暂时留空，后面有需要再加
}

return RemoteNames
```

---

## 为什么这里要单独做一个模块

因为以后你会经常写这种东西：

```lua
local event = ReplicatedStorage.Remotes.Events:FindFirstChild("SelectLordRequest")
```

这很容易出问题，因为字符串是手敲的。

如果你哪天写成：

```lua
"SelectLordRequset"
```

你自己可能都看不出来。

所以后面我们会统一写：

```lua
RemoteNames.Events.SelectLordRequest
```

这样更稳。

---

# 第 3 步：写 `FactionConfig`

路径：

```text
ReplicatedStorage
└─ Shared
   └─ Config
      └─ FactionConfig
```

把内容替换成：

```lua
local GameConstants = require(game.ReplicatedStorage.Shared.Constants.GameConstants)

local FactionConfig = {}

FactionConfig.Factions = {
	[GameConstants.Factions.Wei] = {
		DisplayName = "魏",
		SpawnPointName = "WeiSpawn",
		CityName = "WeiCity",
	},

	[GameConstants.Factions.Shu] = {
		DisplayName = "蜀",
		SpawnPointName = "ShuSpawn",
		CityName = "ShuCity",
	},

	[GameConstants.Factions.Wu] = {
		DisplayName = "吴",
		SpawnPointName = "WuSpawn",
		CityName = "WuCity",
	},
}

return FactionConfig
```

---

## 这里你要重点理解两件事

### 1. 配置和常量的区别

常量是“名字、固定标识”。  
配置是“某个系统的具体规则和映射关系”。

比如：

- `GameConstants.Factions.Wei` 是常量
    
- `Wei` 对应 `WeiSpawn` 是配置
    

### 2. 为什么 key 写成：

```lua
[GameConstants.Factions.Wei]
```

因为这样你后面可以通过统一常量访问，而不是自己再打一遍 `"Wei"`。

---

# 第 4 步：写 `MapConstants`

路径：

```text
ReplicatedStorage
└─ Shared
   └─ Constants
      └─ MapConstants
```

把内容替换成：

```lua
local MapConstants = {}

MapConstants.MapFolderName = "Map"
MapConstants.CitiesFolderName = "Cities"
MapConstants.SpawnPointsFolderName = "SpawnPoints"
MapConstants.ResourceZoneFolderName = "ResourceZone"
MapConstants.DungeonInstancesFolderName = "DungeonInstances"

MapConstants.InteractablesFolderName = "Interactables"
MapConstants.TeleportersFolderName = "Teleporters"
MapConstants.ResourceNodesFolderName = "ResourceNodes"

return MapConstants
```

---

## 为什么要有这个

因为以后你会经常从 `Workspace` 找对象。

如果你每次都手写：

```lua
workspace.Map.SpawnPoints
workspace.Interactables.Teleporters
```

虽然也能写，但对象名字一旦改了，很多地方都要跟着改。

先集中在一个地方，后面维护更轻松。

---

# 第 5 步：写 `LevelConfig`

路径：

```text
ReplicatedStorage
└─ Shared
   └─ Config
      └─ LevelConfig
```

把内容替换成：

```lua
local LevelConfig = {}

LevelConfig.ExpRequiredByLevel = {
	[1] = 100,
	[2] = 200,
	[3] = 400,
	[4] = 800,
	[5] = 1600,
}

return LevelConfig
```

---

## 这一版为什么只写这么少

因为我们现在只是先把“配置结构”搭起来。  
不是现在就做完整成长系统。

只要先让你理解：

**数值表应该放配置，不应该散落在业务代码里。**

---

# 第 6 步：写 `ResourceConfig`

路径：

```text
ReplicatedStorage
└─ Shared
   └─ Config
      └─ ResourceConfig
```

把内容替换成：

```lua
local GameConstants = require(game.ReplicatedStorage.Shared.Constants.GameConstants)

local ResourceConfig = {}

ResourceConfig.NodeTypes = {
	Tree = {
		DisplayName = "树木",
		RewardType = GameConstants.ResourceTypes.Wood,
		RewardAmount = 10,
		RespawnTime = 5,
	},

	Rock = {
		DisplayName = "矿石",
		RewardType = GameConstants.ResourceTypes.Stone,
		RewardAmount = 10,
		RespawnTime = 5,
	},
}

return ResourceConfig
```

---

# 第 7 步：先不用细写 `DungeonConfig` 和 `EquipmentConfig`

这两个模块你现在可以先改成最小占位版，别一上来写太多。

## `DungeonConfig`

```lua
local DungeonConfig = {}

DungeonConfig.Dungeons = {
	TestDungeon = {
		DisplayName = "测试副本",
		RequiredLevel = 1,
		RewardGold = 50,
		RewardExp = 20,
	},
}

return DungeonConfig
```

## `EquipmentConfig`

```lua
local EquipmentConfig = {}

EquipmentConfig.Equipments = {
	WoodSword = {
		Id = "WoodSword",
		DisplayName = "木剑",
		Slot = "Weapon",
		Attack = 5,
	},
}

return EquipmentConfig
```

---

# 第 8 步：先写 `RemoteManager`

路径：

```text
ServerScriptService
└─ Server
   └─ Managers
      └─ RemoteManager
```

把内容替换成：

```lua
local ReplicatedStorage = game:GetService("ReplicatedStorage")

local RemoteNames = require(ReplicatedStorage.Shared.Constants.RemoteNames)

local RemoteManager = {}

local function createRemoteEvent(folder, remoteName)
	local existing = folder:FindFirstChild(remoteName)
	if existing then
		return existing
	end

	local remoteEvent = Instance.new("RemoteEvent")
	remoteEvent.Name = remoteName
	remoteEvent.Parent = folder

	print("[RemoteManager] Created RemoteEvent:", remoteName)

	return remoteEvent
end

function RemoteManager.Init()
	local remotesFolder = ReplicatedStorage:WaitForChild("Remotes")
	local eventsFolder = remotesFolder:WaitForChild("Events")
	local functionsFolder = remotesFolder:WaitForChild("Functions")

	for _, remoteName in pairs(RemoteNames.Events) do
		createRemoteEvent(eventsFolder, remoteName)
	end

	for _, functionName in pairs(RemoteNames.Functions) do
		local existing = functionsFolder:FindFirstChild(functionName)
		if not existing then
			local remoteFunction = Instance.new("RemoteFunction")
			remoteFunction.Name = functionName
			remoteFunction.Parent = functionsFolder

			print("[RemoteManager] Created RemoteFunction:", functionName)
		end
	end

	print("[RemoteManager] Init completed")
end

return RemoteManager
```

---

## 这一段要怎么理解

这段代码做的事很简单：

### 1. 找到：

- `ReplicatedStorage/Remotes/Events`
    
- `ReplicatedStorage/Remotes/Functions`
    

### 2. 读取 `RemoteNames`

看我们定义了哪些 Event 和 Function

### 3. 自动检查是否已经存在

如果存在，不重复创建  
如果不存在，就创建

---

## 为什么这样做好

因为以后你不用手动去 Explorer 里一个个新建 Remote。

你只需要：

- 在 `RemoteNames` 里加名字
    
- 运行游戏
    

系统就自动帮你建好。

这就是工程化。

---

# 第 9 步：写 `ServerBootstrap`

路径：

```text
ServerScriptService
└─ Server
   └─ Bootstrap
      └─ ServerBootstrap
```

把内容替换成：

```lua
local ServerScriptService = game:GetService("ServerScriptService")

local ServerFolder = ServerScriptService:WaitForChild("Server")
local ManagersFolder = ServerFolder:WaitForChild("Managers")

local RemoteManager = require(ManagersFolder:WaitForChild("RemoteManager"))

print("[ServerBootstrap] Server starting...")

RemoteManager.Init()

print("[ServerBootstrap] Server started successfully")
```

---

## 为什么这里不用一次 require 一堆模块

因为我们现在在做“最小启动流程”。

先只启动一个东西：

- `RemoteManager`
    

先确认启动链是通的。  
不要一口气把 `DataService`、`PlayerService`、`SelectionSystem` 全塞进来。

新手最容易犯的错就是一开始把所有模块全连起来，然后报错时根本不知道是谁的问题。

---

# 第 10 步：测试

现在请你做下面操作：

### 1. 保存所有脚本

### 2. 点击“运行”

### 3. 看 Output

正常情况下，你应该看到类似：

```text
[ServerBootstrap] Server starting...
[RemoteManager] Created RemoteEvent: SelectLordRequest
[RemoteManager] Created RemoteEvent: ResourceCollectRequest
[RemoteManager] Created RemoteEvent: TeleportRequest
[RemoteManager] Created RemoteEvent: DungeonRequest
[RemoteManager] Init completed
[ServerBootstrap] Server started successfully
```

---

## 然后再去 Explorer 看

展开：

```text
ReplicatedStorage
└─ Remotes
   └─ Events
```

你应该能看到自动生成的：

- `SelectLordRequest`
    
- `ResourceCollectRequest`
    
- `TeleportRequest`
    
- `DungeonRequest`
    

---

# 第 11 步：如果你报错，先按这个顺序检查

## 1. `ReplicatedStorage` 名字是否正确

必须是系统自带的 `ReplicatedStorage`

## 2. `RemoteNames` 是否 `return RemoteNames`

很多新手会忘掉最后的 `return`

## 3. `RemoteManager` 是否 `return RemoteManager`

也不能漏

## 4. `ServerBootstrap` 路径是否正确

它必须放在：

```text
ServerScriptService > Server > Bootstrap
```

而且类型必须是普通 `Script`，不是 `ModuleScript`

## 5. `RemoteManager` 类型是否正确

它必须是 `ModuleScript`

---

# 第 12 步：这一步你学到的核心知识

你做完这一轮，实际上已经掌握了 Roblox 项目里很关键的 5 个点：

### 1. `ModuleScript` 是返回表给别人用的

### 2. `require()` 是拿到模块返回值

### 3. 常量和配置应该分开

### 4. 启动逻辑应该集中在 Bootstrap

### 5. 重复创建型工作应该交给 Manager 统一处理

这几个知识点后面会一直反复用到。

---

# 你现在要做的事

先不要继续往下问新系统。  
你现在就按我上面的代码，逐个替换：

- `GameConstants`
    
- `RemoteNames`
    
- `FactionConfig`
    
- `MapConstants`
    
- `LevelConfig`
    
- `ResourceConfig`
    
- `DungeonConfig`
    
- `EquipmentConfig`
    
- `RemoteManager`
    
- `ServerBootstrap`
    

然后运行一次。

接着把两样东西发给我：

1. `Output` 截图
    
2. `ReplicatedStorage > Remotes > Events` 展开后的截图
    

我会帮你检查这一步是不是完全正确，然后再带你进下一小步：  
**给 `ClientBootstrap` 接上共享模块读取，验证客户端也能拿到这些 Remotes。**