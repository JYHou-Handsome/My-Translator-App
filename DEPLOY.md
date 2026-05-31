# 部署文档

本文档详细介绍如何在本地环境部署和运行划词翻译工具。

## 环境要求

- **操作系统**：Windows 10/11、macOS 10.15+、Linux（Ubuntu 20.04+）
- **Python 版本**：Python 3.10 或更高版本
- **网络**：需要联网访问有道翻译 API

## 部署步骤

### 一、安装 Python

#### Windows

1. 访问 [Python 官网](https://www.python.org/downloads/)
2. 下载 Python 3.10 或更高版本的安装包
3. 运行安装程序，**务必勾选** "Add Python to PATH"
4. 点击 "Install Now" 完成安装
5. 打开命令提示符（CMD）或 PowerShell，验证安装：

```bash
python --version
```

#### macOS

```bash
# 使用 Homebrew 安装
brew install python@3.10

# 验证安装
python3 --version
```

#### Linux (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv

# 验证安装
python3 --version
```

### 二、下载项目

#### 方式一：使用 Git 克隆

```bash
git clone git@github.com:JYHou-Handsome/My-Translator-App.git
cd My-Translator-App
```

#### 方式二：直接下载

1. 访问 [项目页面](https://github.com/JYHou-Handsome/My-Translator-App)
2. 点击绿色 "Code" 按钮
3. 选择 "Download ZIP"
4. 解压下载的压缩包

### 三、创建虚拟环境（推荐）

创建虚拟环境可以避免依赖冲突，建议使用。

#### Windows

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
venv\Scripts\activate
```

#### macOS / Linux

```bash
# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
source venv/bin/activate
```

激活后，命令行前面会显示 `(venv)`，表示虚拟环境已启用。

### 四、安装依赖

确保虚拟环境已激活，然后执行：

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

如果安装速度慢，可以使用国内镜像源：

```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 五、申请有道翻译 API

1. 访问 [有道智云](https://ai.youdao.com/)
2. 注册并登录账号
3. 进入控制台，选择 "创建应用"
4. 填写应用信息：
   - 应用名称：随意填写（如"划词翻译"）
   - 应用类型：选择"翻译"
   - 服务内容：勾选"文本翻译"
5. 创建完成后，获取以下信息：
   - **App Key**（应用 ID）
   - **App Secret**（应用密钥）

### 六、运行程序

```bash
python main.py
```

首次运行后：

1. 程序会在系统托盘显示图标
2. 右键点击托盘图标，选择 "设置"
3. 在设置界面填入有道翻译的 **App Key** 和 **App Secret**
4. 点击 "测试连接" 验证配置是否正确
5. 保存设置

### 七、使用方法

| 快捷键 | 功能 |
|--------|------|
| `Ctrl + Shift + T` | 翻译剪贴板中的文本 |

使用流程：

1. 选中要翻译的文本
2. 按 `Ctrl + C` 复制到剪贴板
3. 按 `Ctrl + Shift + T` 触发翻译
4. 悬浮窗显示翻译结果

## 常见问题

### 1. 提示 "Python 不是内部或外部命令"

**原因**：Python 未添加到系统环境变量

**解决**：
- 重新安装 Python，勾选 "Add Python to PATH"
- 或手动添加 Python 到环境变量

### 2. 安装依赖时报错

**原因**：pip 版本过低或网络问题

**解决**：

```bash
# 升级 pip
python -m pip install --upgrade pip

# 使用国内镜像源
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 3. 快捷键不生效

**原因**：快捷键被其他软件占用

**解决**：
- 检查是否有其他软件使用了相同的快捷键
- 以管理员权限运行程序（Windows）

### 4. 翻译失败

**原因**：API 配置错误或网络问题

**解决**：
- 检查 App Key 和 App Secret 是否正确
- 检查网络连接是否正常
- 在设置界面点击 "测试连接" 查看具体错误

### 5. 语音朗读没有声音

**原因**：系统未安装 TTS 语音引擎

**解决**：
- Windows：系统自带语音引擎，通常无需额外安装
- macOS：系统自带语音引擎
- Linux：安装 espeak

```bash
sudo apt install espeak
```

## 卸载方法

1. 删除项目文件夹
2. 如果创建了虚拟环境，删除 `venv` 文件夹即可

## 技术支持

如遇到问题，请在 [GitHub Issues](https://github.com/JYHou-Handsome/My-Translator-App/issues) 提交反馈。