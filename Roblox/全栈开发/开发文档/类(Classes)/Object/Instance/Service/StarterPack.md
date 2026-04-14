## 一、基础定义

`StarterPack` 是 Roblox 中的**服务级容器对象**，继承自 `Instance`（继承 `Instance` 的 57 个成员 + `Object` 的 6 个成员，拥有所有实例通用的基础属性、方法、事件），核心作用是管理玩家出生时的初始背包内容。

---

## 二、核心工作逻辑

### 1. 复制规则

- 玩家**角色首次生成**、**每次死亡复活**时，Roblox 会自动将 `StarterPack` + `StarterGear` 内的所有内容，**完整复制一份**到玩家的 `Backpack`（个人背包）中。
- 角色死亡后，旧的 `Backpack` 会被移除，新建的 `Backpack` 会重新填充 `StarterPack`/`StarterGear` 的内容，因此玩家复活后会自动恢复初始工具。

### 2. 适用内容

- 最常用：存放 `Tool`（工具 / 武器），确保所有玩家出生即获得对应工具。
- 可存放：`LocalScript`（本地脚本），保证每个玩家获取独立副本，互不干扰。
- 不可存放：服务器脚本（`Script`），仅客户端脚本可正常运行。

---

## 三、关键使用规则

### 1. 全局 vs 专属工具

- **全局工具**：放入 `StarterPack`，所有玩家出生自动获得，适合通用初始道具。
- **专属工具**：不可放入 `StarterPack`，需通过代码手动挂载到对应玩家的 `Backpack`（如 VIP 专属武器、任务奖励），示例代码：
```
-- 服务器端执行
    local Tool = game.ServerStorage.MyVIPTool
    local Player = game.Players:GetPlayerByName("玩家名")
    Tool.Parent = Player.Backpack
```
### 2. 动态修改规则

- 可在游戏运行时**服务器端**动态增删 `StarterPack` 内的工具，修改不会立即生效，需等待玩家**下一次复活**，才会同步到玩家背包。
- **禁止客户端修改**：仅服务器脚本可修改 `StarterPack`，客户端（`LocalScript`）的修改会被服务器同步覆盖，无效。

### 3. 代码操作示例

- 向 `StarterPack` 添加工具：
	- ```lua
	  local Tool = game.ServerStorage.MyTool
    Tool.Parent = game:GetService("StarterPack")
	  ```

---

## 四、核心注意事项

1. `StarterPack` 仅负责**初始复制**，玩家背包内的工具修改（如丢弃、新增）不会反向同步到 `StarterPack`。
2. 继承特性：`StarterPack` 可直接使用 `Instance` 的所有通用方法，如 `FindFirstChild()`、`Destroy()`、`ChildAdded` 事件等，无需额外实现。
3. 容器层级：`StarterPack` 是服务器端容器，内容仅在玩家生成时复制到客户端背包，本身不直接在客户端存在。

---

## 五、相关概念区分

表格

|容器|作用|生命周期|
|---|---|---|
|`StarterPack`|全局初始道具模板，所有玩家共享|服务器端，游戏全程存在|
|`Backpack`|玩家个人背包，存储当前携带道具|客户端，随角色生成 / 死亡重置|
|`StarterGear`|玩家账号绑定的初始装备，与 `StarterPack` 共同复制到背包|服务器端，随玩家账号同步|