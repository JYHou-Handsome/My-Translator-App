# 划词翻译工具

一个基于 PyQt6 的桌面划词翻译工具，支持多语言翻译，提供悬浮窗显示翻译结果。

## 功能特性

- **划词翻译**：选中文本后按快捷键即可翻译
- **多语言支持**：支持中文、英文、日文、韩文、法文、德文、西班牙文、葡萄牙文、俄文
- **悬浮窗显示**：翻译结果以悬浮窗形式展示，支持透明度调整
- **生词本**：可收藏翻译结果，方便复习
- **翻译历史**：记录翻译历史，支持查看和管理
- **语音朗读**：支持对原文和译文进行语音朗读
- **系统托盘**：最小化到系统托盘，不占用任务栏空间

## 技术栈

- **Python 3.10+**
- **PyQt6**：GUI 框架
- **有道翻译 API**：翻译服务
- **pyttsx3**：语音合成
- **SQLite**：本地数据存储

## 项目结构

```
translator-app/
├── main.py                    # 程序入口
├── requirements.txt           # Python 依赖
├── README.md                  # 项目说明
└── src/
    ├── __init__.py            # 包初始化
    ├── app.py                 # 主应用类，系统托盘和全局逻辑
    ├── floating_window.py     # 悬浮窗，显示翻译结果
    ├── hotkey_listener.py     # 全局热键监听
    ├── translator.py          # 有道翻译 API 封装
    ├── tts_engine.py          # 语音朗读引擎
    ├── database.py            # SQLite 数据库操作
    ├── settings_window.py     # 设置窗口
    ├── history_window.py      # 翻译历史窗口
    └── word_book_window.py    # 生词本窗口
```

## 运行方式

### 1. 安装 Python 依赖

```bash
pip install -r requirements.txt
```

依赖说明：

| 包名 | 版本要求 | 用途 |
|------|----------|------|
| PyQt6 | >=6.5.0 | GUI 图形界面框架 |
| requests | >=2.28.0 | 发送 HTTP 请求调用有道翻译 API |
| keyboard | >=0.13.5 | 注册全局快捷键 |
| pyttsx3 | >=2.90 | 文本转语音朗读 |
| pyperclip | >=1.8.2 | 读取系统剪贴板内容 |
| pytesseract | >=0.3.10 | OCR 文字识别（可选，截图翻译功能需要） |
| Pillow | >=10.0.0 | 图像处理（可选，截图翻译功能需要） |

### 2. 配置有道翻译 API

1. 访问 [有道智云](https://ai.youdao.com/) 注册账号
2. 创建翻译应用，获取 **App Key** 和 **App Secret**
3. 运行程序后，在设置中填入密钥

### 3. 运行程序

```bash
python main.py
```

## 使用说明

1. 选中要翻译的文本，按 `Ctrl + C` 复制到剪贴板
2. 按下快捷键 `Ctrl + Shift + T` 触发翻译
3. 翻译结果会以悬浮窗形式显示在屏幕上

## 许可证

MIT License