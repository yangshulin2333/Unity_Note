```lua
local ProfileService = require(game.ServerStorage.ProfileService)
local Players = game:GetService("Players")

local DataManager = {}
local Profiles = {} -- 用于存放当前服务器在线玩家的数据

-- 1. 定义数据模板（初始值）
local DataTemplate = {
    Cash = 0,
    LastUsedPartTime = 0,
}

-- 2. 获取 ProfileStore
local ProfileStore = ProfileService.GetProfileStore(
    "PlayerData", -- 数据存储的名称
    DataTemplate  -- 初始模板
)

-- 3. 玩家加入时的处理函数
local function onPlayerAdded(player)
    -- 尝试加载玩家数据，"ForceLoad" 会在玩家从其他服务器切过来时强制接管权限
    local profile = ProfileStore:LoadProfileAsync("Player_" .. player.UserId, "ForceLoad")
    
    if profile ~= nil then
        -- 确认玩家是否还在游戏中
        profile:ListenToRelease(function()
            Profiles[player] = nil
            player:Kick("你的数据在其他地方被加载，请重新加入。")
        end)

        if player:IsDescendantOf(Players) then
            Profiles[player] = profile
            -- 这里可以初始化玩家的领袖统计表 (Leaderstats)
        else
            profile:Release()
        end
    else
        -- 加载失败，踢出玩家防止数据覆盖
        player:Kick("数据加载失败，请重新加入。")
    end
end

-- 启动监听
for _, player in ipairs(Players:GetPlayers()) do
    task.spawn(onPlayerAdded, player)
end
Players.PlayerAdded:Connect(onPlayerAdded)

-- 玩家离开时的处理
Players.PlayerRemoving:Connect(function(player)
    local profile = Profiles[player]
    if profile ~= nil then
        profile:Release() -- 释放锁定，数据会自动保存
    end
end)

-- 4. 提供给其他脚本调用的接口
function DataManager:GetPlayerData(player)
    local profile = Profiles[player]
    if profile then
        return profile.Data
    end
    return nil
end

return DataManager
```

### 1. `LoadProfileAsync`：核心加载函数

Lua

```
local profile = ProfileStore:LoadProfileAsync("Player_" .. player.UserId, "ForceLoad")
```

- **参数 1 (Key)：** `string` 类型。
    
    - **原理**：这是数据库里的“索引”。每个玩家必须唯一，所以用 `"Player_" .. player.UserId`。`UserId` 是玩家唯一的数字 ID，这样即使玩家改了名字，数据也不会丢。
        
- **参数 2 (Handle Method)：** `string` 类型。
    
    - **原理**：这里通常传 `"ForceLoad"`。它的意思是：如果数据在别的服务器被锁住了，这台服务器会强行接管它。