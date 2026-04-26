下面是这个视频 **“Roblox UI Importing Masterclass”** 的详细学习笔记。这个视频是上一期 Roblox GUI 基础的进阶版，重点讲 **如何把 Photoshop / Figma / Affinity / Photopea 等软件里设计好的 UI 正确导入 Roblox Studio，并让它可缩放、可交互、可脚本化**。


# Roblox UI Importing Masterclass 学习笔记

视频链接：https://www.youtube.com/watch?v=_6v86vc-9Xc  
作者：Kek / Kakuza  
主题：Roblox UI 导入完整流程

## 1. 什么是 UI Importing

UI Importing 指的是：

> 把第三方设计软件里做好的 UI 元素导出成图片，再导入 Roblox Studio，并在 Studio 中重新搭建成可用的 GUI。

常见设计软件包括：

- Photoshop
- Figma
- Affinity Designer / Photo
- Photopea
- Canva

重点不是“从哪个软件导出”，而是：

> 一旦你已经拿到了 PNG 图片，导入 Roblox Studio 的逻辑基本都是一样的。

也就是说：

- 导出流程因软件而异
- 导入流程基本一致
- Roblox Studio 里要重新搭建层级、尺寸、按钮、文字和交互

## 2. 导入 UI 的核心原则

### 2.1 使用 PNG，不使用 JPG

导入 UI 时推荐全部使用 PNG。

原因：

- PNG 支持透明背景
- JPG 不支持透明背景
- PNG 更适合 UI 图标、按钮、边框、发光效果
- JPG 会压缩画质，不适合精细 UI

例如一个圆形按钮：

- PNG：圆外面的四个角可以透明
- JPG：透明区域会变成黑色、白色或灰色背景

### 2.2 不要把普通文字导出成图片

一般情况下，不要把文字导出成 PNG。

原因：

- 导出成图片后，文字不能在 Roblox Studio 中修改
- 不能方便地脚本更新
- 不能适配不同语言
- 不能动态显示数值

应该在 Roblox Studio 里用：

- `TextLabel`
- `TextButton`
- `TextBox`

例外情况：

如果某些文字用了 Roblox 没有的特殊字体、特殊扭曲或复杂效果，并且以后不需要修改，可以把它 rasterize 后导出成图片。

### 2.3 图片尺寸不要超过 1024x1024

Roblox 会对过大的图片进行压缩或缩小。

作者建议：

```text
单张图片尽量控制在 1024 x 1024 以下
```

如果是很大的 UI，不要整张导出。

更好的做法：

- 分成多个小图
- 背景、按钮、图标、发光层分别导出
- 在 Roblox Studio 中重新拼起来

### 2.4 导入素材不要用主账号

作者强烈建议：

> 上传图片、音效、贴图等资源时，不要使用 Roblox 主账号。

原因是 Roblox 审核机制有时会误判素材，可能导致账号被警告、封禁或资源被删除。

建议做法：

- 准备一个小号
- 用小号上传 UI 图片资源
- 主账号继续开发游戏

## 3. Photoshop 导出 UI 的方法

### 3.1 合并不需要单独控制的图层

如果一个 UI 元素由多个图层组成，但在 Roblox 中不需要分别控制，就应该合并后导出。

例如 Header 由这些组成：

- 背景色
- 渐变
- 纹理
- 装饰图案

如果这些东西以后不会单独动，就可以合并成一张图片：

```text
Header Background
```

操作流程：

1. 隐藏文字图层
2. 选中背景、纹理、渐变等图层
3. `Ctrl + E` 合并图层
4. 重命名为 `header_bg`
5. Quick Export as PNG

### 3.2 发光效果要单独导出

如果按钮有 Glow / Outer Glow，不建议和按钮本体强行合并。

推荐分开导出：

```text
cross_button.png
cross_button_glow.png
```

这样在 Roblox Studio 中可以：

- 单独调 glow 颜色
- 单独调透明度
- 做 hover 动画
- 改变发光强度

Photoshop 中可以：

1. 右键带有 glow 的图层
2. `Create Layer`
3. 把 glow 分离成独立图层
4. 单独导出 PNG

### 3.3 有 Mask 的图层要先 Apply Mask

如果图层用了蒙版，导出前需要确认效果是否已经应用。

操作：

```text
Right Click Mask -> Apply Layer Mask
```

否则导出的结果可能和设计稿不一致。

## 4. Figma 导出 UI 的方法

### 4.1 隐藏文字，只导出非文字元素

在 Figma 中同样遵循：

```text
文字尽量不导出
背景、按钮、图标、装饰单独导出
```

例如一个背包 UI：

- 主背景单独导出
- 物品格子单独导出
- 按钮背景单独导出
- 图标单独导出
- 文字在 Roblox Studio 里重做

### 4.2 Figma 导出 PNG

流程：

1. 选中要导出的 Group / Frame
2. 右下角找到 Export
3. 格式选择 PNG
4. 倍率一般选择 `1x`
5. 点击 Export

### 4.3 Figma 中制作 Glow

作者讲了两种方式：

#### 方法一：Drop Shadow

1. 复制原按钮形状
2. 放到按钮下面
3. 添加 Drop Shadow
4. Y 设为 0
5. Blur 增大
6. Spread 增大
7. 调整颜色和透明度

#### 方法二：Layer Blur

作者更推荐这种。

1. 复制形状
2. 放到底层
3. 使用 Layer Blur
4. 去掉 Stroke
5. 保留 Fill
6. 需要更强 glow 时复制多层
7. Group 后导出 PNG

## 5. Affinity 导出 UI 的方法

Affinity 的逻辑和 Photoshop 类似。

常见操作：

- 隐藏文字
- 选中需要导出的 UI 元素
- 如果有效果，先 rasterize
- 导出 PNG

如果要导出 Glow：

1. 给元素添加 Outer Glow
2. 隐藏 Stroke
3. 把 Fill 改成白色
4. 导出成 PNG
5. 到 Roblox Studio 里用 `ImageColor3` 改颜色

这样更灵活。

## 6. Photopea 导出 UI 的方法

作者不太推荐 Photopea，因为流程较繁琐。

可用方法：

### 方法一：Smart Object

1. 合并图层
2. Convert to Smart Object
3. 双击 Smart Object
4. 在新文件中 Export as PNG

### 方法二：Export Layers

可以批量导出图层，但容易遇到：

- 文字图层也被导出
- Mask 处理麻烦
- Blending Options 结果不稳定
- 命名和筛选麻烦

所以作者认为 Photopea 可以用，但不够顺手。

## 7. 在 Roblox Studio 上传图片

### 方法一：Asset Manager

流程：

1. 打开 Roblox Studio
2. 打开 `Asset Manager`
3. 进入 Images
4. 点击 Bulk Import
5. 选择一个或多个 PNG
6. 上传完成后，右键图片
7. `Copy ID to Clipboard`

然后把 ID 填进 `ImageLabel.Image` 或 `ImageButton.Image`。

### 方法二：Creator Hub 上传 Decal

流程：

1. 打开 `create.roblox.com`
2. 进入 Creations
3. Development Items
4. Decals
5. Upload Asset
6. 上传 PNG
7. 上传后复制 Asset ID

注意：

Roblox 有时把图片作为 Decal 管理，但复制出来的 ID 仍然可以用于 UI 图片。

## 8. Roblox GUI 类型复习

### 8.1 ScreenGui

用于屏幕上的 2D UI。

必须放在：

```text
StarterGui
```

常用属性：

- `Enabled`：是否显示
- `DisplayOrder`：多个 ScreenGui 的显示层级
- `IgnoreGuiInset`：是否忽略 Roblox 默认顶部栏区域
- `ResetOnSpawn`：玩家重生时是否重置
- `ScreenInsets`：移动端安全区域相关
- `ZIndexBehavior`：通常保持 `Sibling`

### 8.2 BillboardGui

显示在 3D 世界中，并且通常面向摄像机。

常见用途：

- NPC 名字
- 血条
- 头顶提示

重要属性：

- `AlwaysOnTop`
- `LightInfluence`
- `MaxDistance`
- `StudsOffset`
- `ClipDescendants`

### 8.3 SurfaceGui

贴在 Part 表面上的 UI。

常见用途：

- 游戏内屏幕
- 墙上的按钮
- 机器控制面板

重要属性：

- `Adornee`
- `Face`
- `PixelsPerStud`
- `AlwaysOnTop`
- `LightInfluence`

## 9. GUI 层级 Hierarchy

导入 UI 时，层级非常重要。

基本结构示例：

```text
StarterGui
└── ScreenGui
    └── HolderFrame
        └── ContainerFrame
            ├── MainInventory
            └── InventoryDetails
```

原则：

- 大 UI 外面套一个总容器 `ContainerFrame`
- 左右区域可以拆成不同 Frame
- 按钮、图标、文字放在对应父级里
- 需要一起移动/缩放的元素放在同一个容器里

这样更方便：

- 动画
- 脚本控制
- 缩放适配
- 批量隐藏/显示

## 10. 常见 GUI 对象

### 10.1 Frame

Frame 是最基础的 UI 容器。

常用来放：

- 背景
- 面板
- 容器
- 列表项
- 按钮底板

重要属性：

- `AnchorPoint`
- `Position`
- `Size`
- `BackgroundColor3`
- `BackgroundTransparency`
- `Visible`
- `ZIndex`
- `ClipDescendants`
- `AutomaticSize`

### 10.2 TextLabel

用于显示文字。

重要属性：

- `Text`
- `FontFace`
- `TextColor3`
- `TextScaled`
- `TextWrapped`
- `RichText`
- `TextXAlignment`
- `TextYAlignment`
- `LineHeight`

作者建议通常开启：

```text
TextScaled = true
```

### 10.3 ImageLabel

用于显示图片。

重要属性：

- `Image`
- `ImageColor3`
- `ImageTransparency`
- `ScaleType`
- `ResampleMode`
- `ImageRectOffset`
- `ImageRectSize`

导入 UI 时最重要的是：

```text
ScaleType = Fit
```

这样图片不会被拉伸变形。

### 10.4 TextBox

可输入文字的 UI。

常用于：

- 搜索框
- 输入兑换码
- 聊天框
- 用户名输入

重要属性：

- `PlaceholderText`
- `PlaceholderColor3`
- `ClearTextOnFocus`
- `MultiLine`
- `TextEditable`

### 10.5 TextButton / ImageButton

按钮类型。

`TextButton`：带文字的按钮  
`ImageButton`：带图片的按钮

重要属性：

- `AutoButtonColor`
- `HoverImage`
- `PressedImage`
- `HoverHapticEffect`
- `PressHapticEffect`

如果要自己做动画，通常可以关闭：

```text
AutoButtonColor = false
```

### 10.6 CanvasGroup

CanvasGroup 可以整体控制内部元素透明度，也能裁切圆角。

但作者不推荐滥用。

原因：

- 性能消耗比 Frame 高
- 内部元素越多越吃资源
- 可能影响游戏性能

适合特殊情况，不适合到处使用。

### 10.7 ViewportFrame

ViewportFrame 可以在 UI 中显示 3D 模型。

常见用途：

- 展示角色
- 展示宠物
- 展示武器
- 展示塔防单位

基本流程：

1. 创建 ViewportFrame
2. 放入模型
3. 放入 Camera
4. 设置 `CurrentCamera`
5. 调整 Lighting / Ambient

如果人物边缘有奇怪描边，可以调整背景颜色，例如灰色，减轻边缘问题。

### 10.8 ScrollingFrame

可滚动容器。

常用于：

- 背包
- 商店
- 单位列表
- 任务列表
- Battle Pass

重要属性：

- `AutomaticCanvasSize`
- `CanvasSize`
- `CanvasPosition`
- `ScrollingDirection`
- `ScrollBarThickness`
- `ScrollBarImageColor3`
- `VerticalScrollBarPosition`

如果内容高度自动变化，推荐：

```text
AutomaticCanvasSize = Y
CanvasSize = 0, 0
```

## 11. UI 组件与约束

### 11.1 UICorner

用于圆角。

例如：

```text
CornerRadius = 0.2, 0
```

如果要做圆形，通常可以设为：

```text
CornerRadius = 1, 0
```

或 `0.5`，效果类似。

### 11.2 UIStroke

用于描边。

常用属性：

- `Color`
- `Thickness`
- `Transparency`
- `ApplyStrokeMode`
- `StrokeSizingMode`
- `LineJoinMode`
- `ZIndex`

作者建议：

```text
StrokeSizingMode = Scale
```

这样描边可以随屏幕缩放。

`ApplyStrokeMode`：

- `Contextual`：给文字或对象内容加描边
- `Border`：给对象边界加描边

多个 UIStroke 可以叠加，用不同 ZIndex 做多层描边。

### 11.3 UIPadding

用于给子元素留边距。

作者不太推荐过度使用，因为可能影响动画和布局。

更推荐：

> 一开始就把 UI 元素布局摆好。

### 11.4 UIScale

用于整体缩放。

常见用途：

- Hover 放大
- 点击缩小
- 弹窗出现动画
- 按钮 bounce 动画

如果希望从中心缩放，应设置：

```text
AnchorPoint = 0.5, 0.5
```

### 11.5 UIAspectRatioConstraint

用于保持宽高比例。

非常重要。

作用：

```text
防止 UI 在不同分辨率下被拉伸或压扁
```

作者强调：

> 不要给所有元素都加 AspectRatioConstraint。

正确做法通常是：

- 给主要容器加
- 不要给全屏 HolderFrame 加
- 不要乱加到每个小元素上

例如：

```text
HolderFrame        不加
└── ContainerFrame 加 AspectRatioConstraint
    ├── LeftPanel
    └── RightPanel
```

### 11.6 UIGradient

用于渐变颜色或透明度。

用途：

- 背景渐变
- 按钮颜色
- 文字渐变
- 发光颜色
- 透明淡出效果
- 进度条遮罩

重要属性：

- `Color`
- `Transparency`
- `Offset`
- `Rotation`

`Offset` 可以用来做扫光动画。

## 12. Layout 布局系统

### 12.1 UIListLayout

把子元素按顺序排成一列或一行。

适合：

- 菜单列表
- 竖向按钮
- 横向按钮组
- 简单物品列表

重要属性：

- `FillDirection`
- `Padding`
- `SortOrder`
- `HorizontalAlignment`
- `VerticalAlignment`
- `Wraps`

注意：

一旦使用 Layout，就不能手动控制子元素 Position。

如果要动画，可以用：

```text
Placeholder Frame
└── 真正内容
```

让 Layout 控制占位 Frame，再动画里面的内容。

### 12.2 UIGridLayout

把子元素排列成网格。

适合：

- 背包
- 商店商品
- 塔防单位
- 卡牌列表

重要属性：

- `CellSize`
- `CellPadding`
- `FillDirection`
- `FillDirectionMaxCells`
- `StartCorner`
- `SortOrder`

UIGridLayout 比 UIListLayout 更适合规则网格，但动画管理会更麻烦。

### 12.3 UIPageLayout

把每个子元素当成页面切换。

适合：

- 页面轮播
- 教程页
- 横向翻页界面

但作者说现在用得比较少，很多人会自己用 Tween 动画实现。

### 12.4 UITableLayout

作者基本不推荐。

它类似表格布局，但现在很少用于现代 Roblox UI。

## 13. Grayscale 灰度导入

Grayscale 是导入 UI 时很重要的技巧。

意思是：

> 把图标或发光图导出成纯白/黑灰图，然后在 Roblox Studio 里用 ImageColor3 改颜色。

好处：

- 一个素材可以变成很多颜色
- 可以做 hover 变色
- 可以用 UIGradient 上色
- 更适合动态 UI

错误做法：

```text
把红色图标直接导入，然后尝试改成绿色
```

这样颜色会很怪，因为 Roblox 的着色类似 Multiply 混合。

正确做法：

1. 在设计软件里把图标变成白色
2. 确保白色是纯白 `#FFFFFF`
3. 导出 PNG
4. Roblox 中用 `ImageColor3` 改颜色

Photoshop 中可用：

```text
Image -> Adjustments -> Desaturate
Image -> Adjustments -> Levels
```

注意：仅仅 Desaturate 不够，因为会变成灰色，不是纯白。

## 14. Hitbox 点击区域

有时 UI 看起来是按钮，但本体是 `ImageLabel`，不能点击。

解决方法是添加一个透明 `ImageButton` 作为 Hitbox。

结构示例：

```text
ImageLabel
└── Hitbox ImageButton
```

Hitbox 设置：

```text
BackgroundTransparency = 1
ImageTransparency = 1
Size = 需要点击的区域大小
```

用途：

- 给复杂图标加点击区域
- 不影响视觉
- 方便脚本绑定点击事件

## 15. 正确添加 Aspect Ratio 的方法

作者特别强调一个常见错误：

```text
给所有东西都加 UIAspectRatioConstraint
```

这是错误的。

尤其不要给全屏主框加固定比例，否则在手机、方屏、宽屏上会出现空白边。

推荐结构：

```text
ScreenGui
└── HolderFrame        # 全屏，Size = 1,1，不加 AspectRatio
    └── ContainerFrame # 包住实际 UI，加 AspectRatio
        ├── LeftFrame
        └── RightFrame
```

原则：

- Holder 负责占满屏幕
- Container 负责保持 UI 比例
- 子元素尽量用 Scale
- 不要乱加约束

## 16. ScrollingFrame 的淡出效果

如果列表滚动到顶部/底部直接切断，看起来很生硬。

作者推荐：

```text
在 ScrollingFrame 上方盖一个 Frame + UIGradient
```

流程：

1. 在 Holder 中添加一个 Frame
2. 放在 ScrollingFrame 上方或下方
3. 设置颜色和背景一致
4. 添加 UIGradient
5. 用 Transparency 做渐隐
6. 调整 Rotation，例如 `-90`

不要为了这个效果滥用 CanvasGroup，因为 CanvasGroup 性能开销更高。

## 17. 导入进度条 / 血条

如果导入了一张血条图片，不要直接横向缩放图片。

错误做法：

```text
改变 Size.X 让血条变短
```

这样可能导致图片拉伸、边缘变形。

推荐做法：

```text
用 UIGradient 的 Transparency 控制显示区域
```

流程：

1. 血条图片使用 `ImageLabel`
2. `ScaleType = Fit`
3. 添加 `UIGradient`
4. 设置 Transparency：
   - 一边可见
   - 一边透明
5. 用 `Offset` 控制可见长度

这样适合：

- HP Bar
- Boss HP
- 能量条
- 经验条

## 18. Slice 九宫格缩放

Slice 是 Roblox 很强的图片缩放功能。

适合：

- 按钮背景
- 长条进度条
- 面板边框
- Loading Bar

它的作用是：

> 只拉伸中间区域，保留边缘和角落不变形。

常用于有圆角或复杂边框的图片。

设置位置：

```text
ImageLabel / ImageButton
ScaleType = Slice
SliceCenter = ...
```

这样按钮可以变长变短，但两边圆角不变形。

## 19. 圆形进度条实现思路

作者展示了一个圆形进度条。

大致结构：

```text
Container
├── BottomCircle
├── LeftMask
│   └── LeftProgress
├── RightMask
│   └── RightProgress
├── TopCircle
└── TextLabel
```

关键点：

- Container 是正方形，并加 AspectRatioConstraint
- 底层是一个圆形底圈
- 左右各一半，用 `ClipDescendants` 裁切
- 用 UIGradient 的 Rotation 控制进度
- TopCircle 盖在上方制造完整圆环效果
- ZIndex 必须正确：
  - Bottom 最低
  - Left/Right 中间
  - Top 最高

这个逻辑需要脚本配合，手动调只能做演示。

## 20. KUI 插件

作者使用自己做的 KUI 插件辅助导入。

插件主要功能：

### 20.1 Scale / Offset 转换

Roblox UI 有两套值：

```text
Scale
Offset
```

Offset 是像素，Scale 是比例。

导入 UI 时，最终应该尽量转成 Scale。

KUI 可以一键转换：

- Size
- Position
- UIStroke Thickness
- UICorner Radius
- Layout Padding
- Grid CellSize
- CanvasSize

### 20.2 Anchor / Position 快速定位

插件提供九宫格按钮，可以快速设置：

- 左上
- 上中
- 右上
- 左中
- 中心
- 右中
- 左下
- 下中
- 右下

可以只改 AnchorPoint，不改 Position。

这很重要，因为：

> 锚点错误会让动画和缩放很难处理。

作者推荐多数 UI 使用：

```text
AnchorPoint = 0.5, 0.5
```

### 20.3 Quick Actions 快捷操作

常用快捷操作包括：

- Center
- Fit to Parent Size
- Remove Background
- Enable TextScaled
- Fixed Aspect Ratio
- Ultra Scale

### 20.4 Fixed Aspect Ratio

这个功能会自动给当前 UI 加 `UIAspectRatioConstraint`，并保持当前形状不变。

比手动试比例快很多。

### 20.5 Ultra Scale

这是作者最强调的功能。

作用：

```text
把一个父级下面所有子元素的 Offset 转成 Scale
```

包括：

- Position
- Size
- UIStroke
- UICorner
- CanvasSize
- Layout Padding
- Grid CellSize

适合导入完成后整体修正。

### 20.6 Reclass

Reclass 可以把一个对象转换成另一个对象。

例如：

```text
Frame -> ScrollingFrame
Frame -> ImageButton
ImageLabel -> ImageButton
TextLabel -> TextBox
```

注意：

作者建议 Reclass 后不要直接 Ctrl+Z，有时可能出问题。需要改回去时，用 Reclass 转回原类型更安全。

### 20.7 Preset UI Gradients

KUI 内置一些常用渐变。

使用建议：

- 先把 Frame 颜色设为白色
- 再应用 Gradient
- 切换 Gradient 时会自动替换旧 Gradient

## 21. 实际导入一个 Inventory UI 的流程

作者后半段演示了完整导入一个背包 UI。

### 21.1 先上传所有 PNG

流程：

1. 换到小号
2. 打开 Asset Manager
3. Bulk Import
4. 全选导出的 PNG
5. 上传
6. 后续逐个复制 Asset ID 使用

### 21.2 创建 ScreenGui

```text
StarterGui
└── ScreenGui
```

推荐设置：

```text
IgnoreGuiInset = true
ResetOnSpawn = false
```

### 21.3 创建 HolderFrame

HolderFrame 占满全屏。

设置：

```text
AnchorPoint = 0.5, 0.5
Position = 0.5, 0.5
Size = 1, 1
BackgroundTransparency = 1
```

作用：

- 作为全屏容器
- 不加 AspectRatioConstraint

### 21.4 放入 Overview 参考图

作者把完整 UI 截图作为 `overview` 放进去，用来对齐。

```text
HolderFrame
└── Overview ImageLabel
```

设置：

```text
ZIndex = -50 或临时设高
ImageTransparency = 0.5
ScaleType = Fit
```

作用：

- 当作参考底图
- 后续所有元素都对着它摆
- 摆完后可以隐藏或删除

### 21.5 创建 ContainerFrame

ContainerFrame 包住实际 UI。

```text
HolderFrame
└── ContainerFrame
```

设置：

- 中心定位
- 背景透明
- 大小覆盖整个实际 UI
- 添加 `UIAspectRatioConstraint`

这是实际 UI 的主容器。

### 21.6 分成左右两个区域

示例：

```text
ContainerFrame
├── MainInventory
└── InventoryDetails
```

左边是背包列表，右边是选中单位详情。

好处：

- 层级清晰
- 方便动画
- 方便脚本控制
- 左右 UI 不互相干扰

### 21.7 导入 Header

Header 是图片，所以用 `ImageLabel`。

设置：

```text
ScaleType = Fit
BackgroundTransparency = 1
ZIndex = 10
```

Header 里的文字用 `TextLabel` 重做。

文字设置：

- `TextScaled = true`
- 字体 Fredoka / Montserrat
- 添加 UIStroke
- Size 和 Stroke 都转 Scale

### 21.8 导入背景

背景通常也是 ImageLabel。

设置：

```text
Name = Background
ZIndex = -10
ScaleType = Fit
```

### 21.9 Close Button 的正确结构

如果按钮需要点击，不应该只用 ImageLabel。

推荐结构：

```text
CloseButton ImageButton
└── Texture ImageLabel
```

ImageButton 负责点击区域。  
Texture ImageLabel 负责显示图片。

好处：

- 点击区域可以单独调
- 图标大小可以单独调
- Hover / Press 动画更方便
- 不会让 glow 区域也变成可点击范围

### 21.10 Search Bar

搜索框结构：

```text
SearchBar Frame
├── UIStroke
├── UICorner
├── SearchIcon ImageLabel
└── SearchBox TextBox
```

SearchBox 设置：

```text
PlaceholderText = Search
TextScaled = true
TextXAlignment = Left
BackgroundTransparency = 1
```

搜索图标：

```text
ScaleType = Fit
ImageTransparency 可调
```

### 21.11 Filter / Lock 按钮组

按钮组使用 UIListLayout 横向排列。

结构：

```text
ExtraButtons Frame
├── UIListLayout
├── FilterButton ImageButton
│   ├── Texture ImageLabel
│   └── Glow ImageLabel
└── LockButton ImageButton
    ├── Texture ImageLabel
    └── Glow ImageLabel
```

注意：

- 按钮本体 `ImageTransparency = 1`
- Texture 显示按钮图
- Glow 放下面，ZIndex 较低
- 不要乱开 `ClipDescendants`，否则 glow 会被裁掉

### 21.12 Unit Capacity 文字

比如：

```text
49 / 100
```

如果想让 `49` 和 `/100` 不同颜色，可以开启：

```text
RichText = true
```

格式类似：

```html
<font color="#HEX颜色">49</font>/100
```

## 22. 背包网格 ScrollingFrame

### 22.1 创建 UnitsHolder

先做一个外框：

```text
UnitsHolder Frame
└── ScrollingFrame
```

UnitsHolder 有：

- UICorner
- UIStroke
- 黑色背景

### 22.2 ScrollingFrame 设置

推荐：

```text
BackgroundTransparency = 1
ScrollingDirection = Y
AutomaticCanvasSize = Y
CanvasSize = 0, 0
```

用 `UIGridLayout` 管理单位卡片。

### 22.3 UIGridLayout 设置

重要属性：

- `CellSize`
- `CellPadding`
- `FillDirectionMaxCells`
- `SortOrder`

作者一开始把一行数量看错，后来修正成一行 6 个卡片。

### 22.4 Glow 被裁切的问题

如果单位卡片的 glow 超出了 Unit Frame 的边界，ScrollingFrame 会裁掉它。

解决方法不是加 Padding，而是：

> 让 Unit Frame 的尺寸包含 glow，然后把内部卡片缩小。

结构：

```text
Unit ImageButton
├── CardGlow
├── CardSelected
├── CardBG
├── ViewportFrame
├── Level TextLabel
├── UnitName TextLabel
├── Traits
└── AccessIcons
```

Unit 外框要足够大，保证 glow 在里面。

## 23. 单位卡片结构

作者制作了一个塔防/背包风格的单位卡片。

### 23.1 Card Background

```text
CardBG ImageLabel
ZIndex = 0
ScaleType = Fit
```

### 23.2 Card Glow

```text
CardGlow ImageLabel
ZIndex = -1
ImageColor3 = 可调颜色
ImageTransparency = 可调透明度
```

如果 glow 是白色导入，可以在 Studio 中自由改颜色。

### 23.3 ViewportFrame

用来显示 3D 单位模型。

```text
ViewportFrame
ZIndex = 1
```

### 23.4 Level / Name

使用 TextLabel。

例如：

```text
LV25
Executioner
```

设置：

- `TextScaled = true`
- `TextColor3`
- `UIStroke`
- `ZIndex` 高于背景和 ViewportFrame

### 23.5 Traits

Traits 应该用 UIListLayout，因为单位特性可能动态变化。

结构：

```text
Traits Frame
├── UIListLayout
├── TraitIcon1
└── TraitIcon2
```

这样以后脚本可以动态添加、删除、排序。

### 23.6 Access Icons

例如：

- 已装备
- 已锁定
- 收藏

可以用 ImageLabel 或 ImageButton，取决于是否需要点击。

### 23.7 卡片要能被点击

如果单位卡片需要选择，就应该把 Unit 转成：

```text
ImageButton
```

而不是普通 Frame。

可以用 KUI 的 Reclass 快速转换。

## 24. 导入 UI 的完整工作流总结

推荐流程：

1. 在设计软件中整理图层
2. 隐藏普通文字
3. 合并不需要单独控制的装饰层
4. 发光、按钮、背景、图标分开导出
5. 使用 PNG
6. 图片尺寸控制在 1024x1024 以内
7. 用小号上传资源
8. 在 Roblox Studio 中创建 ScreenGui
9. 创建 HolderFrame
10. 放入 Overview 参考图
11. 创建 ContainerFrame
12. 给 ContainerFrame 加 AspectRatioConstraint
13. 按区域拆分 Frame
14. 用 ImageLabel / TextLabel / TextBox / ImageButton 重建 UI
15. 所有图片设置 ScaleType = Fit
16. 所有尺寸尽量转 Scale
17. 检查 ZIndex
18. 检查不同设备分辨率
19. 用 Device Emulator 测试 1080p、VGA、iPhone
20. 最后隐藏或删除 Overview

## 25. 作者反复强调的重点

### 25.1 Importing 不是把整张图塞进 Roblox

正确导入不是：

```text
整张 UI 导出成一张 PNG，然后放进 Studio
```

而是：

```text
把 UI 拆成可复用、可交互、可脚本控制的元素
```

### 25.2 要为脚本和动画考虑

UI 不是只要看起来像就行。

还要考虑：

- 按钮能不能点
- 文本能不能变
- 数值能不能动态更新
- 卡片能不能复制
- 滚动列表能不能自动扩展
- Hover 动画是否正常
- 点击区域是否合理

### 25.3 Scale 比 Offset 更重要

Offset 是像素，会导致不同设备错位。

导入完成后应尽量：

```text
Position 使用 Scale
Size 使用 Scale
Stroke 使用 Scale
Corner 使用 Scale
Padding 使用 Scale
CanvasSize 使用 Scale
```

### 25.4 AnchorPoint 很重要

作者建议多数可动画对象用：

```text
AnchorPoint = 0.5, 0.5
```

这样缩放、弹出、hover 动画都会更自然。

### 25.5 一定要测试不同设备

推荐测试：

- 1920x1080
- VGA
- iPhone 14 Pro
- 平板
- 其他移动设备

不要只在一种分辨率下看起来正常。

## 26. 学习路线建议

如果你要真正学会这个视频内容，可以按这个顺序练：

### 第一阶段：基础属性

先熟悉：

- Frame
- TextLabel
- ImageLabel
- ImageButton
- TextBox
- UICorner
- UIStroke
- UIGradient
- UIAspectRatioConstraint

### 第二阶段：导出素材

练习从 Figma 或 Photoshop 导出：

- 一个按钮
- 一个背景
- 一个图标
- 一个 glow
- 一个 header

### 第三阶段：Studio 重建

在 Roblox Studio 中重新搭：

- ScreenGui
- HolderFrame
- ContainerFrame
- Header
- Button
- Search Bar
- Scroll List

### 第四阶段：适配

重点练：

- Scale
- AnchorPoint
- AspectRatioConstraint
- Device Emulator

### 第五阶段：可交互 UI

练：

- ImageButton
- Hitbox
- TextBox
- ScrollingFrame
- UIGridLayout
- ViewportFrame

## 27. 最重要的一句话

> UI 导入的本质不是“搬图片”，而是把设计稿拆解成 Roblox 可以理解、可以缩放、可以交互、可以脚本控制的 GUI 结构。
```

这个视频比上一期难很多，核心是“设计稿到 Roblox Studio 的工程化还原”。你如果要跟着学，建议不要一上来做完整背包 UI，先做一个小练习：**一个带图标、文字、发光和点击区域的按钮**。把这个做顺了，再做搜索框、滚动列表和单位卡片。