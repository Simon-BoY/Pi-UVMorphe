"""
配置模块 - 包含项目配置和路径设置
"""

import os
import torch
from pathlib import Path

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent

# 数据目录
DATA_DIR = PROJECT_ROOT / 'data'
RAW_DATA_DIR = DATA_DIR / 'raw'
PROCESSED_DATA_DIR = DATA_DIR / 'processed'

# 模型目录
MODEL_DIR = PROJECT_ROOT / 'models' / 'checkpoints'

# 输出目录
OUTPUT_DIR = PROJECT_ROOT / 'output'
TEMP_DIR = PROJECT_ROOT / 'temp'

# 默认配置
DEFAULT_CONFIG = {
    'device': 'cuda' if torch.cuda.is_available() else 'cpu',
    'batch_size': 64,
    'image_size': (224, 224),
    'ppm': 5,
    'num_classes': 2
}

# 模型配置
MODEL_CONFIG = {
    'tabular_input_dim': 4,
    'tabular_hidden_dims': [64, 32],
    'image_size': 224,
    'patch_size': 32,
    'vit_dim': 384,
    'vit_depth': 6,
    'vit_heads': 6,
    'vit_mlp_dim': 1536,
    'num_classes': 2
}

def ensure_directories():
    """确保所有必要的目录存在"""
    for dir_path in [DATA_DIR, RAW_DATA_DIR, PROCESSED_DATA_DIR,
                     MODEL_DIR, OUTPUT_DIR, TEMP_DIR]:
        dir_path.mkdir(parents=True, exist_ok=True)
    print("✓ 所有目录已准备就绪")

__all__ = [
    'PROJECT_ROOT',
    'DATA_DIR',
    'RAW_DATA_DIR',
    'PROCESSED_DATA_DIR',
    'MODEL_DIR',
    'OUTPUT_DIR',
    'TEMP_DIR',
    'DEFAULT_CONFIG',
    'MODEL_CONFIG',
    'ensure_directories'
]