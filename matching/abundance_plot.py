"""
丰度条形图模块 - 绘制碎片离子丰度分布图
"""

import os
import copy
import numpy as np
import pandas as pd
import plotly.express as px
from plotly.offline import plot


def get_TIC(ions_df) -> float:
    """计算总离子流强度"""
    return np.sum(ions_df["Intensity"])


def get_terminal_frag_df(ions_df, seqLen):
    """筛选末端断裂：Start AA 为 1 (N端) 或 End AA 为序列长度 (C端)"""
    return ions_df[(ions_df["Start AA"] == 1) | (ions_df["End AA"] == seqLen)].copy()


def get_internal_frag_df(ions_df, seqLen):
    """筛选内部中间断裂：两头都不靠"""
    return ions_df[(ions_df["Start AA"] > 1) & (ions_df["End AA"] < seqLen)].copy()


def get_terminal_relative_AA_site(ions_df, seqLen):
    """获取终端相对氨基酸位置"""
    AA_site_series = pd.Series(0.0, index=ions_df.index, dtype=float)
    N_ions_df = ions_df[ions_df["Start AA"] == 1]
    C_ions_df = ions_df[ions_df["End AA"] == seqLen]
    AA_site_series[N_ions_df.index] = N_ions_df["End AA"].astype(float)
    AA_site_series[C_ions_df.index] = C_ions_df["Start AA"].astype(float) - 1
    return AA_site_series


def get_terminal_abundance_fig(ions_df, seqLen):
    """生成终端丰度条形图"""
    fig = px.bar(ions_df, x="Backbone position", y="Intensity", color="Frag Type")
    fig.update_xaxes(
        showline=True,
        linewidth=2,
        linecolor='black',
        mirror=True,
        title_font=dict(size=25),
        tickfont=dict(size=25)
    )
    fig.update_xaxes(range=[0, seqLen])
    fig.update_yaxes(
        showline=True,
        linewidth=2,
        linecolor='black',
        mirror=True,
        title_font=dict(size=25),
        tickfont=dict(size=25),
        showticklabels=True
    )
    fig.update_layout(
        title_font_family='Arial',
        title_x=0.5,
        title_font=dict(size=25),
        legend_font=dict(size=25)
    )
    fig.update_layout(template='seaborn', plot_bgcolor='white')
    fig.update_traces(marker=dict(pattern_solidity=0.4, pattern_fgcolor='black'))
    return fig


def split_internal_to_terminal(internal_ions_df_i, seqLen):
    """
    将内部碎片拆分为N端和C端碎片

    Parameters:
    -----------
    internal_ions_df_i : pd.Series
        单个内部碎片行
    seqLen : int
        序列长度

    Returns:
    --------
    tuple
        (C端碎片DataFrame, N端碎片DataFrame)
    """
    ion_type = str(internal_ions_df_i["Frag Type"])
    C_ion_type = ion_type[0] if len(ion_type) > 0 else 'unknown'
    N_ion_type = ion_type[1] if len(ion_type) > 1 else ion_type[0]

    C_ions_df_i = copy.deepcopy(internal_ions_df_i)
    N_ions_df_i = copy.deepcopy(internal_ions_df_i)

    C_ions_df_i["Frag Type"] = C_ion_type
    C_ions_df_i["End AA"] = internal_ions_df_i["Start AA"] - 1
    C_ions_df_i["Start AA"] = 1

    N_ions_df_i["Frag Type"] = N_ion_type
    N_ions_df_i["Start AA"] = internal_ions_df_i["End AA"] + 1
    N_ions_df_i["End AA"] = seqLen

    return pd.DataFrame([C_ions_df_i]), pd.DataFrame([N_ions_df_i])


def fragment_abundance_plot_main(workplace_dir, ions_df, seq, filename_suffix=""):
    """
    绘制碎片丰度条形图主函数

    Parameters:
    -----------
    workplace_dir : str
        输出目录
    ions_df : pd.DataFrame
        离子匹配结果DataFrame
    seq : str
        蛋白质序列
    filename_suffix : str
        文件名后缀（用于区分不同文件）
    """
    seqLen = len(seq)

    # 确保输出目录存在
    os.makedirs(workplace_dir, exist_ok=True)

    # --- 处理末端碎片 ---
    terminal_frag_df = get_terminal_frag_df(ions_df, seqLen)
    if not terminal_frag_df.empty:
        terminal_frag_df = terminal_frag_df.sort_values("Frag Type")
        terminal_relative_AA_site = get_terminal_relative_AA_site(terminal_frag_df, seqLen)
        terminal_frag_df["Backbone position"] = terminal_relative_AA_site

        terminal_abundance_fig = get_terminal_abundance_fig(terminal_frag_df, seqLen)
        plot(
            terminal_abundance_fig,
            filename=os.path.join(workplace_dir, f"bar_plot_terminal_{filename_suffix}.html"),
            auto_open=False,
            include_plotlyjs=True
        )
        print(f"✓ saved: bar_plot_terminal_{filename_suffix}.html")

    # --- 处理内部碎片 ---
    internal_frag_df = get_internal_frag_df(ions_df, seqLen)
    if not internal_frag_df.empty:
        split_internal_list = []

        # 拆分内部碎片
        for _, internal_frag_df_i in internal_frag_df.iterrows():
            split_i_1, split_i_2 = split_internal_to_terminal(internal_frag_df_i, seqLen)
            split_internal_list.extend([split_i_1, split_i_2])

        # 统一合并
        split_internal_df = pd.concat(split_internal_list, ignore_index=True)

        internal_relative_AA_site = get_terminal_relative_AA_site(split_internal_df, seqLen)
        split_internal_df["Backbone position"] = internal_relative_AA_site

        internal_abundance_fig = get_terminal_abundance_fig(
            split_internal_df.sort_values("Frag Type"),
            seqLen
        )
        plot(
            internal_abundance_fig,
            filename=os.path.join(workplace_dir, f"bar_plot_internal_{filename_suffix}.html"),
            auto_open=False,
            include_plotlyjs=True
        )
        print(f"✓ saved: bar_plot_internal_{filename_suffix}.html")

    if terminal_frag_df.empty and internal_frag_df.empty:
        print("⚠ skipped")