P3 验收通过。你现在已经有：

```text
资源点识别
→ 采集提示
→ 采集进度条
→ 服务端校验
→ 加 Wood / Stone
→ HUD 自动刷新
→ 冷却判定
```

现在进入 **P4：商店系统真实接入**。

---

# P4 目标

这一步要完成：

```text
打开 ShopGui
↓
ShopController 从 ShopConfig 读取商品
↓
动态生成商品按钮
↓
点击购买
↓
客户端发送 BuyItemRequest
↓
ShopSystem 服务端校验商品 / 金币
↓
DataService 扣金币
↓
DataService 加入背包 Inventory
↓
DataService 推送玩家数据
↓
HUD 金币刷新
↓
客户端显示购买成功 / 失败
```

第一版只做：

- 金币购买
    
- 买装备进背包数据
    
- 不做穿戴
    
- 不做背包显示
    
- 不做 Robux 充值
    
- 不做限购
    

---

# P4-0：你将新增 / 修改这些文件

```text
ReplicatedStorage
└─ Shared
   ├─ Config
   │  ├─ ShopConfig          新增
   │  └─ EquipmentConfig     修改
   └─ Constants
      └─ RemoteNames         修改

ServerScriptService
└─ Server
   ├─ Services
   │  └─ DataService         修改
   ├─ Systems
   │  └─ ShopSystem          新增
   └─ Bootstrap
      └─ ServerBootstrap     修改

StarterPlayerScripts
└─ Client
   └─ Controllers
      └─ ShopController      新增

StarterGui
└─ ShopGui                   需要有基础 UI 结构
```

---

# P4-1：确认 ShopGui 结构

你的 `ShopGui` 至少要有这个结构：

```text
ShopGui
└─ Root
   ├─ BackgroundDim
   └─ Window
      ├─ Header
      │  ├─ TitleLabel
      │  └─ CloseButton
      ├─ Content
      │  └─ ItemList
      └─ Footer
         └─ TipLabel
```

对象类型建议：

```text
ShopGui        = ScreenGui
Root           = Frame
BackgroundDim  = Frame
Window         = Frame
Header         = Frame
TitleLabel     = TextLabel
CloseButton    = TextButton
Content        = Frame 或 ScrollingFrame
ItemList       = Frame 或 ScrollingFrame
Footer         = Frame
TipLabel       = TextLabel
```

如果你现在 `ShopGui` 已经有 `Root / Window / Header / Content / Footer`，只需要在：

```text
ShopGui > Root > Window > Content
```

下面加一个：

```text
ItemList
```

`ItemList` 类型可以先用 `Frame`。

`TipLabel` 如果没有，也可以先不建，代码会兼容。

---

# P4-2：修改 `RemoteNames`

打开：

```text
ReplicatedStorage > Shared > Constants > RemoteNames
```

在 `Events` 里新增：

```lua
BuyItemRequest = "BuyItemRequest",
```

最终类似：

```lua
local RemoteNames = {}

RemoteNames.Events = {
	SelectLordRequest = "SelectLordRequest",
	ResourceCollectRequest = "ResourceCollectRequest",
	TeleportRequest = "TeleportRequest",
	DungeonRequest = "DungeonRequest",
	PlayerDataUpdate = "PlayerDataUpdate",

	BuyItemRequest = "BuyItemRequest",
}

RemoteNames.Functions = {
	GetPlayerData = "GetPlayerData",
}

return RemoteNames
```

说明：

- 客户端点击购买时，用 `BuyItemRequest:FireServer(itemId)`
    
- 服务端购买成功 / 失败后，用同一个 Remote `FireClient` 回结果
    

---

# P4-3：修改 `EquipmentConfig`

打开：

```text
ReplicatedStorage > Shared > Config > EquipmentConfig
```

替换成：

```lua
local EquipmentConfig = {}

EquipmentConfig.Equipments = {
	WoodSword = {
		Id = "WoodSword",
		DisplayName = "木剑",
		Slot = "Weapon",
		Attack = 5,
		Defense = 0,
		Hp = 0,
	},

	IronSword = {
		Id = "IronSword",
		DisplayName = "铁剑",
		Slot = "Weapon",
		Attack = 12,
		Defense = 0,
		Hp = 0,
	},

	ClothArmor = {
		Id = "ClothArmor",
		DisplayName = "布甲",
		Slot = "Armor",
		Attack = 0,
		Defense = 4,
		Hp = 20,
	},

	IronArmor = {
		Id = "IronArmor",
		DisplayName = "铁甲",
		Slot = "Armor",
		Attack = 0,
		Defense = 10,
		Hp = 50,
	},
}

return EquipmentConfig
```

第一版先只做装备模板。

---

# P4-4：新增 `ShopConfig`

在：

```text
ReplicatedStorage > Shared > Config
```

新建 `ModuleScript`：

```text
ShopConfig
```

内容：

```lua
local GameConstants = require(game.ReplicatedStorage.Shared.Constants.GameConstants)

local ShopConfig = {}

ShopConfig.Items = {
	WoodSword = {
		ItemId = "WoodSword",
		DisplayName = "木剑",
		Desc = "新手用的基础武器，攻击 +5",
		PriceType = GameConstants.ResourceTypes.Gold,
		Price = 50,
	},

	IronSword = {
		ItemId = "IronSword",
		DisplayName = "铁剑",
		Desc = "更锋利的武器，攻击 +12",
		PriceType = GameConstants.ResourceTypes.Gold,
		Price = 150,
	},

	ClothArmor = {
		ItemId = "ClothArmor",
		DisplayName = "布甲",
		Desc = "基础护甲，防御 +4，生命 +20",
		PriceType = GameConstants.ResourceTypes.Gold,
		Price = 80,
	},

	IronArmor = {
		ItemId = "IronArmor",
		DisplayName = "铁甲",
		Desc = "更结实的护甲，防御 +10，生命 +50",
		PriceType = GameConstants.ResourceTypes.Gold,
		Price = 200,
	},
}

ShopConfig.DisplayOrder = {
	"WoodSword",
	"IronSword",
	"ClothArmor",
	"IronArmor",
}

return ShopConfig
```

这里先只支持金币购买。

---

# P4-5：修改 `GameConstants`

确认 `DefaultPlayerData` 里有：

```lua
Inventory = {},
Equipped = {},
```

推荐完整结构：

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

如果你已经有这些字段，就不用重复改。

---

# P4-6：修改 `DataService`

打开：

```text
ServerScriptService > Server > Services > DataService
```

在已有代码基础上新增这些函数。

## 1. 添加生成物品实例 ID 的函数

放在文件上方工具函数区域：

```lua
local nextInventoryId = 0

local function generateInventoryInstanceId(player, itemId)
	nextInventoryId += 1
	return tostring(player.UserId) .. "_" .. itemId .. "_" .. tostring(os.time()) .. "_" .. tostring(nextInventoryId)
end
```

---

## 2. 新增扣货币函数

放在 `DataService.AddCurrency` 后面：

```lua
function DataService.SpendCurrency(player, currencyName, amount)
	local data = DataService.GetPlayerData(player)

	if not data then
		return false, "找不到玩家数据"
	end

	if data[currencyName] == nil then
		return false, "不存在的货币字段: " .. tostring(currencyName)
	end

	if data[currencyName] < amount then
		return false, "资源不足"
	end

	data[currencyName] -= amount

	DataService.PushPlayerData(player)

	return true, data
end
```

---

## 3. 新增加入背包函数

继续放后面：

```lua
function DataService.AddInventoryItem(player, itemId)
	local data = DataService.GetPlayerData(player)

	if not data then
		return false, "找不到玩家数据"
	end

	if type(data.Inventory) ~= "table" then
		data.Inventory = {}
	end

	local itemInstance = {
		InstanceId = generateInventoryInstanceId(player, itemId),
		ItemId = itemId,
		Level = 0,
	}

	table.insert(data.Inventory, itemInstance)

	DataService.PushPlayerData(player)

	return true, itemInstance
end
```

---

## 4. 新增获取背包函数，方便后面调试

```lua
function DataService.GetInventory(player)
	local data = DataService.GetPlayerData(player)

	if not data then
		return nil
	end

	return data.Inventory
end
```

---

# 注意：这里会推送两次数据

购买时如果先 `SpendCurrency`，再 `AddInventoryItem`，会推送两次 HUD 数据。

第一版可以接受。  
后面优化时，我们再做一个批量更新函数，避免多次推送。

---

# P4-7：新增 `ShopSystem`

在：

```text
ServerScriptService > Server > Systems
```

新建 `ModuleScript`：

```text
ShopSystem
```

内容：

```lua
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local ServerScriptService = game:GetService("ServerScriptService")

local RemoteNames = require(ReplicatedStorage.Shared.Constants.RemoteNames)
local ShopConfig = require(ReplicatedStorage.Shared.Config.ShopConfig)
local EquipmentConfig = require(ReplicatedStorage.Shared.Config.EquipmentConfig)

local ServerFolder = ServerScriptService:WaitForChild("Server")
local ServicesFolder = ServerFolder:WaitForChild("Services")

local DataService = require(ServicesFolder:WaitForChild("DataService"))

local ShopSystem = {}

local function isValidShopItem(itemId)
	if type(itemId) ~= "string" then
		return false
	end

	if not ShopConfig.Items[itemId] then
		return false
	end

	return true
end

function ShopSystem.Init()
	local remotesFolder = ReplicatedStorage:WaitForChild("Remotes")
	local eventsFolder = remotesFolder:WaitForChild("Events")

	local buyItemEvent = eventsFolder:WaitForChild(RemoteNames.Events.BuyItemRequest)

	buyItemEvent.OnServerEvent:Connect(function(player, itemId)
		print("[ShopSystem] 收到购买请求:", player.Name, itemId)

		if not isValidShopItem(itemId) then
			warn("[ShopSystem] 非法商品:", itemId)
			buyItemEvent:FireClient(player, {
				success = false,
				message = "商品不存在",
			})
			return
		end

		local shopItem = ShopConfig.Items[itemId]
		local equipment = EquipmentConfig.Equipments[shopItem.ItemId]

		if not equipment then
			warn("[ShopSystem] 商品对应装备不存在:", shopItem.ItemId)
			buyItemEvent:FireClient(player, {
				success = false,
				message = "装备配置不存在",
			})
			return
		end

		local successSpend, spendResult = DataService.SpendCurrency(player, shopItem.PriceType, shopItem.Price)

		if not successSpend then
			warn("[ShopSystem] 扣费失败:", spendResult)
			buyItemEvent:FireClient(player, {
				success = false,
				message = spendResult,
			})
			return
		end

		local successAdd, itemInstance = DataService.AddInventoryItem(player, shopItem.ItemId)

		if not successAdd then
			warn("[ShopSystem] 加入背包失败:", itemInstance)

			-- 第一版暂时不做退款逻辑，后面可以补
			buyItemEvent:FireClient(player, {
				success = false,
				message = "加入背包失败",
			})
			return
		end

		print("[ShopSystem] 购买成功:", player.Name, shopItem.ItemId)

		buyItemEvent:FireClient(player, {
			success = true,
			message = "购买成功",
			itemId = shopItem.ItemId,
			displayName = equipment.DisplayName,
			instanceId = itemInstance.InstanceId,
		})
	end)

	print("[ShopSystem] 初始化完成")
end

return ShopSystem
```

---

# P4-8：接入 `ServerBootstrap`

打开：

```text
ServerScriptService > Server > Bootstrap > ServerBootstrap
```

新增 require：

```lua
local ShopSystem = require(SystemsFolder:WaitForChild("ShopSystem"))
```

初始化里加：

```lua
ShopSystem.Init()
```

推荐顺序：

```lua
RemoteManager.Init()
DataService.Init()
SelectionSystem.Init()
TeleportSystem.Init()
ResourceSystem.Init()
ShopSystem.Init()
```

示例：

```lua
local ServerScriptService = game:GetService("ServerScriptService")

local ServerFolder = ServerScriptService:WaitForChild("Server")
local ManagersFolder = ServerFolder:WaitForChild("Managers")
local ServicesFolder = ServerFolder:WaitForChild("Services")
local SystemsFolder = ServerFolder:WaitForChild("Systems")

local RemoteManager = require(ManagersFolder:WaitForChild("RemoteManager"))
local DataService = require(ServicesFolder:WaitForChild("DataService"))
local SelectionSystem = require(SystemsFolder:WaitForChild("SelectionSystem"))
local TeleportSystem = require(SystemsFolder:WaitForChild("TeleportSystem"))
local ResourceSystem = require(SystemsFolder:WaitForChild("ResourceSystem"))
local ShopSystem = require(SystemsFolder:WaitForChild("ShopSystem"))

print("[ServerBootstrap] 服务器启动中...")

RemoteManager.Init()
DataService.Init()
SelectionSystem.Init()
TeleportSystem.Init()
ResourceSystem.Init()
ShopSystem.Init()

print("[ServerBootstrap] 服务启动完成")
```

---

# P4-9：新增 `ShopController`

在：

```text
StarterPlayerScripts > Client > Controllers
```

新建：

```text
ShopController
```

内容：

```lua
local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")

local RemoteNames = require(ReplicatedStorage.Shared.Constants.RemoteNames)
local ShopConfig = require(ReplicatedStorage.Shared.Config.ShopConfig)

local ShopController = {}

local initialized = false

local function clearChildrenExceptLayout(parent)
	for _, child in ipairs(parent:GetChildren()) do
		if not child:IsA("UIListLayout")
			and not child:IsA("UIPadding")
			and not child:IsA("UIGridLayout")
			and not child:IsA("UICorner")
			and not child:IsA("UIStroke") then
			child:Destroy()
		end
	end
end

local function createShopItemButton(itemList, itemConfig)
	local button = Instance.new("TextButton")
	button.Name = itemConfig.ItemId .. "Button"
	button.Size = UDim2.new(1, -10, 0, 70)
	button.BackgroundTransparency = 0.15
	button.TextScaled = true
	button.TextWrapped = true
	button.Text = itemConfig.DisplayName .. "\n价格: " .. tostring(itemConfig.Price) .. " " .. tostring(itemConfig.PriceType)
	button.Parent = itemList

	return button
end

local function findItemList(root)
	local window = root:WaitForChild("Window", 5)
	if not window then
		return nil
	end

	local content = window:WaitForChild("Content", 5)
	if not content then
		return nil
	end

	local itemList = content:FindFirstChild("ItemList")

	if itemList then
		return itemList
	end

	return content
end

local function findTipLabel(root)
	local window = root:FindFirstChild("Window")
	if not window then
		return nil
	end

	local footer = window:FindFirstChild("Footer")
	if not footer then
		return nil
	end

	return footer:FindFirstChild("TipLabel")
end

function ShopController.Init()
	if initialized then
		warn("[ShopController] 已经初始化过，跳过重复初始化")
		return
	end
	initialized = true

	local player = Players.LocalPlayer
	local playerGui = player:WaitForChild("PlayerGui")

	local shopGui = playerGui:WaitForChild("ShopGui", 10)
	if not shopGui then
		warn("[ShopController] 找不到 ShopGui")
		return
	end

	local root = shopGui:WaitForChild("Root", 10)
	if not root then
		warn("[ShopController] 找不到 ShopGui.Root")
		return
	end

	local itemList = findItemList(root)
	if not itemList then
		warn("[ShopController] 找不到 ShopGui 的商品列表")
		return
	end

	local tipLabel = findTipLabel(root)

	local remotesFolder = ReplicatedStorage:WaitForChild("Remotes")
	local eventsFolder = remotesFolder:WaitForChild("Events")
	local buyItemEvent = eventsFolder:WaitForChild(RemoteNames.Events.BuyItemRequest)

	clearChildrenExceptLayout(itemList)

	for _, itemId in ipairs(ShopConfig.DisplayOrder) do
		local itemConfig = ShopConfig.Items[itemId]

		if itemConfig then
			local button = createShopItemButton(itemList, itemConfig)

			button.MouseButton1Click:Connect(function()
				print("[ShopController] 请求购买:", itemConfig.ItemId)

				if tipLabel then
					tipLabel.Text = "正在购买 " .. itemConfig.DisplayName .. "..."
				end

				buyItemEvent:FireServer(itemConfig.ItemId)
			end)
		end
	end

	buyItemEvent.OnClientEvent:Connect(function(response)
		if not response then
			return
		end

		if response.success then
			print("[ShopController] 购买成功:", response.displayName)

			if tipLabel then
				tipLabel.Text = "购买成功：" .. tostring(response.displayName)
			end
		else
			warn("[ShopController] 购买失败:", response.message)

			if tipLabel then
				tipLabel.Text = "购买失败：" .. tostring(response.message)
			end
		end
	end)

	print("[ShopController] 初始化完成")
end

return ShopController
```

---

# P4-10：接入 `ClientBootstrap`

打开：

```text
StarterPlayerScripts > Client > Bootstrap > ClientBootstrap
```

新增 require：

```lua
local ShopController = require(ControllersFolder:WaitForChild("ShopController"))
```

初始化里加：

```lua
LoadingController.SetStatus("正在初始化商店系统...")
ShopController.Init()
```

推荐放在 `MainMenuController.Init(UIManager)` 前后都可以。建议放在前面：

```lua
LoadingController.SetStatus("正在初始化资源采集系统...")
ResourceController.Init()

LoadingController.SetStatus("正在初始化商店系统...")
ShopController.Init()

LoadingController.SetStatus("正在初始化主菜单...")
MainMenuController.Init(UIManager)
```

---

# P4-11：测试流程

## 测试 1：启动检查

运行后 Output 应该出现：

```text
[RemoteManager] 创建了 RemoteEvent BuyItemRequest
[ShopSystem] 初始化完成
[ShopController] 初始化完成
```

---

## 测试 2：打开商店

点击主界面的商店按钮。

应该打开 `ShopGui`，并看到商品按钮：

```text
木剑
铁剑
布甲
铁甲
```

---

## 测试 3：购买木剑

点击木剑。

Output 应该出现：

```text
[ShopController] 请求购买: WoodSword
[ShopSystem] 收到购买请求: 玩家名 WoodSword
[ShopSystem] 购买成功: 玩家名 WoodSword
[ShopController] 购买成功: 木剑
```

HUD 金币应该减少 50。

---

## 测试 4：金币不足

你可以连续买几次，直到钱不够。

应该提示：

```text
购买失败：资源不足
```

---

# P4 完成标准

你完成后应该满足：

```text
[ ] BuyItemRequest 自动生成
[ ] ShopConfig 存在商品配置
[ ] EquipmentConfig 存在装备配置
[ ] ShopSystem 初始化完成
[ ] ShopController 初始化完成
[ ] 打开 ShopGui 能看到商品
[ ] 点击商品能发送购买请求
[ ] 服务端校验商品存在
[ ] 服务端扣 Gold
[ ] 服务端把装备加入 Inventory
[ ] HUD 金币减少
[ ] 购买成功 / 失败有提示
```

---

# 这一步最容易出问题的地方

## 1. 商店按钮点了打不开

看你的 `MainMenuController` 是否能找到：

```text
MainHUD > Root > BottomMenu > ShopButton
```

你之前 Output 里有：

```text
找不到按钮，跳过绑定: ShopButton
```

如果你还没修这个，先检查实际路径。

---

## 2. ShopGui 打开了但没商品

检查：

```text
ShopGui > Root > Window > Content > ItemList
```

如果你没有 `ItemList`，代码会用 `Content` 本身生成按钮。

---

## 3. 购买时服务端报商品不存在

检查：

```text
ShopConfig.Items[itemId]
```

和按钮传的 `itemConfig.ItemId` 是否一致。

---

## 4. 扣金币失败

检查 `GameConstants.ResourceTypes.Gold` 是不是：

```lua
Gold = "Gold"
```

并且 `DefaultPlayerData` 里有：

```lua
Gold = 100
```

---

## 5. HUD 没刷新

检查 `DataService.SpendCurrency()` 和 `DataService.AddInventoryItem()` 是否都有：

```lua
DataService.PushPlayerData(player)
```

---

你先按这套做。完成后发我：

1. `ShopGui` 打开截图
    
2. 点击购买后的 Output 截图
    
3. HUD 金币减少后的截图
    

我帮你验收，然后下一步接 **P5：背包系统真实接入**。