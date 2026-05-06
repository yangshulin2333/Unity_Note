好，进入 **P1：HUD 接真实数据**。

这一阶段目标是：

> `MainHUD` 不再显示假数据，而是显示服务端 `DataService` 里的真实玩家数据。

我们要实现这条链路：

```text
DataService 创建玩家数据
↓
客户端 HUDController 请求一次玩家数据
↓
服务端返回真实数据
↓
HUDController 更新金币 / 木材 / 石头 / 等级
↓
以后服务端数据变化时，再主动推送 PlayerDataUpdate
↓
HUD 自动刷新
```

---

# P1 总共做 4 件事

```text
P1-1：RemoteNames 增加数据同步 Remote
P1-2：DataService 改成稳定数据结构 + 支持同步
P1-3：HUDController 改成接真实数据
P1-4：SelectionSystem 选主公成功后刷新 HUD
```

---

# P1-1：修改 RemoteNames

打开：

```text
ReplicatedStorage
└─ Shared
   └─ Constants
      └─ RemoteNames
```

把它改成类似这样：

```lua
local RemoteNames = {}

RemoteNames.Events = {
	SelectLordRequest = "SelectLordRequest",
	ResourceCollectRequest = "ResourceCollectRequest",
	TeleportRequest = "TeleportRequest",
	DungeonRequest = "DungeonRequest",

	-- 服务端主动推送玩家数据给客户端
	PlayerDataUpdate = "PlayerDataUpdate",
}

RemoteNames.Functions = {
	-- 客户端主动向服务端请求当前玩家数据
	GetPlayerData = "GetPlayerData",
}

return RemoteNames
```

---

## 为什么要加两个

### `PlayerDataUpdate`

服务端主动通知客户端：

```text
你的金币变了
你的等级变了
你的木材变了
```

### `GetPlayerData`

客户端刚初始化 HUD 时，主动问服务端：

```text
我当前数据是多少？
```

这比只靠 `FireClient` 稳定，因为有时候服务端推送早了，客户端 HUD 还没初始化完。

---

# P1-2：修改 DataService

打开：

```text
ServerScriptService
└─ Server
   └─ Services
      └─ DataService
```

把内容替换成这个版本：

```lua
local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")

local GameConstants = require(ReplicatedStorage.Shared.Constants.GameConstants)
local RemoteNames = require(ReplicatedStorage.Shared.Constants.RemoteNames)

local DataService = {}

local playerDataMap = {}

local function deepCopy(original)
	if type(original) ~= "table" then
		return original
	end

	local copy = {}

	for key, value in pairs(original) do
		copy[key] = deepCopy(value)
	end

	return copy
end

local function getPlayerDataUpdateEvent()
	local remotesFolder = ReplicatedStorage:WaitForChild("Remotes")
	local eventsFolder = remotesFolder:WaitForChild("Events")

	return eventsFolder:WaitForChild(RemoteNames.Events.PlayerDataUpdate)
end

local function getGetPlayerDataFunction()
	local remotesFolder = ReplicatedStorage:WaitForChild("Remotes")
	local functionsFolder = remotesFolder:WaitForChild("Functions")

	return functionsFolder:WaitForChild(RemoteNames.Functions.GetPlayerData)
end

function DataService.Init()
	local getPlayerDataFunction = getGetPlayerDataFunction()

	getPlayerDataFunction.OnServerInvoke = function(player)
		local data = DataService.GetPlayerData(player)

		if not data then
			warn("[DataService] 客户端请求数据失败，找不到玩家数据:", player.Name)
			return nil
		end

		return deepCopy(data)
	end

	Players.PlayerAdded:Connect(function(player)
		local defaultData = deepCopy(GameConstants.DefaultPlayerData)

		playerDataMap[player.UserId] = defaultData

		print("[DataService] 玩家数据初始化完成:", player.Name)

		task.delay(1, function()
			DataService.PushPlayerData(player)
		end)
	end)

	Players.PlayerRemoving:Connect(function(player)
		playerDataMap[player.UserId] = nil

		print("[DataService] 玩家数据已移除:", player.Name)
	end)

	print("[DataService] 初始化完成")
end

function DataService.GetPlayerData(player)
	return playerDataMap[player.UserId]
end

function DataService.PushPlayerData(player)
	local data = DataService.GetPlayerData(player)

	if not data then
		warn("[DataService] 推送玩家数据失败，找不到数据:", player.Name)
		return
	end

	local playerDataUpdateEvent = getPlayerDataUpdateEvent()

	playerDataUpdateEvent:FireClient(player, deepCopy(data))

	print("[DataService] 已推送玩家数据:", player.Name)
end

function DataService.SetFaction(player, faction)
	local data = DataService.GetPlayerData(player)

	if not data then
		return false, "找不到玩家数据"
	end

	data.Faction = faction
	data.HasSelectedLord = true
	data.LordId = faction .. "_Lord"

	DataService.PushPlayerData(player)

	return true, data
end

function DataService.AddCurrency(player, currencyName, amount)
	local data = DataService.GetPlayerData(player)

	if not data then
		return false, "找不到玩家数据"
	end

	if data[currencyName] == nil then
		return false, "不存在的货币字段: " .. tostring(currencyName)
	end

	data[currencyName] += amount

	DataService.PushPlayerData(player)

	return true, data
end

return DataService
```

---

# P1-3：确认 GameConstants 默认数据结构

打开：

```text
ReplicatedStorage
└─ Shared
   └─ Constants
      └─ GameConstants
```

确认 `DefaultPlayerData` 至少是这种结构：

```lua
GameConstants.DefaultPlayerData = {
	HasSelectedLord = false,
	Faction = nil,
	LordId = nil,

	Level = 1,
	Exp = 0,

	Gold = 100,
	Wood = 20,
	Stone = 15,

	Inventory = {},
	Equipped = {},

	UnlockedDungeons = {
		TestDungeon = true,
	},
}
```

注意：  
如果你现在还用的是：

```lua
Gold = 0,
Wood = 0,
Stone = 0,
```

也没问题。只是 HUD 会显示 0。  
为了测试方便，我建议先给：

```lua
Gold = 100
Wood = 20
Stone = 15
```

---

# P1-4：修改 HUDController

你现在的 `HUDController` 应该还在用假数据。  
现在改成接服务端真实数据。

打开：

```text
StarterPlayer
└─ StarterPlayerScripts
   └─ Client
      └─ Controllers
         └─ HUDController
```

替换成这个版本。

这个版本兼容两种 HUD 结构：

### 旧结构

```text
Root > ResourceBar > GoldLabel
```

### 新结构

```text
Root > TopBar > CurrencyPanel > GoldItem > AmountLabel
```

代码如下：

```lua
local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")

local RemoteNames = require(ReplicatedStorage.Shared.Constants.RemoteNames)

local HUDController = {}

local initialized = false

local goldLabel = nil
local woodLabel = nil
local stoneLabel = nil
local levelLabel = nil

local function waitForPath(root, pathList, timeout)
	local current = root

	for _, childName in ipairs(pathList) do
		if not current then
			return nil
		end

		current = current:WaitForChild(childName, timeout or 5)

		if not current then
			return nil
		end
	end

	return current
end

local function findFirstAvailable(root, pathGroups)
	for _, pathList in ipairs(pathGroups) do
		local target = waitForPath(root, pathList, 2)

		if target then
			return target
		end
	end

	return nil
end

local function updateHUD(data)
	if not data then
		warn("[HUDController] 更新HUD失败，data为空")
		return
	end

	if goldLabel then
		goldLabel.Text = tostring(data.Gold or 0)
	end

	if woodLabel then
		woodLabel.Text = tostring(data.Wood or 0)
	end

	if stoneLabel then
		stoneLabel.Text = tostring(data.Stone or 0)
	end

	if levelLabel then
		levelLabel.Text = "等级: " .. tostring(data.Level or 1)
	end

	print("[HUDController] HUD已刷新:", "Gold =", data.Gold, "Wood =", data.Wood, "Stone =", data.Stone, "Level =", data.Level)
end

function HUDController.Init()
	if initialized then
		warn("[HUDController] 已经初始化过，跳过重复初始化")
		return
	end
	initialized = true

	local player = Players.LocalPlayer
	local playerGui = player:WaitForChild("PlayerGui")

	local mainHUD = playerGui:WaitForChild("MainHUD", 10)
	if not mainHUD then
		warn("[HUDController] 找不到 MainHUD")
		return
	end

	local root = mainHUD:WaitForChild("Root", 10)
	if not root then
		warn("[HUDController] 找不到 MainHUD.Root")
		return
	end

	goldLabel = findFirstAvailable(root, {
		{"TopBar", "CurrencyPanel", "GoldItem", "AmountLabel"},
		{"ResourceBar", "GoldLabel"},
	})

	woodLabel = findFirstAvailable(root, {
		{"TopBar", "CurrencyPanel", "WoodItem", "AmountLabel"},
		{"ResourceBar", "WoodLabel"},
	})

	stoneLabel = findFirstAvailable(root, {
		{"TopBar", "CurrencyPanel", "StoneItem", "AmountLabel"},
		{"ResourceBar", "StoneLabel"},
	})

	levelLabel = findFirstAvailable(root, {
		{"TopBar", "PlayerInfoPanel", "LevelLabel"},
		{"ResourceBar", "LevelLabel"},
	})

	if not goldLabel then
		warn("[HUDController] 找不到 Gold 显示 Label")
	end

	if not woodLabel then
		warn("[HUDController] 找不到 Wood 显示 Label")
	end

	if not stoneLabel then
		warn("[HUDController] 找不到 Stone 显示 Label")
	end

	if not levelLabel then
		warn("[HUDController] 找不到 Level 显示 Label")
	end

	local remotesFolder = ReplicatedStorage:WaitForChild("Remotes")
	local eventsFolder = remotesFolder:WaitForChild("Events")
	local functionsFolder = remotesFolder:WaitForChild("Functions")

	local playerDataUpdateEvent = eventsFolder:WaitForChild(RemoteNames.Events.PlayerDataUpdate)
	local getPlayerDataFunction = functionsFolder:WaitForChild(RemoteNames.Functions.GetPlayerData)

	playerDataUpdateEvent.OnClientEvent:Connect(function(data)
		updateHUD(data)
	end)

	local success, data = pcall(function()
		return getPlayerDataFunction:InvokeServer()
	end)

	if success then
		updateHUD(data)
	else
		warn("[HUDController] 请求初始玩家数据失败:", data)
	end

	print("[HUDController] 初始化完成")
end

return HUDController
```

---

# 注意：如果你现在的新 UI 资源文本是这样显示的

比如截图里看起来像：

```text
金币图标 + 100
宝石图标 + 9999.9K
木材图标 + 20
石头图标 + 15
```

那你需要确认它们的路径和名字是：

```text
MainHUD
└─ Root
   └─ TopBar
      └─ CurrencyPanel
         ├─ GoldItem
         │  └─ AmountLabel
         ├─ WoodItem
         │  └─ AmountLabel
         └─ StoneItem
            └─ AmountLabel
```

如果你的实际命名不是这样，比如叫：

```text
CoinLabel
GoldText
NumberLabel
```

那 `HUDController` 找不到，需要你要么改 UI 名字，要么告诉我你的实际结构，我帮你改路径。

---

# P1-5：确认 ServerBootstrap 顺序

打开：

```text
ServerScriptService
└─ Server
   └─ Bootstrap
      └─ ServerBootstrap
```

确认顺序是：

```lua
RemoteManager.Init()
DataService.Init()
SelectionSystem.Init()
TeleportSystem.Init()
```

一定要保证：

```text
RemoteManager 在 DataService 前面
```

因为 `DataService.Init()` 会找：

```text
Remotes > Events > PlayerDataUpdate
Remotes > Functions > GetPlayerData
```

这些必须先由 `RemoteManager` 创建。

---

# P1-6：SelectionSystem 不需要大改

因为我们刚才已经在 `DataService.SetFaction()` 里加了：

```lua
DataService.PushPlayerData(player)
```

所以你选完主公后，HUD 会收到一次最新数据。

如果你想在 `SelectionSystem` 里保留原来的：

```lua
local success, result = DataService.SetFaction(player, faction)
```

不用改。

---

# P1-7：测试步骤

现在测试时按这个顺序：

## 第一步：运行游戏

看 Output 是否出现：

```text
[RemoteManager] 创建了 RemoteEvent PlayerDataUpdate
[RemoteManager] 创建了 RemoteFunction GetPlayerData
[DataService] 初始化完成
```

---

## 第二步：看 HUD

HUD 应该显示服务端默认数据：

```text
Gold = GameConstants.DefaultPlayerData.Gold
Wood = GameConstants.DefaultPlayerData.Wood
Stone = GameConstants.DefaultPlayerData.Stone
Level = GameConstants.DefaultPlayerData.Level
```

不是 HUDController 里写死的假数据。

---

## 第三步：选主公

选完主公后，Output 应该出现：

```text
[DataService] 已推送玩家数据
[HUDController] HUD已刷新
```

---

## 第四步：临时测试数据变化

为了确认 HUD 真接上了服务端数据，你可以临时在 `SelectionSystem` 选主公成功后加一行测试代码：

```lua
DataService.AddCurrency(player, "Gold", 50)
```

放在选主公成功之后。

测试时如果 HUD 金币从 100 变成 150，说明：

```text
服务端改数据 → 推送客户端 → HUD刷新
```

完整通了。

测试完可以删掉这行。

---

# P1 完成标准

你完成后应该满足：

```text
[ ] RemoteNames 里有 PlayerDataUpdate
[ ] RemoteNames 里有 GetPlayerData
[ ] RemoteManager 自动创建 PlayerDataUpdate
[ ] RemoteManager 自动创建 GetPlayerData
[ ] DataService 能创建默认玩家数据
[ ] HUDController 不再写假数据
[ ] HUDController 会 InvokeServer 请求初始数据
[ ] HUDController 会监听 PlayerDataUpdate
[ ] HUD 显示服务端数据
[ ] 服务端数据变化后 HUD 会刷新
```

---

你先做这一步。  
做完后发我：

1. `ReplicatedStorage > Remotes > Events / Functions` 展开截图
    
2. HUD 显示截图
    
3. Output 截图，尤其是 `[HUDController] HUD已刷新` 那几行
    

我帮你验收。