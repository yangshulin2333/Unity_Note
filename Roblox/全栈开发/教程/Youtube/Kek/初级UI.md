
# The Ultimate Beginner’s Guide to Roblox GUI 笔记

视频链接：https://www.youtube.com/watch?v=lmNWskz9cEI&t=173s  
主题：Roblox Studio 中 GUI 的基础概念与一个货币 UI 的制作流程

## 1. GUI 是什么

GUI 即 Graphical User Interface，图形用户界面。

在 Roblox 游戏中，GUI 用来让玩家通过视觉元素与游戏功能交互，例如：

- 商店窗口
- 设置面板
- 货币栏
- 按钮
- 图标
- 弹窗界面

几乎所有 Roblox 游戏都会使用 GUI。

## 2. 准备 Roblox Studio

制作 GUI 前需要安装并打开 Roblox Studio。

如果界面和教程不同，可能是因为开启了 Beta 功能。作者建议：

1. 打开 `Beta Features`
2. 找到 `New NextG Studio Preview`
3. 关闭它
4. 保存并重启/刷新界面

## 3. GUI 的主要类型

Roblox 中常见 GUI 有三类：

### ScreenGui

显示在玩家屏幕上的 2D UI。

适合制作：

- 商店
- 货币栏
- 设置界面
- 按钮
- 菜单

本视频主要讲 `ScreenGui`。

### BillboardGui

显示在 3D 世界中，但始终面向摄像机。

常用于：

- NPC 头顶文字
- 血条
- 名字标签

### SurfaceGui

贴在 3D 物体表面上的 GUI。

常用于：

- 屏幕面板
- 墙上的按钮
- 游戏内显示器

## 4. 创建基础 ScreenGui

基本结构：

```text
StarterGui
└── ScreenGui
    └── Frame
```

`StarterGui` 是 GUI 的父级容器，放在这里的界面会显示到玩家屏幕上。

`ScreenGui` 是屏幕 UI 的容器。

`Frame` 是最常用的基础 UI 元素，可以变成：

- 面板
- 背景
- 货币栏
- 商店框
- 按钮容器

## 5. Anchor Point 与 Position

作者建议把 Frame 的锚点设为：

```text
AnchorPoint = 0.5, 0.5
Position = 0.5, 0.5
```

含义：

- `AnchorPoint = 0.5, 0.5`：把对象的中心点作为定位点
- `Position = 0.5, 0.5`：把对象放到屏幕中心

Roblox 的 UI 坐标一般从 `0` 到 `1`：

- X 轴：左边是 `0`，右边是 `1`
- Y 轴：顶部是 `0`，底部是 `1`
- `0.5` 表示中间

## 6. 开启 Device Emulation

作者推荐开启设备模拟功能，用来测试 UI 在不同设备上的显示效果。

原因：

- 玩家可能使用电脑、平板、手机
- 不同分辨率下 UI 可能变形
- 提前测试可以避免 UI 太大、太小或位置错误

## 7. Offset 与 Scale 的区别

### Offset

Offset 使用像素值。

例如：

```text
Size = 555px, 555px
```

问题是：不同设备分辨率不同，像素大小不适配。

在小屏幕上可能显得过大，在大屏幕上可能显得过小。

### Scale

Scale 使用相对比例。

例如：

```text
Size = 0.2, 0.25
```

优点：

- 更适合多设备适配
- UI 在不同分辨率下比例更稳定
- 推荐优先使用 Scale，而不是 Offset

## 8. ZIndex：控制 UI 层级

`ZIndex` 决定哪个 UI 显示在上面。

规则：

```text
ZIndex 数值越大，显示越靠上
```

例子：

```text
Frame A: ZIndex = 1
Frame B: ZIndex = 3
```

结果：Frame B 会显示在 Frame A 上方。

制作复杂 UI 时，按钮、图标、文字经常需要调整 ZIndex。

## 9. 制作货币 UI 的流程

视频中制作了一个类似游戏货币栏的 UI。

基本结构：

```text
ScreenGui
└── Frame
    ├── UI Corner
    ├── UI Gradient
    ├── UI Stroke
    ├── TextLabel
    ├── ImageLabel
    └── ImageButton
```

### Frame

作为货币栏背景。

设置内容包括：

- 调整大小
- 使用 Scale
- 设置位置
- 添加圆角
- 添加渐变
- 添加描边

### UI Corner

用于制作圆角。

推荐使用 Scale，而不是 Offset。

### UI Gradient

用于给 Frame 添加颜色渐变。

可以调整：

- 颜色
- 渐变方向
- Rotation
- Transparency

### UI Stroke

用于给 UI 添加描边。

作者建议设置合适的厚度，并使用 `Scale Size`。

## 10. 添加货币文字

添加 `TextLabel` 显示货币数量，例如：

```text
999.9K
```

常用设置：

```text
AnchorPoint = 0.5, 0.5
Position = 0.5, 0.5
Size = 1, 1
BackgroundTransparency = 1
TextScaled = true
```

其他美化：

- 字体可选 Fredoka、Montserrat 等
- 文字颜色设为白色
- 给文字添加 UI Stroke
- 也可以添加 UI Gradient

## 11. UIAspectRatioConstraint

当 UI 在不同设备上比例不正确时，可以添加：

```text
UIAspectRatioConstraint
```

作用：

- 保持 UI 宽高比例
- 防止不同设备下 UI 被拉伸或压扁
- 帮助文字和背景保持一致布局

作者手动调整了 Aspect Ratio，例如接近：

```text
AspectRatio = 3.65
```

实际项目中可以用插件更精准地转换和调整。

## 12. 制作并导入图标

作者用 Photoshop 演示制作货币图标，但也提到可以使用：

- Figma
- Affinity
- Photopea
- Canva
- Photoshop

流程：

1. 找一个图标素材，例如宝石图标
2. 去除背景
3. 添加描边
4. 缩小预览，检查放到游戏 UI 中是否清晰
5. 导出 PNG
6. 在 Roblox Studio 中打开 `Asset Manager`
7. 上传图片
8. 复制图片 ID
9. 放入 `ImageLabel` 的 Image 属性中

## 13. ImageLabel 的关键设置

导入图片后，添加 `ImageLabel`。

重要设置：

```text
ScaleType = Fit
BackgroundTransparency = 1
Image = 上传图片的 Asset ID
```

`ScaleType = Fit` 可以让图片保持比例，不被拉伸变形。

## 14. 添加加号按钮

作者添加了一个 `ImageButton` 作为加号按钮。

`ImageButton` 是可以点击的图片按钮，也可以不用图片，只当作彩色按钮使用。

设置流程：

1. 添加 `ImageButton`
2. 清空 Image
3. 设置绿色背景
4. 添加 `UI Corner`
5. 添加 `UI Stroke`
6. 调整 ZIndex
7. 在里面添加 `TextLabel`
8. 文字设为 `+`
9. 开启 `TextScaled`
10. 调整字体、颜色、描边

按钮定位示例：

```text
AnchorPoint = 0.5, 0.5
Position = 1, 0.5
```

含义：按钮放在父级 Frame 的最右侧中间位置。

## 15. 多个货币栏的复用

完成一个货币 UI 后，可以复制它并修改：

- Position
- 颜色渐变
- 图标
- 文字内容
- 尺寸

这样可以快速做出多个货币栏，例如：

- 金币
- 宝石
- 钻石
- 点数

## 16. 作者强调的设计思路

UI 设计不只是技术操作，还要理解：

- 什么元素放在哪里
- 图标和文字如何平衡
- 颜色是否协调
- 大小是否合适
- 不同设备是否适配
- 层级是否清晰

作者认为，多练习比记住每个属性更重要。

## 17. 核心建议总结

- 优先使用 `Scale`，少用 `Offset`
- 用 `AnchorPoint = 0.5, 0.5` 更方便居中
- 开启设备模拟，检查不同屏幕效果
- 用 `ZIndex` 控制 UI 前后层级
- 用 `UIAspectRatioConstraint` 保持比例
- 图片要设置 `ScaleType = Fit`
- 用 `UI Corner`、`UI Gradient`、`UI Stroke` 提升视觉效果
- 一个 UI 做好后可以复制复用，快速制作多个界面

## 18. 本视频最终完成的效果

最终制作了一个可缩放、带图标、文字和加号按钮的 Roblox 货币 UI。

这个方法也可以扩展到其他界面，例如：

- 商店 UI
- 设置 UI
- 兑换码 UI
- 背包 UI
- 菜单 UI
- 任务界面
```

注：以上笔记基于该视频的英文自动字幕整理，个别术语按 Roblox Studio 常用中文理解翻译。