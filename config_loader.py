# -*- coding: utf-8 -*-
import os
import yaml
from typing import Dict, Tuple
from pydantic import BaseModel


class Config(BaseModel):
    """配置模型类 - Web API版本，仅包含图片生成相关配置"""
    font_file: str = "font.ttf"
    """字体文件路径"""
    baseimage_mapping: Dict[str, str] = {
        "#普通#": os.path.join("BaseImages", "base.png")
    }
    """差分表情映射字典"""
    baseimage_file: str = os.path.join("BaseImages", "base.png")
    """默认底图文件路径"""
    text_box_topleft: Tuple[int, int] = (119, 450)
    """文本框左上角坐标"""
    image_box_bottomright: Tuple[int, int] = (398, 625)
    """文本框右下角坐标"""
    base_overlay_file: str = os.path.join("BaseImages", "base_overlay.png")
    """底图置顶图层文件路径"""
    use_base_overlay: bool = False
    """是否使用底图置顶图层"""
    logging_level: str = "INFO"
    """日志记录等级"""
    text_wrap_algorithm: str = "original"
    """文本换行算法，可选值："original"(原始算法), "knuth_plass"(改进的Knuth-Plass算法)"""
    server_host: str = "0.0.0.0"
    """服务器监听地址，0.0.0.0 表示监听所有网络接口"""
    server_port: int = 5001
    """服务器端口号"""

    class Config:
        arbitrary_types_allowed = True


def load_config(config_file: str = "config.yaml") -> Config:
    """
    从YAML文件加载配置
    
    Args:
        config_file: 配置文件路径
        
    Returns:
        Config: 配置对象
    """
    # 如果配置文件不存在，使用默认配置
    if not os.path.exists(config_file):
        return Config()
    
    # 读取YAML配置文件
    with open(config_file, 'r', encoding='utf-8') as f:
        config_data = yaml.safe_load(f)
    
    # 处理坐标值，确保它们是元组而不是列表
    if 'text_box_topleft' in config_data and isinstance(config_data['text_box_topleft'], list):
        config_data['text_box_topleft'] = tuple(config_data['text_box_topleft'])
    
    if 'image_box_bottomright' in config_data and isinstance(config_data['image_box_bottomright'], list):
        config_data['image_box_bottomright'] = tuple(config_data['image_box_bottomright'])
    
    # 规范化文件路径，确保跨平台兼容（将 \\ 转换为当前系统的路径分隔符）
    def normalize_path(path: str) -> str:
        """将路径中的反斜杠转换为当前系统的路径分隔符"""
        if isinstance(path, str):
            # 将 Windows 风格的反斜杠转换为当前系统的路径分隔符
            normalized = path.replace('\\', os.sep)
            return os.path.normpath(normalized)
        return path
    
    path_fields = ['font_file', 'baseimage_file', 'base_overlay_file']
    for field in path_fields:
        if field in config_data and isinstance(config_data[field], str):
            config_data[field] = normalize_path(config_data[field])
    
    # 规范化 baseimage_mapping 中的所有路径
    if 'baseimage_mapping' in config_data and isinstance(config_data['baseimage_mapping'], dict):
        normalized_mapping = {}
        for key, value in config_data['baseimage_mapping'].items():
            if isinstance(value, str):
                normalized_mapping[key] = normalize_path(value)
            else:
                normalized_mapping[key] = value
        config_data['baseimage_mapping'] = normalized_mapping
    
    # 创建并返回配置对象
    return Config(**config_data)