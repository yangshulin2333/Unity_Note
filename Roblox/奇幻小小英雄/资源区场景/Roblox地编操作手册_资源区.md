# Roblox 地编操作手册：资源区场景

> 参考视频：<https://www.youtube.com/watch?v=0ENeVVC9QT0>  
> 适用项目：《奇幻小小英雄》资源区  
> 目标：把混元生成的资源区参考图，落地成 Roblox Studio 里可传送、可采集、可维护的资源场景。

---

## 1. 你现在要学什么

你不需要一开始学习完整 3D 建模流程。当前阶段只需要掌握 Roblox Studio 的**地编最小闭环**：

```text
Terrain 打地形
-> Part / Model 搭资源区结构
-> 摆放树和矿石
-> 设置碰撞和锚定
-> 按项目目录放 ResourceNodes
-> 设置 ResourceType Attribute
-> 测试传送和采集
```

优先级：

1. **地形编辑**：会做平地、山坡、岩壁、边界。
2. **场景分区**：中心传送营地、左侧伐木区、右侧矿石区。
3. **资源节点摆放**：树和矿石必须按项目结构放到 `ResourceNodes`。
4. **碰撞与动线**：玩家能走、能靠近、不会卡住。
5. **视觉整理**：最后再补灯笼、木桶、矿车、木栅栏。

---

## 2. 混元结果怎么用

混元生成图不要直接等同于最终地图。它的作用是：

- 定整体构图。
- 定美术风格。
- 定资源区氛围。
- 给你参考“哪里放树、哪里放矿、哪里放传送阵”。

当前混元图可以拆成这个布局：

```text
左侧 / 左下：伐木区
中心：传送阵和安全空地
右侧：岩壁矿区
外围：山体、森林、海岸远景
```

在 Roblox Studio 里要更规整一点：

```text
              岩壁 / 矿洞入口
                 RocksArea

TreesArea     TeleportCamp     RocksArea

              玩家活动空地
```

---

## 3. Roblox Studio 操作顺序

### Step 1：准备 Explorer 目录

在 Studio 里确认或创建这些目录：

```text
Workspace
├─ Map
│  └─ ResourceZone
└─ Interactables
   ├─ ResourceNodes
   │  ├─ Trees
   │  └─ Rocks
   └─ Teleporters
      └─ ResourceToCity
```

然后在 `Workspace.Map.ResourceZone` 下创建：

```text
Ground
TeleportCamp
TreesArea
RocksArea
Decorations
Boundaries
```

原则：

- 可采集资源点放 `Workspace.Interactables.ResourceNodes`。
- 纯视觉装饰放 `Workspace.Map.ResourceZone`。
- 不要把装饰树误放进 `ResourceNodes.Trees`，否则采集系统可能把它当成资源点。

---

### Step 2：用 Terrain 做地形底盘

打开：

```text
Studio 顶部栏 -> Home / Model 附近 -> Terrain Editor
```

第一版建议做一个中小型资源区，不要太大：

```text
宽度：180-240 studs
长度：180-240 studs
中心空地：直径 40-60 studs
```

操作建议：

1. 用 `Generate` 或手动工具做基础地形。
2. 用 `Flatten` 压出中心平地。
3. 用 `Sculpt` 拉出右侧岩壁。
4. 用 `Smooth` 把太尖的地方抹平。
5. 用 `Paint` 给区域刷材质：
   - 中心和伐木区：Grass / Ground。
   - 路径：Ground / Pavement。
   - 岩壁和矿区：Rock / Slate / Basalt。

注意：

- Terrain 是体素地形，官方文档说明每格大约是 `4x4x4 studs`，所以细节不要依赖 Terrain 做太碎。
- 中心空地和采集点前方必须平整，否则玩家靠近资源点时容易卡住或提示距离不稳定。

---

### Step 3：搭中心传送营地

在 `Workspace.Map.ResourceZone.TeleportCamp` 下搭：

```text
TeleportPlatform
PortalVisual
Lanterns
Barrels
Crates
Signposts
```

推荐做法：

- 用圆形或八边形石台表示传送阵。
- 中间放蓝色发光 Part 或 Particle 当传送门视觉。
- `ResourceToCity` 放在传送阵旁边，不要藏起来。
- 周围留出 40-60 studs 的空地，玩家传送进来不会挤住。

`ResourceToCity` 注意：

- 它应该在 `Workspace.Interactables.Teleporters.ResourceToCity`。
- 视觉可以放在 `TeleportCamp`，但真正被传送系统识别的交互 Part 要保持命名和目录正确。

---

### Step 4：搭左侧伐木区

先只放 8 棵树测试，不要一开始放满。

可采集树放到：

```text
Workspace.Interactables.ResourceNodes.Trees
```

命名：

```text
Tree_01
Tree_02
Tree_03
...
```

每棵树设置 Attribute：

```text
ResourceType = "Tree"
```

摆放规则：

- 树与树之间保留 8-12 studs。
- 树前方留站位。
- 不要把树贴着墙或贴着其他装饰。
- 树干 `CanCollide = true`，树叶通常 `CanCollide = false`。
- 整棵树或主要 Part 要 `Anchored = true`。

装饰物放到：

```text
Workspace.Map.ResourceZone.TreesArea
```

装饰物包括：

- 树桩。
- 木材堆。
- 倒木。
- 木栅栏。
- 小石头。

第一版推荐数量：

```text
可采集树：20-30
树桩装饰：6-10
木材堆：4-8
木栅栏：按边界需要摆
```

---

### Step 5：搭右侧矿石区

可采集矿石放到：

```text
Workspace.Interactables.ResourceNodes.Rocks
```

命名：

```text
Rock_01
Rock_02
Rock_03
...
```

每个矿石设置 Attribute：

```text
ResourceType = "Rock"
```

摆放规则：

- 矿石靠近岩壁，但前方要留 8-12 studs 站位。
- 矿石不要陷进 Terrain 里太深。
- 矿石之间不要贴得太近。
- 发光水晶可以做装饰，但第一版不要设置成新资源类型。

装饰物放到：

```text
Workspace.Map.ResourceZone.RocksArea
```

装饰物包括：

- 岩壁。
- 矿车。
- 木支架。
- 木桶。
- 箱子。
- 碎石。
- 蓝紫色水晶装饰。

第一版推荐数量：

```text
可采集矿石：8-12
矿车：1-2
木支架：2-4
水晶装饰：3-6
木桶/箱子：4-8
```

---

## 4. 地编核心知识点

### 4.1 Terrain 和 Part 的分工

Terrain 适合：

- 地面。
- 山坡。
- 大岩壁。
- 水面。
- 自然边界。

Part / MeshPart / Model 适合：

- 树。
- 矿石。
- 传送阵。
- 木桶箱子。
- 矿车。
- 木栅栏。
- 可交互资源点。

不要用 Terrain 做每一块矿石，也不要用大量小 Part 拼整座山。

---

### 4.2 可玩地图优先于漂亮地图

资源区判断标准不是“像不像原画”，而是：

- 玩家能不能看懂哪里砍树。
- 玩家能不能看懂哪里挖矿。
- 玩家能不能顺利从中心跑到资源点。
- 多人同时采集时会不会互相卡住。
- 资源点能不能被现有系统识别。

所以第一版要保持清晰：

```text
中心空地大一点
树距大一点
矿石前方空一点
装饰少一点
边界明确一点
```

---

### 4.3 Anchor 和 Collision

常用设置：

```text
地面 / 岩壁 / 树干 / 矿石：Anchored = true
装饰小草 / 树叶 / 细枝：CanCollide = false
隐形边界：Transparency = 1, CanCollide = true, Anchored = true
```

如果忘记 `Anchored`：

- 物体可能掉落。
- 运行时场景散掉。

如果碰撞设置太多：

- 玩家容易卡住。
- 采集时靠近不了资源点。

---

### 4.4 资源节点必须服务端可识别

当前项目已有采集系统，资源点的关键不是模型多漂亮，而是：

```text
目录正确
命名清楚
Attribute 正确
玩家距离合适
```

树：

```text
Workspace.Interactables.ResourceNodes.Trees.Tree_01
ResourceType = "Tree"
```

矿：

```text
Workspace.Interactables.ResourceNodes.Rocks.Rock_01
ResourceType = "Rock"
```

---

## 5. 推荐练习顺序

不要一次做完整大地图。按这个顺序练：

### 练习 A：5 分钟地形

目标：

- 做一块平地。
- 右侧拉一面岩壁。
- 左侧留森林空间。

验收：

- 玩家能从中心跑到左侧和右侧。
- 没有明显卡点。

### 练习 B：中心传送营地

目标：

- 搭一个传送阵。
- 放 `ResourceToCity`。
- 放灯笼、木桶、箱子。

验收：

- 传送点一眼能看到。
- 中心空地不拥挤。

### 练习 C：8 棵树 + 4 个矿

目标：

- 放 8 棵可采集树。
- 放 4 个可采集矿。
- 设置 Attribute。

验收：

- 靠近树显示采集提示。
- 采树增加 Wood。
- 靠近矿显示采集提示。
- 采矿增加 Stone。

### 练习 D：扩展到 MVP 数量

目标：

- 树扩展到 20-30。
- 矿扩展到 8-12。
- 加边界和装饰。

验收：

- 玩家不能跑出资源区。
- 多人采集空间足够。
- 场景不会显得空，但也不拥挤。

---

## 6. 常见错误

### 错误 1：把整个混元场景导入 Roblox 当地图

问题：

- 碰撞不可控。
- 资源点不可维护。
- 模型可能过重。
- 后续交互难做。

正确做法：

```text
混元图当参考
Roblox Studio 里重搭可交互结构
```

### 错误 2：资源点放在视觉目录里

错误：

```text
Workspace.Map.ResourceZone.TreesArea.Tree_01
```

正确：

```text
Workspace.Interactables.ResourceNodes.Trees.Tree_01
```

### 错误 3：忘记设置 ResourceType

树必须：

```text
ResourceType = "Tree"
```

矿必须：

```text
ResourceType = "Rock"
```

### 错误 4：树和矿摆得太密

后果：

- 玩家卡住。
- 多人无法同时采集。
- 采集提示不稳定。

正确：

- 树间距 8-12 studs。
- 矿石前方留 8-12 studs。

### 错误 5：装饰太早做太多

先完成：

```text
传送
采树
采矿
返回
```

再补：

```text
灯笼
木桶
矿车
碎石
栅栏
水晶装饰
```

---

## 7. 最终验收清单

- [ ] 玩家可以从主城传送进资源区。
- [ ] 玩家落点在中心传送营地空地。
- [ ] 玩家可以从资源区返回主城。
- [ ] 左侧一眼看出是伐木区。
- [ ] 右侧一眼看出是矿石区。
- [ ] 可采集树在 `Workspace.Interactables.ResourceNodes.Trees`。
- [ ] 可采集矿在 `Workspace.Interactables.ResourceNodes.Rocks`。
- [ ] 树设置了 `ResourceType = "Tree"`。
- [ ] 矿设置了 `ResourceType = "Rock"`。
- [ ] 采树能增加 Wood。
- [ ] 采矿能增加 Stone。
- [ ] 玩家不会被树、矿、装饰物频繁卡住。
- [ ] 玩家不能轻易跑出资源区。
- [ ] 没有加入草药、蘑菇、怪物、战斗区。

---

## 8. 下一阶段再学

当前阶段先不要急着学这些：

- Blender 深度建模。
- LOD 优化。
- 骨骼动画。
- 复杂粒子。
- 砍树倒下动画。
- 木材掉落拾取。
- 多人贡献奖励分配。

这些是第二阶段内容。第一阶段只要做到：

```text
资源区能进入
树能采
矿能采
资源能加到 HUD
能返回主城
```

就算成功。
