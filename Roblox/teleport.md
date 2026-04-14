```Luau
local CollectionService = game:GetService("CollectionService")
local Players = game:GetService("Players")

-- 通用配置（只改这里即可）
local CONFIG = {
	Tag = "Teleporter",               -- 传送门统一标签
	Cooldown = 1,                     -- 传送冷却秒数
	HeightOffset = 3,                 -- 传送后抬高高度
	PushForce = 50,                   -- 拒绝时的推力
	UpForce = 30                      -- 拒绝时向上的力
}

-- 通用传送处理
local function handleTeleport(otherPart, teleporter)
	-- 安全获取角色
	local character = otherPart:FindFirstAncestorOfClass("Model")
	if not character then return end

	local humanoid = character:FindFirstChild("Humanoid")
	local rootPart = character:FindFirstChild("HumanoidRootPart")
	local isTeleporting = character:GetAttribute("IsTeleporting")

	if not humanoid or not rootPart or isTeleporting then
		return
	end

	-- 阵营权限校验（完全属性驱动，通用）
	local player = Players:GetPlayerFromCharacter(character)
	local requiredTeam = teleporter:GetAttribute("RequiredTeam")

	if player and requiredTeam then
		local playerTeamName = player.Team and player.Team.Name or ""
		if playerTeamName ~= requiredTeam then
			-- 通用击退逻辑
			local dir = (rootPart.Position - teleporter.Position).Unit
			rootPart.AssemblyLinearVelocity = dir * CONFIG.PushForce + Vector3.new(0, CONFIG.UpForce, 0)
			return
		end
	end

	-- 通用传送逻辑
	local targetValue = teleporter:FindFirstChild("Target")
	if targetValue and targetValue.Value then
		character:SetAttribute("IsTeleporting", true)

		-- 目标位置 + 抬高
		rootPart.CFrame = targetValue.Value.CFrame * CFrame.new(0, CONFIG.HeightOffset, 0)

		-- 冷却
		task.wait(CONFIG.Cooldown)
		character:SetAttribute("IsTeleporting", nil)
	end
end

-- 绑定传送门
local function setupTeleporter(part)
	if part:IsA("BasePart") then --所有能踩、能碰、能触发 Touched 事件的实体，都继承自 BasePart
		part.Touched:Connect(function(hit) --确保能调用Touched方法
			handleTeleport(hit, part)
		end)
	end
end

-- 初始化所有已存在的传送门
for _, part in CollectionService:GetTagged(CONFIG.Tag) do
	setupTeleporter(part)
end

-- 监听未来新增的传送门
CollectionService:GetInstanceAddedSignal(CONFIG.Tag):Connect(setupTeleporter)
```

运行要求：

1. 2 个 Part
2. 给其中 1 个 Part 加标签 **Teleporter**
3. 这个 Part 下面加 **ObjectValue 命名 Target**
4. Target 指向另一个 Part
5. 脚本放入 ServerScriptService

**满足以上 5 条 → 直接运行，就能传送！**





## 1. **服务（Service）**

游戏里所有功能必须通过官方服务获取：

- `Players`：管理玩家
- `CollectionService`：管理标签

> 知识点：**不直接用 workspace.xxx 硬找，而是用服务解耦**

## 2. **标签驱动（Tag）**

- 给零件打 `Teleporter` 标签
- 脚本自动识别所有传送门

> 知识点：**零件只存数据，脚本只跑逻辑 → 完全解耦**

## 3. **FindFirstAncestorOfClass("Model")**

- 精准找到玩家角色模型
- 比 `otherPart.Parent` 更稳定

> 知识点：**角色结构是固定 Model，这是标准写法**

## 4. **防抖标记 IsTeleporting**

- 防止一秒触发几十次传送
- 用 `Attribute` 动态标记状态

> 知识点：**游戏逻辑必须做防抖**

## 5. **阵营权限校验（核心）**



```
local requiredTeam = 传送门属性
local playerTeam = 玩家的队伍名称
if 不一致 → 弹开 + return
```

> 知识点：**游戏权限系统底层 = 比对数据**

## 6. **击退物理逻辑**



```
dir = 玩家位置 - 传送门位置 → 单位向量
速度 = dir * 力量 + 向上跳
```

> 知识点：**游戏物理 = 向量运算**

------

# 📌 一句话总结这段代码的架构

**标签识别 → 碰撞触发 → 角色检测 → 阵营校验 → 允许 / 拦截 → 传送 / 击退**

这就是**所有游戏传送门、安全区、副本准入、阵营保护**的通用底层模型。





| **维度**     | **对应技术点**               | **作用**                                                     |
| ------------ | ---------------------------- | ------------------------------------------------------------ |
| **层级管理** | `FindFirstAncestorOfClass`   | **向上溯源**。解决碰撞时只拿到“脚”的问题，确保拿到的是整个“人”模型。 |
| **属性系统** | `Attributes` (IsTeleporting) | **状态机控制**。比 `bool` 变量更灵活，它是附加在对象身上的元数据，自带跨脚本读取能力。 |
| **逻辑保护** | `A and B or C`               | **防御性编程**。防止因为玩家没阵营（`nil`）导致的程序空指针崩溃。 |
| **空间计算** | `CFrame` 矩阵乘法            | **相对坐标变换**。`destination.CFrame * CFrame.new(0, 3, 0)` 是在目标零件的“本地坐标系”向上移，不会受零件旋转影响。 |





类名:方法名( 参数名 : 参数类型 ) : 返回值类型