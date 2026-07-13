import json
import re


def parse_spectrum_js(filepath):
    """解析spectrum0.js文件，提取envelopes数据"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    match = re.search(r'ms2_data\s*=\s*({.*});?\s*$', content, re.DOTALL)

    data = json.loads(match.group(1))
    return data