
# 🛠️ 3ds Max 至 Roblox Studio 资源导入指南

## 一、 3ds Max 导出前置准备

在导出 FBX 之前，请务必检查以下几项，以确保模型在 Roblox 引擎中表现正常。

1. **单位设置 (Units)**
    
    - **设置：** `Customize > Units Setup > System Unit Setup` 设置为 **Centimeters**。
        
    - **原因：** Roblox 的 1 Stud 约等于 28cm，使用厘米作为系统单位能保证 1:1 的导入比例。
        
2. **重置变换 (Reset XForm)**
    
    - **操作：** 选中模型，在工具栏选择 `Utilities (小锤子) > Reset XForm > Reset Selected`。
        
    - **后续：** 回到修改器列表（Modify），右键点击 `XForm` 并选择 `Collapse All`。
        
    - **目的：** 清除模型在 Max 里的缩放、旋转偏差，防止导入后出现“模型巨大”或“轴心偏移”。
        
3. **坐标原点 (Pivot)**
    
    - 确保模型在 3ds Max 的世界坐标 **(0,0,0)** 处。
        

---

## 二、 贴图格式规范

Roblox 目前对贴图格式有特定要求，不合规的格式会导致导入失败或显示异常。

- **推荐格式：** `.png` (支持透明通道) 或 `.jpg`。
    
- **不建议格式：** `.tga`, `.gif`, `.tiff` (Studio 3D Importer 会弹出兼容性警告)。
    
- **处理流程：**
    
    1. 在 XnConvert 或工具中将 `.tga` 贴图另存为 `.png`。
        
    2. 在 3ds Max 材质球中重新指定新格式贴图。
        

---

## 三、 FBX 导出参数设置 (标准模板)

在 `Export Selected` 弹出框中，按照以下标准配置：

|**模块**|**设置项**|**建议状态**|**备注**|
|---|---|---|---|
|**Geometry**|Smoothing Groups|**勾选**|保留平滑组信息，防止模型变“块状”|
||Triangulate|**勾选**|强制三角化，避免导入后拓扑错误|
||Tangents and Binormals|**取消勾选**|Roblox 会自动计算，勾选可能导致光影错乱|
|**Animation**|Animation|根据需求|若无动画请关闭以减小体积|
|**Units**|Automatic|**取消勾选**|手动指定为 **Centimeters**|
|**Axis**|Up Axis|**Y-Up**|确保模型不会“躺在”地上|
|**Embed Media**|Embed Media|建议勾选|可将贴图路径打包入 FBX (若报错可改为手动上传)|

---

## 四、 Roblox Studio 导入与优化

使用 **3D Importer** (位于 `Avatar` 或 `View` 选项卡) 进行导入。

### 1. 导入检查

- **Scale (缩放)：** 如果模型太大，检查导入面板中的 `File Units` 是否正确识别。
    
- **Texture (材质)：** 如果模型变白，在 `Properties` 面板找到 `TextureID`，点击并上传对应的 `.png` 文件。
    

### 2. 轴心校正 (Pivot Correction)

- **操作：** 选中 Model > 点击 `Model` 选项卡 > `Edit Pivot`。
    
- **建议：** 点击 **Center** 使轴心回到模型中心，点击 **Reset** 使其恢复默认朝向。
    

### 3. 碰撞设置 (Collision)

根据物件用途修改 `MeshPart` 的属性：

- **饰品/非交互物：** `CanCollide = false`。
    
- **普通建筑：** `CollisionFidelity = Default` (节省性能)。
    
- **需要钻进去的模型 (如帐篷)：** `CollisionFidelity = PreciseConvexDecomposition` (精确碰撞)。
    

### 4. 渲染优化

- **DoubleSided (双面)：** 若模型内部（如帐篷内部）透明，勾选此项。
    
- **RenderFidelity：** 若模型远看不需要太细，设为 `Automatic` 以启用 LOD 优化性能。
    

---

## 五、 常见问题 FAQ

- **Q: 导入后模型是碎的？**
    
    - A: 在 Max 中检查法线是否反转，导出时确保勾选了 `Triangulate`。
        
- **Q: 缩小后才看到材质？**
    
    - A: 可能是因为初始导入尺寸过大，超出了摄像机的渲染视距。在 3D Importer 面板预先调整缩放比例是最佳做法。
        
- **Q: 无法通过代码移动整个模型？**
    
    - A: 确保为 `Model` 设置了 **PrimaryPart**（通常指定为模型的主体 Mesh）。
        

---

_整理人：Gemini (根据你的 Roblox 全栈开发习惯定制)_