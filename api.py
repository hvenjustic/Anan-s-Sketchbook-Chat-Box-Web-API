# -*- coding: utf-8 -*-
"""
Web API 服务器，提供图片生成接口
"""
import io
import logging
import base64
import urllib.request
import urllib.parse
import uuid
from typing import Optional
from flask import Flask, request, send_file, jsonify
from PIL import Image

from config_loader import load_config
from image_fit_paste import paste_image_auto
from text_fit_draw import draw_text_auto

app = Flask(__name__)
config = load_config()

# 配置日志
logging.basicConfig(
    level=getattr(logging, config.logging_level.upper(), logging.INFO),
    format="%(asctime)s [%(levelname)s] %(message)s",
)

# 全局变量：当前使用的表情和比例
current_emotion = "#普通#"
last_used_image_file = config.baseimage_mapping.get(current_emotion, config.baseimage_file)
ratio = 1


def is_vertical_image(image: Image.Image) -> bool:
    """
    判断图像是否为竖图
    """
    return image.height * ratio > image.width


def get_ratio(x1, y1, x2, y2):
    """
    计算并更新全局比例
    """
    global ratio
    try:
        ratio = (x2 - x1) / (y2 - y1)
        logging.info("比例: %s", ratio)
    except Exception as e:
        logging.error("计算比例时出错: %s", e)


def load_image_from_url_or_base64(image_input: str) -> Optional[Image.Image]:
    """
    从URL或base64字符串加载图片
    
    Args:
        image_input: 图片URL或base64编码的图片数据（支持 data:image/...;base64,... 格式）
    
    Returns:
        PIL Image对象，如果加载失败返回None
    """
    try:
        # URL解码（处理URL编码的字符）
        image_input = urllib.parse.unquote(image_input)
        
        # 检查是否是base64格式
        if image_input.startswith('data:image'):
            # 处理 data:image/png;base64,xxx 格式
            header, data = image_input.split(',', 1)
            image_data = base64.b64decode(data)
            return Image.open(io.BytesIO(image_data))
        elif image_input.startswith('http://') or image_input.startswith('https://'):
            # 从URL下载图片
            req = urllib.request.Request(image_input)
            req.add_header('User-Agent', 'Mozilla/5.0')
            with urllib.request.urlopen(req, timeout=10) as response:
                image_data = response.read()
                return Image.open(io.BytesIO(image_data))
        else:
            # 尝试直接作为base64解码
            image_data = base64.b64decode(image_input)
            return Image.open(io.BytesIO(image_data))
    except Exception as e:
        logging.error(f"加载图片失败: {e}")
        return None


def process_text_and_image(text: str, image: Optional[Image.Image], emotion: Optional[str] = None) -> Optional[bytes]:
    """
    同时处理文本和图像内容，将其绘制到同一张图片上
    
    Args:
        text: 文本内容
        image: PIL Image对象（可选）
        emotion: 表情标签（可选）
    
    Returns:
        PNG图片的字节流，如果失败返回None
    """
    global last_used_image_file
    
    # 确定使用的底图
    if emotion and emotion in config.baseimage_mapping:
        last_used_image_file = config.baseimage_mapping[emotion]
        logging.info(f"使用表情: {emotion}，底图: {last_used_image_file}")
    elif not emotion:
        # 如果没有指定表情，检查文本中是否包含表情标签
        for keyword, img_file in config.baseimage_mapping.items():
            if keyword in text:
                last_used_image_file = img_file
                text = text.replace(keyword, "").strip()
                logging.info(f"检测到关键词 '{keyword}'，使用底图: {last_used_image_file}")
                break
    
    if text == "" and image is None:
        return None

    # 获取配置的区域坐标
    x1, y1 = config.text_box_topleft
    x2, y2 = config.image_box_bottomright
    region_width = x2 - x1
    region_height = y2 - y1

    # 只有图像的情况
    if text == "" and image is not None:
        logging.info("处理图片内容")
        try:
            return paste_image_auto(
                image_source=last_used_image_file,
                image_overlay=(
                    config.base_overlay_file if config.use_base_overlay else None
                ),
                top_left=(x1, y1),
                bottom_right=(x2, y2),
                content_image=image,
                align="center",
                valign="middle",
                padding=12,
                allow_upscale=True,
                keep_alpha=True,
            )
        except Exception as e:
            logging.error("生成图片失败: %s", e)
            return None

    # 只有文本的情况
    elif text != "" and image is None:
        logging.info("从文本生成图片: " + text)
        try:
            return draw_text_auto(
                image_source=last_used_image_file,
                image_overlay=(
                    config.base_overlay_file if config.use_base_overlay else None
                ),
                top_left=(x1, y1),
                bottom_right=(x2, y2),
                text=text,
                color=(0, 0, 0),
                max_font_height=64,
                font_path=config.font_file,
                wrap_algorithm=config.text_wrap_algorithm,
            )
        except Exception as e:
            logging.error("生成图片失败: %s", e)
            return None

    # 同时有图像和文本的情况
    else:
        logging.info("同时处理文本和图片内容")
        logging.info("文本内容: " + text)
        get_ratio(x1, y1, x2, y2)
        try:
            # 根据图像方向决定排布方式
            if is_vertical_image(image):
                logging.info("使用左右排布（竖图）")
                # 左右排布：图像在左，文本在右
                spacing = 10
                left_width = region_width // 2 - spacing // 2
                right_width = region_width - left_width - spacing
                
                left_region_right = x1 + left_width
                right_region_left = left_region_right + spacing
                
                # 先绘制左半部分的图像
                intermediate_bytes = paste_image_auto(
                    image_source=last_used_image_file,
                    image_overlay=None,
                    top_left=(x1, y1),
                    bottom_right=(left_region_right, y2),
                    content_image=image,
                    align="center",
                    valign="middle",
                    padding=12,
                    allow_upscale=True, 
                    keep_alpha=True,
                )
                
                # 在已有图像基础上添加右半部分的文本
                final_bytes = draw_text_auto(
                    image_source=io.BytesIO(intermediate_bytes),
                    image_overlay=config.base_overlay_file if config.use_base_overlay else None,
                    top_left=(right_region_left, y1),
                    bottom_right=(x2, y2),
                    text=text,
                    color=(0, 0, 0),
                    max_font_height=64,
                    font_path=config.font_file,
                    wrap_algorithm=config.text_wrap_algorithm,
                )
            else:
                logging.info("使用上下排布（横图）")
                # 上下排布：图像在上，文本在下
                estimated_text_height = min(region_height // 2, 100)
                image_region_bottom = y1 + (region_height - estimated_text_height)
                text_region_top = image_region_bottom
                text_region_bottom = y2
                
                # 先绘制图像
                intermediate_bytes = paste_image_auto(
                    image_source=last_used_image_file,
                    image_overlay=None,
                    top_left=(x1, y1),
                    bottom_right=(x2, image_region_bottom),
                    content_image=image,
                    align="center",
                    valign="middle",
                    padding=12,
                    allow_upscale=True, 
                    keep_alpha=True,
                )
                
                # 在已有图像基础上添加文本
                final_bytes = draw_text_auto(
                    image_source=io.BytesIO(intermediate_bytes),
                    image_overlay=config.base_overlay_file if config.use_base_overlay else None,
                    top_left=(x1, text_region_top),
                    bottom_right=(x2, text_region_bottom),
                    text=text,
                    color=(0, 0, 0),
                    max_font_height=64,
                    font_path=config.font_file,
                    wrap_algorithm=config.text_wrap_algorithm,
                )
            
            return final_bytes
            
        except Exception as e:
            logging.error("生成图片失败: %s", e)
            return None


@app.route('/generate', methods=['POST'])
def generate_image():
    """
    生成图片的API端点
    
    JSON Body参数:
        text: 文本内容（可选）
        image_url: 图片URL或base64编码的图片数据（可选）
        emotion: 表情标签，如 #普通#、#开心# 等（可选）
    
    返回:
        生成的PNG图片，或错误信息（JSON格式）
    
    示例:
        POST /generate
        Body: {"text": "你好世界", "emotion": "#开心#"}
    """
    try:
        # 获取JSON数据
        data = request.get_json()
        if not data:
            return jsonify({
                'error': '请提供JSON格式的请求体'
            }), 400
        
        text = data.get('text', '').strip()
        image_url = data.get('image_url', '').strip()
        emotion = data.get('emotion', '').strip()
        
        # 如果没有提供任何内容，返回错误
        if not text and not image_url:
            return jsonify({
                'error': '请至少提供 text 或 image_url 参数之一'
            }), 400
        
        # 加载图片（如果提供了）
        image = None
        if image_url:
            image = load_image_from_url_or_base64(image_url)
            if image is None:
                return jsonify({
                    'error': '无法加载图片，请检查 image_url 参数是否正确'
                }), 400
        
        # 处理表情参数
        emotion_tag = emotion if emotion else None
        
        # 生成图片
        png_bytes = process_text_and_image(text, image, emotion_tag)
        
        if png_bytes is None:
            return jsonify({
                'error': '生成图片失败，请检查参数是否正确'
            }), 500
        
        # 生成UUID文件名
        filename = f"{uuid.uuid4()}.png"
        
        # 返回图片，设置Content-Disposition头以支持下载
        return send_file(
            io.BytesIO(png_bytes),
            mimetype='image/png',
            as_attachment=True,
            download_name=filename
        )
        
    except Exception as e:
        logging.error(f"API错误: {e}", exc_info=True)
        return jsonify({
            'error': f'服务器内部错误: {str(e)}'
        }), 500


if __name__ == '__main__':
    logging.info("启动Web API服务器...")
    logging.info("生成图片: http://localhost:5000/generate?text=你好世界")
    app.run(host='0.0.0.0', port=5000, debug=False)

