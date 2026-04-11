##### 行结束符
在 Luau 中不需要分号，但它们不会破坏语法。

##### 保留关键字
以下表格包含了 Luau 的保留关键字及其对应的 C# 等效项。注意它并不显示所有 C# 关键字。

| Luau     | C# 等效            | 说明                                         |
| -------- | ---------------- | ------------------------------------------ |
| and      | &&               | 逻辑与                                        |
| break    | break            | 跳出循环                                       |
| do       | do               | 循环或代码块开始                                   |
| if       | if               | 条件判断                                       |
| else     | else             | 条件分支                                       |
| elseif   | else if          | 多条件分支                                      |
| then     | 无                | Luau 的 if 必须搭配 then                        |
| end      | }                | 结束代码块                                      |
| true     | true             | 布尔真                                        |
| false    | false            | 布尔假                                        |
| for      | for / foreach    | 循环语句                                       |
| function | 方法 / 委托 / lambda | 定义函数                                       |
| in       | in               | 迭代遍历                                       |
| local    | （无需关键字）          | 声明局部变量                                     |
| nil      | null             | 空值                                         |
| not      | !                | 逻辑非                                        |
| or       | \|\|             | 逻辑或                                        |
| repeat   | do               | 后置循环开始                                     |
| return   | return           | 返回值                                        |
| until    | while(!条件)       | 与 repeat 配合;`repeat until` ≈ C# `do while` |
| while    | while            | 前置循环                                       |

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

