# Anan's Sketchbook 生成器

一个基于Flask的图片生成API和前端界面，支持文本+表情的聊天框风格图片生成。

## 快速开始

```bash
pip install -r requirements.txt
python api.py
```

访问：**https://www.hvenjustic.com:5000/**

## API 使用

**POST** `/generate`

参数：
- `text` (string): 文本内容
- `emotion` (string): 表情标签（可选）

```bash
curl -X POST "https://www.hvenjustic.com:5000/generate" \
  -H "Content-Type: application/json" \
  -d '{"text": "你好世界", "emotion": "#开心#"}' \
  --output result.png
```

**Python示例**：
```python
import requests

response = requests.post("https://www.hvenjustic.com:5000/generate", json={
    "text": "你好世界",
    "emotion": "#开心#"
})

with open("result.png", "wb") as f:
    f.write(response.content)
```

**JavaScript示例**：
```javascript
fetch('https://www.hvenjustic.com:5000/generate', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({text: '你好世界', emotion: '#开心#'})
})
.then(r => r.blob())
.then(blob => {
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url; a.click();
});
```

## 表情列表
`#普通#`、`#开心#`、`#生气#`、`#无语#`、`#脸红#`、`#病娇#`、`#闭眼#`、`#难受#`、`#害怕#`、`#激动#`、`#惊讶#`、`#哭泣#`

## 生产部署
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 api:app
```

## 常见问题

**端口占用**：修改 `api.py` 最后一行端口号
```python
app.run(host='0.0.0.0', port=8080, debug=False)
```

**依赖安装失败**：使用国内镜像
```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

**字体文件缺失**：确保 `font.ttf` 文件存在
**底图文件缺失**：确保 `BaseImages/` 目录完整

## 项目结构
```
├── api.py                 # Flask应用主文件
├── index.html            # 前端页面
├── config.yaml           # 配置文件
├── font.ttf             # 字体文件
├── BaseImages/          # 表情底图目录
├── requirements.txt     # Python依赖
└── *.py 模块文件       # 核心功能模块
```

---

**前端页面**：http://www.hvenjustic.top:5000/

