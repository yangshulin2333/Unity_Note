## 一、基础定义

`ProximityPrompt` 是 Roblox 内置的**交互提示组件**，用于在 3D 对象上显示 “按 E 交互” 的提示 UI，玩家靠近时自动显示，按指定按键触发交互逻辑。

常用于开门、捡道具、对话、开关、调查等交互场景。

---

## 二、核心工作逻辑

1. **依附对象**
    
    必须放在 `Part`/`Model`/`Tool` 等 3D 对象下，才能在世界中显示。
    
2. **距离检测**
    
    系统自动判断玩家与对象的距离，在 `MaxActivationDistance` 范围内显示提示，超出则隐藏。
    
3. **触发流程**
    
    - 玩家进入范围 → UI 自动出现
    - 玩家按下设置键（默认 E）→ 触发 `Triggered` 事件
    - 可设置是否需要长按、是否可重复触发
    
4. **客户端自动管理**
    
    显示、隐藏、按键监听均由引擎自动处理，无需自己写距离判断与 UI。
    

---

## 三、关键使用规则

### 常用属性

- `Enabled`：是否启用提示
- `ObjectText`：主文字（如 “箱子”）
- `ActionText`：操作文字（如 “打开”）
- `KeyCode`：触发按键（默认 `Enum.KeyCode.E`）
- `MaxActivationDistance`：最大可交互距离
- `HoldDuration`：长按时间（0 为点击触发）
- `RequiresLineOfSight`：是否需要无遮挡视线

### 核心事件

- `Triggered`：玩家成功触发时执行（最常用）
- `PromptShown`：提示显示时
- `PromptHidden`：提示隐藏时
- `PromptButtonHoldBegan`：开始长按时
- `PromptButtonHoldEnded`：结束长按时

### 简单示例

lua

```
local prompt = script.Parent

prompt.Triggered:Connect(function(player)
    print(player.Name .. " 触发了交互")
end)
```

---

## 四、核心注意事项

1. **必须放在 3D 对象下**
    
    直接放在 `Workspace` 根目录不会显示。
    
2. **脚本位置**
    
    - 逻辑写在 `Script`（服务器）可做权限、物品、 doors 等安全操作
    - 写在 `LocalScript` 可做纯客户端表现（不推荐关键逻辑）
    
3. **多个 Prompt 不冲突**
    
    同一对象可放多个，但会重叠显示。
    
4. **默认 UI 可覆盖**
    
    可通过 `StarterGui:SetCoreGuiEnabled` 或自定义 UI 替换原生样式。
    
5. **触发范围是球形检测**
    
    以对象中心为球心，不是盒形。
    

---

## 五、相关概念区分

表格

|类|区别|
|---|---|
|ProximityPrompt|引擎自带交互提示，自动显示 / 隐藏 / 按键|
|ClickDetector|鼠标点击检测，无距离提示 UI|
|GuiButton|2D UI 按钮，不依附 3D 对象|
|TouchTransmitter|角色触碰触发，无按键提示|

简单记：

**ClickDetector = 点击**

**ProximityPrompt = 靠近按 E**