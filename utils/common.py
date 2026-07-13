import numpy as np


def cal_ppm(mz1, mz2):
    """计算ppm误差"""
    return ((mz1 - mz2) / mz2) * 1e6


def cal_mz(mz, ppm):
    """根据ppm计算mz"""
    return mz / (1 + ppm / 1e6)


def mz_tolerance(mz, ppm):
    """计算mz容差范围"""
    left = mz / (1 + ppm / 1e6)
    right = mz + mz * ppm / 1e6
    return [left, right]


def get_fixed_mod_list_name(mod_list):
    """从mod_list返回固定修饰名称"""
    mod_name_list = []
    for mods in mod_list:
        for mod in mods:
            mod_name_list.append(mod.name)
    return "|".join(mod_name_list)


def get_unloc_mod_list_name(mod_list):
    """从mod_list返回非固定修饰名称"""
    mod_name_list = []
    for mod in mod_list:
        mod_name_list.append(mod.name)
    return "|".join(mod_name_list)