![image](https://github.com/user-attachments/assets/7839bb50-4a17-4b2e-9cb2-040d27251f3e)
### MyViewportButtonsExtension README

#### 概述
`MyViewportButtonsExtension` 是一个用于 NVIDIA Omniverse 平台的扩展，允许用户跟踪多个 Prim，并为每个 Prim 的变体集创建对应的按钮。按钮会根据用户提供的 Prim 顺序显示，并且会在变体集发生变化时实时更新。

#### 安装与启动
1. **下载扩展**：
   - 确保已下载并解压 `my_viewport_buttons_extension.py` 文件。

2. **添加扩展到 Omniverse**：
   - 打开 Omniverse Kit。
   - 导航到扩展管理器，添加并启用 `MyViewportButtonsExtension`。

#### 使用说明
1. **启动扩展**：
   - 启动 Omniverse Kit 后，扩展会自动启动，并显示一个对话框。

2. **输入 Prim 路径**：
   - 在对话框中输入要跟踪的 Prim 路径。可以输入多个路径，使用逗号分隔。
   - 示例：`/World/Prim1, /World/Prim2`
   - 点击“Track Prims”按钮。

3. **查看和操作变体**：
   - 在弹出的窗口中，可以查看和操作每个被跟踪的 Prim 的变体集。
   - 每个 Prim 及其变体集会以按钮的形式显示。

4. **拖动和调整窗口大小**：
   - 可以拖动窗口到所需位置，并调整窗口大小以查看所有按钮。

#### 示例操作
1. **输入路径**：
   - `/World/Prim1, /World/Prim2`

2. **查看窗口**：
   - 看到两个 Prim，每个 Prim 的变体集按钮。

3. **操作变体**：
   - 点击按钮更改变体集选择，实时更新 Prim。

#### 注意事项
- 确保输入的 Prim 路径有效且存在于当前 USD Stage 中。
- 如果 Prim 的变体集发生变化，窗口会自动更新按钮。

#### 问题与反馈
如有任何问题或需要反馈，请联系开发团队或在项目仓库中提交问题。

---

该 README 文件简要介绍了 `MyViewportButtonsExtension` 的安装、启动和使用方法，提供了必要的步骤和示例以帮助用户快速上手。
