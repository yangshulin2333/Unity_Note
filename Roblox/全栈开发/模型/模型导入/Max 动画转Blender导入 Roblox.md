 
# 一、整体流程
```text
3ds Max
→ 导出 FBX
→ Blender 导入
→ Blender 再导出 FBX
→ Roblox 导入模型
→ Roblox 动画编辑器导入动画
````

不要：

```text
3ds Max 直接导 Roblox
```

容易动画不识别。

---

# 二、3ds Max 导出 FBX

## 1. 选择角色

包含：

- 模型
    
- 骨骼
    
- 动画
    

---

## 2. 导出

```text
文件
→ 导出选定对象
→ FBX
```

---

## 3. 导出设置

### Geometry

开启：

```text
✔ Smoothing Groups
✔ Tangents and Binormals
✔ Triangulate
```

### Animation

开启：

```text
✔ Animation
✔ Bake Animation
```

### 关闭

```text
❌ Camera
❌ Light
❌ Embed Media
```

导出：

```text
Demo04.fbx
```

---

# 三、Blender 导入 FBX

## 1. 打开 Blender

删除默认物体：

```text
A
Delete
```

---

## 2. 导入 FBX

```text
文件
→ 导入
→ FBX
```

选择：

```text
Demo04.fbx
```

---

## 3. 检查动画

按：

```text
空格
```

如果角色会动，说明动画正常。

---

# 四、Blender 导出 FBX（关键）

## 1. 全选

```text
A
```

---

## 2. 导出

```text
文件
→ 导出
→ FBX
```

---

# 五、Blender 导出设置（最重要）

## Include

只保留：

```text
✔ 骨架
✔ 网格
```

---

## Transform

设置：

```text
Scale = 1.0
Forward = -Z Forward
Up = Y Up
```

开启：

```text
✔ 应用单位
✔ 使用空间变换
```

关闭：

```text
❌ 应用变换
```

---

## Armature

关闭：

```text
❌ Add Leaf Bones
```

---

## Animation

开启：

```text
✔ 动画
✔ 强制开始末处插帧
```

关闭：

```text
❌ NLA Strips
❌ All Actions
```

设置：

```text
Simplify = 0
```

---

## 3. 导出

导出：

```text
Demo05.fbx
```

---

# 六、Roblox 导入模型

## 1. 导入

```text
Home
→ Import 3D
```

选择：

```text
Demo05.fbx
```

---

## 2. 导入设置

开启：

```text
✔ 仅以模型导入
✔ 添加至工作区
```

骨架类型：

```text
自定义
```

---

## 3. 导入完成

Workspace 出现：

```text
Demo05
```

说明成功。

---

# 七、Roblox 导入动画

## 1. 选中模型

选：

```text
Demo05
```

不要选骨骼。

---

## 2. 打开动画编辑器

```text
Avatar 即 虚拟形象
→ Animation Editor 即 剪辑编辑器
```

![](assets/Max%20动画转Blender导入%20Roblox/file-20260507101522614.jpg)
---

## 3. 导入动画

左上：

```text
...
→ 导入
→ 从文件
```

选择：

```text
Demo05.fbx
```

---

## 4. 导入设置

选择：

```text
● 导入的骨架
```

然后：

```text
导入
```

---

# 八、成功标准

成功后：

```text
底部时间轴出现轨道
点击播放人物正常动
```

---

# 九、本次最关键的坑

## 错误做法

```text
Blender 导出 Scale 写 0.025
```

会导致：

```text
人物炸开
```

---

## 正确做法

```text
Blender 导出 FBX：

Scale = 1.0
```

不要二次缩放。

---

# 十、核心记忆

```text
Max 导出
→ Blender 中转
→ Blender 导出 Scale = 1.0
→ Roblox 导入模型
→ Animation Editor 导入动画
```