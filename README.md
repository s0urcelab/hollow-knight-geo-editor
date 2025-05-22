# 空洞骑士金币（Geo）修改器

[中文](#chinese) | [English](#english)

## Chinese

### 简介
空洞骑士金币修改器是一个简单易用的工具，允许你修改空洞骑士存档文件中的金币（Geo）数值。该工具提供了图形界面，方便存档文件管理和金币编辑。灵感来自于：[bloodorca/hollow](https://github.com/bloodorca/hollow)

### 功能特点
- 浏览和选择不同存档槽中的存档文件
- 查看存档文件详细信息（文件名、大小、修改时间）
- 修改存档文件中的金币数值
- 自动备份存档文件
- 用户友好的图形界面
- 支持多个存档槽

### 系统要求
- Windows 操作系统

### 开发
1. 克隆此仓库或下载最新发布版本
2. 安装所需的依赖项：
```bash
pip install -r requirements.txt
```

### 编译可执行文件
要创建独立的可执行文件：

1. 确保安装了 Python 3.9 或 3.10（不支持 Python 3.11+ 版本）
2. 安装 PyInstaller：
```bash
pip install pyinstaller
```
3. 运行编译脚本：
```bash
python build.py
```
4. 可执行文件将在 `dist` 文件夹中生成

### 注意事项
- 工具会自动创建存档文件的备份
- 存档文件位置：`%APPDATA%\..\LocalLow\Team Cherry\Hollow Knight`

---

## English

### Hollow Knight Geo Editor

### Description
Hollow Knight Geo Editor is a simple and user-friendly tool that allows you to modify the Geo (currency) value in your Hollow Knight save files. This tool provides a graphical interface for easy save file management and Geo editing. Inspired by: [bloodorca/hollow](https://github.com/bloodorca/hollow)

### Features
- Browse and select save files from different save slots
- View save file details (filename, size, modification time)
- Modify Geo value in save files
- Automatic save file backup
- User-friendly graphical interface
- Support for multiple save slots

### Requirements
- Windows operating system

### Develop
1. Clone this repository or download the latest release
2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

### Building the Executable
To create a standalone executable:

1. Make sure you have Python 3.9 or 3.10 installed (Python 3.11+ is not supported)
2. Install PyInstaller:
```bash
pip install pyinstaller
```
3. Run the build script:
```bash
python build.py
```
4. The executable will be created in the `dist` folder

### Note
- The tool automatically creates backups of your save files
- Save files are located in: `%APPDATA%\..\LocalLow\Team Cherry\Hollow Knight`
