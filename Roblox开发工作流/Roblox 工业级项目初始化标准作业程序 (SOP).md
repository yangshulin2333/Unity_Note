

**前置条件：** 已全局安装 VS Code 及 Rokit 工具链管理器。

## 阶段一：声明与初始化 (Initialization)

> **目的：** 在空文件夹中建立基本的工程结构，并绑定该项目专属的工具版本。

1. **新建并打开工作区**
    
    - 创建一个空文件夹（如 `Roblox_Demo`），在 VS Code 中打开。
        
    - 使用 `Ctrl + ~` 打开集成终端。
        
2. **初始化 Rokit (工具链管理)**
    
    Bash
    
    ```
    rokit init
    ```
    
3. **声明项目所需工具**
    
    _逐行执行，将基础工具与当前项目绑定：_
    
    Bash
    
    ```
    rokit add rojo
    rokit add wally
    rokit add wally-package-types
    rokit add selene
    rokit add stylua
    ```
    
4. **生成核心工程文件**
    
    _逐行执行，生成代码目录和包管理清单：_
    
    Bash
    
    ```
    rojo init
    wally init
    ```
    

---

## 阶段二：工程环境调优 (Configuration Tuning)

> **目的：** 剔除危险的默认配置，建立代码规范和版本控制黑名单。这是最容易遗漏的一环。

1. **解除 Rojo 对游戏物理世界的控制 (🚨极其重要)**
    
    - **文件：** `default.project.json`
        
    - **操作：** 找到 `"Workspace": { ... }` 这个代码块。**将其连同内部所有内容彻底删除**。
        
    - **原因：** 防止 Rojo 在连接 Studio 时，将你手动摆放的 3D 模型和地形全部抹除覆盖。
        
2. **配置静态代码检查 (Linter)**
    
    - **文件：** 在根目录手动新建 `selene.toml`
        
    - **内容：** 写入以下代码，告诉代码检查工具这是 Roblox 环境，不要对 `game` 或 `workspace` 等全局变量报错。
        ```Ini, TOML
        std = "roblox"
        ```
        
3. **配置版本控制黑名单**
    
    - **文件：** 打开 `.gitignore` (由 rojo init 自动生成)
        
    - **操作：** 在文件末尾追加以下内容，防止 Git 记录海量的第三方库和临时生成的地图文件：
        
        Plaintext
        
        ```
        Packages/
        ServerPackages/
        sourcemap.json
        wally.lock
        ```

---

## 阶段三：依赖包引入与类型生成 (Dependency & Types)

> **目的：** 引入第三方框架，并生成智能代码提示。

1. **声明所需依赖**
    
    - **文件：** `wally.toml`
        
    - **操作：** 在 `[dependencies]` 下方填入你需要的包。例如：
        ```Ini, TOML
        [dependencies]
        Matter = "evaera/matter@0.7.0"
        ```
        
2. **执行装包与映射三连命令**
    
    _在终端中按顺序执行：_
    
    Bash
    
    ```
    # 1. 下载远程包到本地
    wally install 
    
    # 2. 扫描当前目录结构，生成关系地图
    rojo sourcemap default.project.json -o sourcemap.json 
    
    # 3. 参照地图，为下载的包提取强类型代码提示
    wally-package-types -s sourcemap.json Packages/ 
    ```
    
3. **将包路径注册到 Rojo 映射中**
    
    - **文件：** `default.project.json`
        
    - **操作：** 在 `"ReplicatedStorage"` 内部，追加 `"Packages"` 的映射路径。修改后应如下所示（注意层级和逗号）：
        ```JSON
        "ReplicatedStorage": {
          "$className": "ReplicatedStorage",
          "Shared": {
            "$path": "src/shared"
          },
          "Packages": {
            "$path": "Packages"
          }
        },
        ```

    ```JSON
          "ServerScriptService": {
          "$className": "ServerScriptService",
          "Server": {
            "$path": "src/server"
          },
          "ServerPackages": {
            "$path": "ServerPackages"
          }
        },
    ```

---

## 阶段四：启动与双向桥接 (Bootstrapping)

> **目的：** 启动本地服务器，完成 VS Code 与 Roblox Studio 的联机。

1. **启动本地 Rojo 服务器 (VS Code 端)**
    
    - 按下 `Ctrl + Shift + P` 打开命令面板。
        
    - 输入 `Rojo: Start server` 并回车。（或点击底部的 Rojo 图标）。
        
    - _此时 VS Code 正在监听 3487 端口的代码变动。_
        
2. **连接游戏引擎 (Studio 端)**
    
    - 打开 Roblox Studio，新建一个空地图 (Baseplate)。
        
    - 在上方菜单栏点击 **Plugins (插件)** -> **Rojo** -> **Connect**。
        
3. **验证联机**
    
    - 检查 Studio 的 `ReplicatedStorage` 目录，确认是否已自动出现 `Shared` 文件夹和装满代码的 `Packages` 文件夹。
        

**至此，标准工业级环境搭建完毕。一切业务逻辑代码，均在 VS Code 的 `src` 目录下开展。**