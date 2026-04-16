
[开发文档](https://create.roblox.com/docs/zh-cn/luau/luau-csharp-comparison#%E8%A1%8C%E7%BB%93%E6%9D%9F%E7%AC%A6)
##### 行结束符
在 Luau 中不需要分号，但它们不会破坏语法。

##### 保留关键字
以下表格包含了 Luau 的保留关键字及其对应的 C# 等效项。注意它并不显示所有 C# 关键字。

|   Luau   |      C# 等效       | 说明                                                 |
| :------: | :--------------: | -------------------------------------------------- |
|   and    |        &&        | 逻辑与                                                |
|  break   |      break       | 跳出循环                                               |
|    do    |        do        | 循环或代码块开始                                           |
|    if    |        if        | 条件判断                                               |
|   else   |       else       | 条件分支                                               |
|  elseif  |     else if      | 多条件分支。elseif 只在前面所有 if 和 elseif 条件都为 false 时才会被检查。 |
|   then   |        无         | Luau 的 if 必须搭配 then                                |
|   end    |        }         | 结束代码块                                              |
|   true   |       true       | 布尔真                                                |
|  false   |      false       | 布尔假                                                |
|   for    |  for / foreach   | 循环语句                                               |
| function | 方法 / 委托 / lambda | 定义函数                                               |
|    in    |        in        | 迭代遍历                                               |
|  local   |     （无需关键字）      | 声明局部变量                                             |
|   nil    |       null       | 空值                                                 |
|   not    |        !         | 逻辑非                                                |
|    or    |       \|\|       | 逻辑或                                                |
|  repeat  |        do        | 后置循环开始                                             |
|  return  |      return      | 返回值                                                |
|  until   |    while(!条件)    | 与 repeat 配合;`repeat until` ≈ C# `do while`         |
|  while   |      while       | 前置循环                                               |
|    ..    |        +         | 用 `+` 只做加法，用 `..` 只做拼接，彻底杜绝隐式类型错误                  |
|          |                  |                                                    |

###### 核心语法差异

###### 1. 代码块结尾

- **Luau**：使用 `end` 闭合
    
    lua
    
    ```
    if a > 0 then
        print(a)
    end
    ```
    
- **C#**：使用大括号 `{ }`
    
    csharp
    
    运行
    
    ```
    if (a > 0) {
        Console.WriteLine(a);
    }
    ```
    

###### 2. 逻辑运算符

- Luau：`and` / `or` / `not`
- C#：`&&` / `||` / `!`

###### 3. 局部变量

- Luau 必须显式写 `local`
    
    lua
    
    ```
    local x = 10
    ```
    
- C# 直接声明
    
    csharp
    
    运行
    
    ```
    int x = 10;
    ```
    

###### 4. 空值

- Luau：`nil`
- C#：`null`

###### 5. 循环结构

while 循环

```lua
while condition do
end
```

```csharp
while (condition) { }
```

repeat until（后置循环）

```lua
repeat
until condition
```

```csharp
do { } while (condition);
```
##### 注释

```Luau
-- 单行注释

--[[ 结果输出：
	块注释
--]]
```

```C# 
// 单行注释

/*
	块注释
*/
```

##### 字符串
```Luau
// 多行字符串
local multiLineString = [[这是一个字符串，
打印时，内容显示在
多行上]]

-- 字符串连接
local s1 = "这是一个字符串 "
local s2 = "由两个部分组成。"
local endString = s1 .. s2
```

##### 表
详见[[表]]
##### 运算符

##### 变量

##### 范围

##### 条件语句

##### 循环

##### 函数

##### Try-catch 结构

##### 

##### 

##### 