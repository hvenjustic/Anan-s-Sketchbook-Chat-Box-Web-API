# 项目运行指南

## 环境要求

- Python 3.8 或更高版本
- Windows / Linux / macOS（已移除Windows特定依赖）

## 安装步骤

### 1. 安装 Python

如果尚未安装 Python，请访问 [Python官网](https://www.python.org/downloads/) 下载并安装。

**注意**: 安装时请勾选 "Add Python to PATH"（添加到PATH环境变量）。

### 2. 安装项目依赖

打开终端（Windows: PowerShell 或 CMD，Linux/macOS: Terminal），进入项目目录，运行：

```bash
pip install -r requirements.txt
```

如果使用 Python 3，可能需要使用：

```bash
pip3 install -r requirements.txt
```

### 3. 检查配置文件

确保 `config.yaml` 文件存在且配置正确。主要需要检查：

- `font_file`: 字体文件路径（默认: `font.ttf`）
- `baseimage_mapping`: 表情底图映射
- `text_box_topleft` 和 `image_box_bottomright`: 文本/图片区域坐标
- `base_overlay_file`: 置顶图层文件路径

## 运行项目

### 启动 Web API 服务器

在项目根目录下运行：

```bash
python api.py
```

或者：

```bash
python3 api.py
```

### 服务器信息

启动成功后，你会看到类似以下的日志：

```
启动Web API服务器...
生成图片: http://localhost:5000/generate?text=你好世界
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Running on http://192.168.x.x:5000
```

服务器将在以下地址运行：
- 本地访问: `http://localhost:5000`
- 局域网访问: `http://你的IP地址:5000`

### 停止服务器

按 `Ctrl + C` 停止服务器。

## 测试运行

### 方法1: 浏览器测试

打开浏览器，访问：

```
http://localhost:5000/generate?text=你好世界
```

如果一切正常，浏览器会下载或显示生成的PNG图片。

### 方法2: 使用 curl 测试

```bash
curl "http://localhost:5000/generate?text=你好世界" --output test.png
```

### 3: 使用 Python 测试

创建 `test.py` 文件：

```python
import requests

response = requests.post("http://localhost:5000/generate", json={
    "text": "你好世界",
    "emotion": "#开心#"
})

if response.status_code == 200:
    with open("test.png", "wb") as f:
        f.write(response.content)
    print("✓ 图片已生成: test.png")
else:
    print(f"✗ 错误: {response.json()}")
```

运行：

```bash
python test.py
```

### 4: 使用前端页面

项目提供了美观的前端界面：

1. 在浏览器中打开 `index.html` 文件
2. 或者使用本地HTTP服务器：
   ```bash
   python -m http.server 8000
   # 然后访问 http://localhost:8000
   ```

前端页面功能：
- 文本输入框
- 表情选择器
- 一键生成
- 图片预览
- 下载功能

**注意**：前端页面使用POST方法调用API，与URL参数方式不同。

## 常见问题

### 1. 端口被占用

如果 5000 端口已被占用，可以修改 `api.py` 文件最后一行：

```python
app.run(host='0.0.0.0', port=8080, debug=False)  # 改为其他端口，如8080
```

### 2. 依赖安装失败

如果 `pip install` 失败，可以尝试：

```bash
# 使用国内镜像源
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 或使用阿里云镜像
pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/
```

### 3. 字体文件不存在

确保 `font.ttf` 文件存在于项目根目录，或修改 `config.yaml` 中的 `font_file` 路径。

### 4. 底图文件不存在

确保 `BaseImages` 目录下存在所需的图片文件：
- `base.png`（默认底图）
- `base_overlay.png`（置顶图层）
- 以及其他表情图片（如 `开心.png`、`生气.png` 等）

### 5. 无法访问服务器

- **本地无法访问**: 检查防火墙设置，确保允许 Python 访问网络
- **局域网无法访问**: 确保服务器绑定到 `0.0.0.0`（已在代码中设置）

## API 使用说明

详细的API调用示例请参考 [API_USAGE.md](API_USAGE.md)

### 快速示例

```bash
# 仅文本
curl "http://localhost:5000/generate?text=你好世界" --output result.png

# 文本 + 表情
curl "http://localhost:5000/generate?text=你好世界&emotion=%23开心%23" --output result.png

# 文本 + 图片URL + 表情
curl "http://localhost:5000/generate?text=测试&image_url=https://example.com/image.png&emotion=%23普通%23" --output result.png
```

## 项目结构

```
项目根目录/
├── api.py                 # Web API 服务器主文件
├── config.yaml            # 配置文件
├── config_loader.py       # 配置加载模块
├── text_fit_draw.py       # 文本绘制模块
├── image_fit_paste.py     # 图片处理模块
├── requirements.txt       # Python依赖列表
├── font.ttf              # 字体文件
├── BaseImages/           # 底图资源目录
│   ├── base.png
│   ├── base_overlay.png
│   └── ...
└── RUN.md                # 本文件
```

## 下一步

- 查看 [API_USAGE.md](API_USAGE.md) 了解详细的API调用方法
- 根据需要修改 `config.yaml` 中的配置
- 集成到你的应用程序中

