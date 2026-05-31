# 划词翻译工具

一个基于 PyQt6 的桌面划词翻译工具，支持屏幕截图 OCR 识别和多语言翻译，提供悬浮窗显示翻译结果。

## 功能特性

- **划词翻译**：选中文本后按快捷键即可翻译
- **截图 OCR**：支持屏幕截图并识别文字进行翻译
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
- **Tesseract OCR**：文字识别
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
    ├── screen_capture.py      # 截图功能
    ├── ocr_engine.py          # OCR 文字识别
    ├── translator.py          # 有道翻译 API 封装
    ├── tts_engine.py          # 语音朗读引擎
    ├── database.py            # SQLite 数据库操作
    ├── settings_window.py     # 设置窗口
    ├── history_window.py      # 翻译历史窗口
    └── word_book_window.py    # 生词本窗口
```

## 运行方式

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 安装 Tesseract OCR

- **Windows**：下载安装 [Tesseract](https://github.com/UB-Mannheim/tesseract/wiki)，安装时勾选中文语言包
- **macOS**：`brew install tesseract tesseract-lang`
- **Linux**：`sudo apt install tesseract-ocr tesseract-ocr-chi-sim`

### 3. 配置有道翻译 API

1. 访问 [有道智云](https://ai.youdao.com/) 注册账号
2. 创建翻译应用，获取 **App Key** 和 **App Secret**
3. 运行程序后，在设置中填入密钥

### 4. 运行程序

```bash
python main.py
```

## 使用说明

| 快捷键 | 功能 |
|--------|------|
| `Ctrl + Shift + T` | 翻译选中的文本 |
| `Ctrl + Shift + O` | 截图 OCR 翻译 |

## 截图

![截图演示](screenshot.png)

## 许可证

MIT License