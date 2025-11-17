# API 调用文档

## 概述

Anan's Sketchbook Web API 提供图片生成服务，支持文本、图片或两者结合的方式生成聊天框风格的图片。

**基础 URL**: `http://localhost:5000`（默认端口，可在 `api.py` 中修改）

---

## API 端点

### 生成图片

**端点**: `/generate`  
**方法**: `POST`  
**Content-Type**: `application/json`  
**描述**: 根据提供的文本和/或图片生成聊天框风格的图片

---

## 请求参数

JSON Body 参数：

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `text` | string | 否 | 要显示的文本内容。如果文本中包含表情标签（如 `#开心#`），会自动识别并使用对应的底图 |
| `image_url` | string | 否 | 图片URL或base64编码的图片数据。支持：<br>- HTTP/HTTPS URL<br>- Base64编码（`data:image/png;base64,...` 格式）<br>- 纯Base64字符串 |
| `emotion` | string | 否 | 表情标签，用于指定底图。格式：`#表情名#`，如 `#开心#`、`#生气#` 等 |

**注意**：
- `text` 和 `image_url` 至少需要提供一个
- 如果同时提供 `text` 和 `image_url`，会根据图片方向自动排布（竖图左右排布，横图上下排布）
- 如果 `text` 中包含表情标签，会优先使用文本中的表情标签，`emotion` 参数会被忽略

**响应**：
- **成功**: PNG图片文件，文件名格式：`{uuid}.png`
- **失败**: JSON格式错误信息

---

## 可用表情列表

| 表情标签 | 说明 |
|---------|------|
| `#普通#` | 默认表情 |
| `#开心#` | 开心表情 |
| `#生气#` | 生气表情 |
| `#无语#` | 无语表情 |
| `#脸红#` | 脸红表情 |
| `#病娇#` | 病娇表情 |
| `#闭眼#` | 闭眼表情 |
| `#难受#` | 难受表情 |
| `#害怕#` | 害怕表情 |
| `#激动#` | 激动表情 |
| `#惊讶#` | 惊讶表情 |
| `#哭泣#` | 哭泣表情 |

---

## 响应格式

### 成功响应

**状态码**: `200 OK`  
**Content-Type**: `image/png`  
**响应体**: PNG 图片的二进制数据

### 错误响应

**状态码**: `400 Bad Request` 或 `500 Internal Server Error`  
**Content-Type**: `application/json`  
**响应体**:
```json
{
  "error": "错误描述信息"
}
```

---

## 使用示例

### 1. 仅文本

生成纯文本的聊天框图片。

**请求示例**:
```bash
curl -X POST "http://localhost:5000/generate" \
  -H "Content-Type: application/json" \
  -d '{"text": "你好世界"}' \
  --output result.png
```

**Python 示例**:
```python
import requests

response = requests.post("http://localhost:5000/generate", json={
    "text": "你好世界"
})

if response.status_code == 200:
    with open("result.png", "wb") as f:
        f.write(response.content)
    print("✓ 图片已生成: result.png")
else:
    print(f"✗ 错误: {response.json()}")
```

**JavaScript (fetch) 示例**:
```javascript
fetch('http://localhost:5000/generate', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    text: '你好世界'
  })
})
  .then(response => {
    if (response.ok) {
      return response.blob();
    }
    return response.json().then(err => Promise.reject(err));
  })
  .then(blob => {
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'result.png';
    a.click();
  })
  .catch(error => console.error('错误:', error));
```

---

### 2. 文本 + 表情

使用指定的表情底图生成图片。

**请求示例**:
```bash
curl -X POST "http://localhost:5000/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "今天心情不错",
    "emotion": "#开心#"
  }' \
  --output result.png
```

**Python 示例**:
```python
import requests

response = requests.post("http://localhost:5000/generate", json={
    "text": "今天心情不错",
    "emotion": "#开心#"
})

if response.status_code == 200:
    with open("result.png", "wb") as f:
        f.write(response.content)
    print("✓ 图片已生成")
```

---

### 3. 文本中包含表情标签

在文本中直接使用表情标签，API会自动识别。

**请求示例**:
```bash
curl -X POST "http://localhost:5000/generate" \
  -H "Content-Type: application/json" \
  -d '{"text": "#开心#今天心情不错"}' \
  --output result.png
```

**Python 示例**:
```python
import requests

# 文本中包含表情标签
response = requests.post("http://localhost:5000/generate", json={
    "text": "#开心#今天心情不错"
})

if response.status_code == 200:
    with open("result.png", "wb") as f:
        f.write(response.content)
```

---

### 4. 仅图片

从URL加载图片并生成聊天框风格图片。

**请求示例**:
```bash
curl -X POST "http://localhost:5000/generate" \
  -H "Content-Type: application/json" \
  -d '{"image_url": "https://example.com/image.png"}' \
  --output result.png
```

**Python 示例**:
```python
import requests

response = requests.post("http://localhost:5000/generate", json={
    "image_url": "https://example.com/image.png"
})

if response.status_code == 200:
    with open("result.png", "wb") as f:
        f.write(response.content)
```

---

### 5. Base64 图片

使用Base64编码的图片数据。

**请求示例**:
```bash
curl -X POST "http://localhost:5000/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "image_url": "data:image/png;base64,iVBORw0KGgoAAAANS..."
  }' \
  --output result.png
```

**Python 示例**:
```python
import requests
import base64

# 读取本地图片并转换为base64
with open("input.png", "rb") as f:
    image_data = base64.b64encode(f.read()).decode('utf-8')
    base64_url = f"data:image/png;base64,{image_data}"

response = requests.post("http://localhost:5000/generate", json={
    "image_url": base64_url
})

if response.status_code == 200:
    with open("result.png", "wb") as f:
        f.write(response.content)
```

---

### 6. 文本 + 图片

同时提供文本和图片，API会根据图片方向自动排布。

**请求示例**:
```bash
curl -X POST "http://localhost:5000/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "这是说明文字",
    "image_url": "https://example.com/image.png",
    "emotion": "#普通#"
  }' \
  --output result.png
```

**Python 示例**:
```python
import requests

response = requests.post("http://localhost:5000/generate", json={
    "text": "这是说明文字",
    "image_url": "https://example.com/image.png",
    "emotion": "#普通#"
})

if response.status_code == 200:
    with open("result.png", "wb") as f:
        f.write(response.content)
```

**排布规则**:
- **竖图**（高度 > 宽度）：左右排布，图片在左，文本在右
- **横图**（宽度 ≥ 高度）：上下排布，图片在上，文本在下

---

## 错误处理

### 常见错误码

| 状态码 | 说明 | 示例 |
|--------|------|------|
| `400` | 请求参数错误 | 未提供 `text` 或 `image_url` |
| `400` | 图片加载失败 | `image_url` 无效或无法访问 |
| `500` | 服务器内部错误 | 图片生成失败 |

### 错误响应示例

```json
{
  "error": "请至少提供 text 或 image_url 参数之一"
}
```

```json
{
  "error": "无法加载图片，请检查 image_url 参数是否正确"
}
```

```json
{
  "error": "生成图片失败，请检查参数是否正确"
}
```

### Python 错误处理示例

```python
import requests

try:
    response = requests.get("http://localhost:5000/generate", params={
        "text": "测试"
    }, timeout=10)
    
    if response.status_code == 200:
        with open("result.png", "wb") as f:
            f.write(response.content)
        print("✓ 成功生成图片")
    else:
        error_info = response.json()
        print(f"✗ 错误 ({response.status_code}): {error_info.get('error', '未知错误')}")
        
except requests.exceptions.Timeout:
    print("✗ 请求超时")
except requests.exceptions.ConnectionError:
    print("✗ 无法连接到服务器")
except Exception as e:
    print(f"✗ 发生错误: {e}")
```

---

## 完整示例代码

### Python 完整示例

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Anan's Sketchbook API 调用示例
"""
import requests
import base64
from pathlib import Path

API_BASE_URL = "http://localhost:5000"

def generate_image(text=None, image_url=None, emotion=None, output_file="result.png"):
    """
    生成图片
    
    Args:
        text: 文本内容（可选）
        image_url: 图片URL或base64（可选）
        emotion: 表情标签（可选）
        output_file: 输出文件名
    
    Returns:
        bool: 是否成功
    """
    params = {}
    if text:
        params["text"] = text
    if image_url:
        params["image_url"] = image_url
    if emotion:
        params["emotion"] = emotion
    
    try:
        response = requests.get(f"{API_BASE_URL}/generate", params=params, timeout=30)
        
        if response.status_code == 200:
            with open(output_file, "wb") as f:
                f.write(response.content)
            print(f"✓ 图片已生成: {output_file}")
            return True
        else:
            error_info = response.json()
            print(f"✗ 错误 ({response.status_code}): {error_info.get('error', '未知错误')}")
            return False
            
    except Exception as e:
        print(f"✗ 发生错误: {e}")
        return False

def image_to_base64(image_path):
    """将本地图片转换为base64"""
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode('utf-8')

if __name__ == "__main__":
    # 示例1: 仅文本
    print("示例1: 仅文本")
    generate_image(text="你好世界", output_file="example1.png")
    
    # 示例2: 文本 + 表情
    print("\n示例2: 文本 + 表情")
    generate_image(text="今天心情不错", emotion="#开心#", output_file="example2.png")
    
    # 示例3: 文本中包含表情标签
    print("\n示例3: 文本中包含表情标签")
    generate_image(text="#生气#我很生气！", output_file="example3.png")
    
    # 示例4: 从URL加载图片
    print("\n示例4: 从URL加载图片")
    generate_image(
        image_url="https://example.com/image.png",
        emotion="#普通#",
        output_file="example4.png"
    )
    
    # 示例5: 使用本地图片（转换为base64）
    print("\n示例5: 使用本地图片")
    local_image_path = "input.png"
    if Path(local_image_path).exists():
        base64_data = image_to_base64(local_image_path)
        base64_url = f"data:image/png;base64,{base64_data}"
        generate_image(
            text="这是说明文字",
            image_url=base64_url,
            emotion="#普通#",
            output_file="example5.png"
        )
    else:
        print(f"⚠ 本地图片不存在: {local_image_path}")
    
    # 示例6: 文本 + 图片
    print("\n示例6: 文本 + 图片")
    generate_image(
        text="这是说明文字",
        image_url="https://example.com/image.png",
        emotion="#普通#",
        output_file="example6.png"
    )
```

---

## 注意事项

1. **URL编码**: 在URL中使用特殊字符（如 `#`）时，需要进行URL编码
   - `#` → `%23`
   - `空格` → `%20` 或 `+`
   - 建议使用编程语言的URL编码函数

2. **图片格式**: 支持的图片格式取决于PIL/Pillow库，通常包括：PNG、JPEG、GIF、BMP等

3. **图片大小**: 建议图片不要过大，避免请求超时或内存占用过高

4. **超时设置**: 建议设置合理的请求超时时间（如30秒）

5. **表情优先级**: 如果文本中包含表情标签，会优先使用文本中的表情，`emotion` 参数会被忽略

6. **服务器配置**: 默认端口为5000，可在 `api.py` 中修改：
   ```python
   app.run(host='0.0.0.0', port=5000, debug=False)
   ```

---

## 前端页面使用

项目提供了一个美观的前端页面（`index.html`），可以方便地调用API生成图片。

### 访问方式

1. **启动后端服务**：
   ```bash
   python api.py
   ```

2. **打开前端页面**：
   在浏览器中打开 `index.html` 文件，或者使用本地HTTP服务器：
   ```bash
   # 使用Python内置HTTP服务器
   python -m http.server 8000
   # 然后访问 http://localhost:8000
   ```

### 前端功能

- **文本输入**：支持多行文本输入
- **表情选择**：下拉菜单选择12种表情
- **实时预览**：生成后立即显示图片预览
- **一键下载**：点击下载按钮保存图片到本地
- **表单清空**：清空按钮重置表单和结果
- **加载状态**：显示生成进度，防止重复提交
- **错误提示**：友好的错误消息显示

### 使用流程

1. 在文本框中输入要显示的内容
2. （可选）从下拉菜单选择表情类型
3. 点击"🎯 生成图片"按钮
4. 等待生成完成，查看预览
5. 点击"💾 下载图片"保存到本地

### 前端特性

- **响应式设计**：适配不同屏幕尺寸
- **现代UI**：使用现代CSS样式，视觉效果良好
- **用户体验**：加载状态、错误处理、操作反馈
- **无需上传图片**：仅支持文本和表情组合生成
- **UUID文件名**：下载的图片使用时间戳命名

### 技术实现

前端使用原生HTML、CSS和JavaScript实现，主要特性：

- **Fetch API**：现代HTTP请求方式
- **Blob处理**：直接处理二进制图片数据
- **File API**：支持图片下载功能
- **DOM操作**：动态更新页面内容
- **事件处理**：表单提交和用户交互

### 注意事项

- 前端默认API地址：`http://localhost:5000`
- 如果后端部署在其他地址，需要修改JavaScript中的 `API_BASE_URL`
- 支持现代浏览器（Chrome、Firefox、Safari、Edge等）
- 需要确保前端页面可以访问后端API（无跨域问题）

---

## 技术支持

如有问题或建议，请查看项目文档或提交Issue。

