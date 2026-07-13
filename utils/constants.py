"""
常量定义模块 - 包含离子类型颜色映射、离子类型列表等
"""

# =========================================================
# 离子类型颜色映射 (用于裂解图谱可视化)
# =========================================================
ION_TYPE_COLOR_MAP = {
    "red": ["a", "a+1", "a-1", "x", "x+1", "x-1"],
    "green": ["b", "y", "y-1", "y-2"],
    "blue": ["c", "c.", "z", "z+1", "z-1"]
}

# 反向映射：离子类型 -> 颜色
ION_TYPE_TO_COLOR = {}
for color, ion_types in ION_TYPE_COLOR_MAP.items():
    for ion_type in ion_types:
        ION_TYPE_TO_COLOR[ion_type] = color

# =========================================================
# 离子类型分类 (用于碎片匹配)
# =========================================================

# N端离子类型
N_TERM_ION_TYPES = ["a", "a-1", "a+1", "b", "c"]

# C端离子类型
C_TERM_ION_TYPES = ["x", "x-1", "x+1", "y", "y-1", "y-2", "z", "z-1", "z+1"]

# 内部离子类型
INTERNAL_ION_TYPES = ["ax", "ay", "az", "bx", "by", "bz", "cx", "cy", "cz"]

# 所有有效离子类型
ALL_ION_TYPES = list(set(N_TERM_ION_TYPES + C_TERM_ION_TYPES + INTERNAL_ION_TYPES))

# =========================================================
# 修饰类型常量
# =========================================================

# N端修饰
N_TERM_MODIFICATIONS = {
    "acetylated": {
        "name": "Acetylated",
        "short_name": "ac-",
        "mass": 42.0105646837,
        "formula": "C2H2O",
        "position": "N-term"
    },
    "deaminated": {
        "name": "Deaminated",
        "short_name": "deam-",
        "mass": 0.984016,
        "formula": "H-1N-1O",
        "position": "N-term"
    },
    "methylated": {
        "name": "Methylated",
        "short_name": "me-",
        "mass": 14.01565,
        "formula": "CH2",
        "position": "N-term"
    },
    "dimethylated": {
        "name": "Dimethylated",
        "short_name": "dime-",
        "mass": 28.0313,
        "formula": "C2H4",
        "position": "N-term"
    },
    "formylated": {
        "name": "Formylated",
        "short_name": "form-",
        "mass": 27.9949,
        "formula": "CO",
        "position": "N-term"
    }
}

# C端修饰
C_TERM_MODIFICATIONS = {
    "amided": {
        "name": "Amided",
        "short_name": "amide-",
        "mass": -0.984016,
        "formula": "HN1O-1",
        "position": "C-term"
    },
    "c_methylated": {
        "name": "Methylated (C-term)",
        "short_name": "cme-",
        "mass": 14.01565,
        "formula": "CH2",
        "position": "C-term"
    },
    "dehydrated": {
        "name": "Dehydrated",
        "short_name": "dehyd-",
        "mass": -18.010565,
        "formula": "H-2O-1",
        "position": "C-term"
    }
}

# 合并所有修饰
ALL_MODIFICATIONS = {**N_TERM_MODIFICATIONS, **C_TERM_MODIFICATIONS}

# =========================================================
# 物理常量
# =========================================================

H_ION_MASS = 1.00782503207  # 氢离子质量 (Da)
PROTON_MASS = 1.007276466812  # 质子质量 (Da)
ELECTRON_MASS = 0.000548579909  # 电子质量 (Da)

# =========================================================
# 数据处理常量
# =========================================================

# 默认表格特征列
DEFAULT_TABULAR_COLUMNS = ['Mass', 'Intensity', 'Charge', 'mz']

# 默认图片尺寸 (ViT输入)
DEFAULT_IMAGE_SIZE = (224, 224)

# 默认ppm容差
DEFAULT_PPM = 5

# 默认MGF光谱信息长度
DEFAULT_SPECTRA_INFO_LENGTH = 14

# =========================================================
# 氨基酸质量 (用于快速查找)
# =========================================================

AMINO_ACID_MASSES = {
    'A': 71.037113805,  # Alanine
    'R': 156.101111050,  # Arginine
    'N': 114.042927470,  # Asparagine
    'D': 115.026943065,  # Aspartic acid
    'C': 103.009184505,  # Cysteine
    'E': 129.042593095,  # Glutamic acid
    'Q': 128.058577505,  # Glutamine
    'G': 57.021463735,  # Glycine
    'H': 137.058911875,  # Histidine
    'I': 113.084064015,  # Isoleucine
    'L': 113.084064015,  # Leucine
    'K': 128.094963015,  # Lysine
    'M': 131.040484645,  # Methionine
    'F': 147.068413945,  # Phenylalanine
    'P': 97.052763875,  # Proline
    'S': 87.032028435,  # Serine
    'T': 101.047678465,  # Threonine
    'W': 186.079312980,  # Tryptophan
    'Y': 163.063328575,  # Tyrosine
    'V': 99.068413945,  # Valine
}

# =========================================================
# 支持类型颜色 (用于IRS可视化)
# =========================================================

IRS_SUPPORT_COLORS = {
    "two_side": "darkgreen",
    "one_side": "darkorange",
    "unsupported": "dimgray"
}

IRS_SUPPORT_LABELS = {
    "two_side": "Two-side supported",
    "one_side": "One-side supported",
    "unsupported": "Unsupported"
}


# =========================================================
# 辅助函数
# =========================================================

def get_ion_color(ion_type: str) -> str:
    """
    根据离子类型获取颜色

    Parameters:
    -----------
    ion_type : str
        离子类型 (如 'a', 'b', 'y'等)

    Returns:
    --------
    str
        颜色名称
    """
    return ION_TYPE_TO_COLOR.get(ion_type, "gray")


def get_modification_info(mod_type: str) -> dict:
    """
    获取修饰信息

    Parameters:
    -----------
    mod_type : str
        修饰类型名称

    Returns:
    --------
    dict
        修饰信息字典
    """
    return ALL_MODIFICATIONS.get(mod_type, {})


def get_amino_acid_mass(aa: str) -> float:
    """
    获取氨基酸质量

    Parameters:
    -----------
    aa : str
        单字母氨基酸代码

    Returns:
    --------
    float
        氨基酸质量 (Da)
    """
    return AMINO_ACID_MASSES.get(aa.upper(), 0.0)


if __name__ == "__main__":
    # 测试常量
    print("=" * 50)
    print("离子类型颜色映射:")
    for ion_type, color in list(ION_TYPE_TO_COLOR.items())[:5]:
        print(f"  {ion_type} -> {color}")

    print("\n可用修饰类型:")
    for mod_name in ALL_MODIFICATIONS.keys():
        print(f"  {mod_name}")

    print("\n默认配置:")
    print(f"  图片尺寸: {DEFAULT_IMAGE_SIZE}")
    print(f"  PPM容差: {DEFAULT_PPM}")
    print(f"  表格特征列: {DEFAULT_TABULAR_COLUMNS}")