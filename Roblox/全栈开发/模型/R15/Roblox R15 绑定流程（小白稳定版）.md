

目标：

```text
你的模型 → 使用 Roblox 官方 R15 骨架
```

结果：

- Roblox动画直接能用
    
- 摄像机正常
    
- 缩放正常
    
- 不再出现偏移
    

---

# 第一阶段：准备 R15 骨架

---

## 1️⃣ Roblox 导出 R15

Roblox Studio：

```text
插件 → Build Rig → R15
```

生成一个 R15 人物。

---

## 2️⃣ 导出 R15

选中 R15：

```text
文件 → 导出所选内容
```

导出：

```text
R15.fbx
```

---

# 第二阶段：Blender 绑定

---

# 3️⃣ Blender 新建场景

打开 Blender：

```text
文件 → 新建
```

删除默认立方体：

```text
A
X
Delete
```

---

# 4️⃣ 导入 R15

```text
文件 → 导入 → FBX
```

导入：

```text
R15.fbx
```

---

# 5️⃣ 导入你的模型

再次：

```text
文件 → 导入 → FBX
```

导入你的角色。

---

# 6️⃣ 删除你原来的骨架（关键）

右上角层级：

找到：

```text
Bip001
Bip001 Footsteps
Armature
```

这种骨架名字。

---

删除：

```text
右键 → 删除
```

---

# ⚠️ 删除后正常现象

删除后：

```text
模型会站着不动
```

这是正常的。

---

# 第三阶段：对齐模型

---

# 7️⃣ 缩放模型（不是骨架）

只选：

```text
你的Mesh
```

不要选 R15骨架。

---

缩放：

```text
S
```

调大小。

---

# 8️⃣ 移动模型位置

目标：

```text
让模型套在R15身体外面
```

像穿衣服一样。

---

移动：

```text
G
```

旋转：

```text
R
```

---

# ⚠️ 不需要完全精准

只需要：

- 头对头
    
- 手对手
    
- 腿对腿
    

大致重合即可。

---

# 第四阶段：绑定（核心）

---

# 9️⃣ 先选模型

只选：

```text
你的Mesh
```

---

# 🔟 Shift选R15骨架

按住：

```text
Shift
```

再点：

```text
R15 Armature
```

---

# ⚠️ 最终状态

必须：

```text
模型橙色
骨架黄色
```

骨架是最后选中的。

---

# 1️⃣1️⃣ 绑定

按：

```text
Ctrl + P
```

弹菜单。

选择：

```text
With Automatic Weights
```

---

# ✅ 成功表现

现在：

移动骨架：

```text
R
```

模型会跟着动。

---

# 第五阶段：导出

---

# 1️⃣2️⃣ 只选两样

右上角：

只选：

```text
Mesh
R15骨架
```

---

# 1️⃣3️⃣ 导出 FBX

```text
文件 → 导出 → FBX
```

---

# 导出设置（重要）

左边：

---

## ✔ 勾选

```text
Selected Objects
Mesh
Armature
```

---

## ❌ 取消

```text
Bake Animation
Animation
```

先不要动画。

---

# 第六阶段：Roblox 导入

---

# 1️⃣4️⃣ 导入 FBX

拖进 Roblox。

---

# 1️⃣5️⃣ 设置 StarterCharacter

放到：

```text
StarterPlayer
```

重命名：

```text
StarterCharacter
```

---

# 1️⃣6️⃣ 测试

运行游戏。

---

# ✅ 成功后效果

你会得到：

- 正常摄像机
    
- 正常落地
    
- 正常缩放
    
- 正常动画
    

---

# 后续动画怎么办？

以后：

```text
所有动画都基于R15做
```

包括：

- Idle
    
- Run
    
- Attack
    
- Skill
    

全部稳定。

---

# ⚠️ 最容易炸的点（记住）

---

## ❌ 不要再用旧骨架

必须删：

```text
Bip001
Footsteps
```

---

## ❌ 不要同时保留两套骨架

否则必炸。

---

## ❌ 不要绑定前缩放骨架

只缩放：

```text
Mesh
```

---

# 最后一句

你现在正式进入：

```text
Roblox标准角色工作流
```

后面会稳定很多。