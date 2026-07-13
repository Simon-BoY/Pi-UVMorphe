"""
可视化模块 - 包含裂解图谱绘制功能
"""

import numpy as np
import pandas as pd
import copy
import plotly.graph_objects as go
from plotly.offline import plot

from utils.constants import ION_TYPE_COLOR_MAP
from matching.post_processing import get_terminal_frag_df, get_internal_frag_df


def get_seq_trace_cor(seq) -> tuple:
    """
    获取序列在二维网格上的坐标

    Parameters:
    -----------
    seq : str
        蛋白质序列

    Returns:
    --------
    tuple
        (x坐标数组, y坐标数组)
    """
    width = 25
    high = 10
    seqLen = len(seq)
    real_high = int(seqLen / width) + 1
    x_cor_arr = np.tile(np.arange(width), real_high)
    x_cor_arr = x_cor_arr[:seqLen]
    y_cor_arr = np.reshape(np.tile(np.array(list(reversed(np.arange(real_high)))), width), [width, real_high]).T
    y_cor_arr = np.reshape((y_cor_arr), [-1])
    y_cor_arr = y_cor_arr[:seqLen]
    return x_cor_arr, y_cor_arr


def get_seq_trace(seq, x_cor_arr, y_cor_arr) -> go.Scatter:
    """生成序列文本轨迹"""
    seq_list = ['<b>' + aa + '<b>' for aa in seq]
    seqLen = len(seq)
    site_num = list(np.arange(seqLen) + 1)
    hovertext = [AA + str(site_num_i) for AA, site_num_i in zip(list(seq), site_num)]
    seq_trace = go.Scatter(
        x=x_cor_arr,
        y=y_cor_arr,
        mode="text",
        text=seq_list,
        textfont=dict(family='Arial', size=40),
        textposition="middle center",
        hovertext=hovertext,
        hoverinfo="text"
    )
    return seq_trace


def get_terminal_seg_trace_cor(ions_df_i, seqLen, x_cor_arr, y_cor_arr) -> tuple:
    """获取终端离子片段坐标"""
    start = ions_df_i["Start AA"]
    end = ions_df_i["End AA"]
    ion_type = ions_df_i["Frag Type"]
    if start == 1 and end < seqLen:
        abs_site = end
        x = x_cor_arr[abs_site - 1] + 0.5
        y = y_cor_arr[abs_site - 1] + 0.08
        return x, y
    elif start > 1 and end == seqLen:
        abs_site = start
        x = x_cor_arr[abs_site - 1] - 0.5
        y = y_cor_arr[abs_site - 1] + 0.08
        return x, y
    else:
        raise ValueError(f"error {ion_type}, start={start}, end={end}")


def get_terminal_seg_trace(ions_df_i, x, y) -> go.Scatter:
    """生成终端离子片段标记"""
    ion_type = ions_df_i["Frag Type"]
    color = None
    for key, value in ION_TYPE_COLOR_MAP.items():
        if ion_type in value:
            color = key
            break
    if color is None:
        raise ValueError(f"error: {ion_type}")

    seg_trace = go.Scatter(
        x=[x],
        y=[y],
        mode='markers',
        marker=dict(symbol='line-ns', color=color, size=25, line=dict(color=color, width=4)),
        hoverinfo='skip',
        name=ion_type
    )
    return seg_trace


def get_internal_seg_trace_cor(ions_df_i, x_cor_arr, y_cor_arr) -> np.ndarray:
    """获取内部离子片段坐标"""
    start = ions_df_i["Start AA"]
    end = ions_df_i["End AA"]
    cor_array = np.zeros(shape=[2, 2])
    N_x = x_cor_arr[start - 1] - 0.5
    N_y = y_cor_arr[start - 1] + 0.08
    C_x = x_cor_arr[end - 1] + 0.5
    C_y = y_cor_arr[end - 1] + 0.08
    cor_array[0, 0] = N_x
    cor_array[0, 1] = N_y
    cor_array[1, 0] = C_x
    cor_array[1, 1] = C_y
    return cor_array


def get_internal_seg_trace(ions_df_i, x_cor_arr, y_cor_arr) -> go.Scatter:
    """生成内部离子片段标记"""
    start = ions_df_i["Start AA"]
    end = ions_df_i["End AA"]
    ion_type = ions_df_i["Frag Type"]
    Error = round(ions_df_i["Error"], 4)
    PCC = round(ions_df_i.get("adjust_PCC", 0), 4)
    exp_mass = round(ions_df_i["Observed Mass"], 4)
    the_mass = round(ions_df_i["Theoretical Mass"], 4)
    Charge = int(ions_df_i["Charge"])
    Intensity = round(ions_df_i["Intensity"], 4)
    mz = round(ions_df_i["mz"], 4)

    cor_array = get_internal_seg_trace_cor(ions_df_i, x_cor_arr, y_cor_arr)
    trace = go.Scatter(
        x=cor_array[:, 0],
        y=cor_array[:, 1],
        mode='markers',
        marker=dict(symbol='line-ns', color="purple", size=25, line=dict(color="purple", width=4)),
        hovertemplate=(
            f'Observed Mass: {exp_mass}Da<br><br>'
            f'AA range: {start},{end}<br>'
            f'Ion Type: {ion_type}<br>'
            f'Theoretical Mass: {the_mass}Da<br>'
            f'PCC: {PCC}<br>'
            f'Error: {Error}ppm<br>'
            f'Charge: {Charge}<br>'
            f'Intensity: {Intensity}<br>'
            f'mz: {mz}<br><extra></extra>'
        ),
        hoveron="points+fills",
        name=ion_type
    )
    return trace


def internal_seg_trace_constructor(ions_df_i, x_cor_arr, y_cor_arr) -> go.Scatter:
    """内部离子片段构造器"""
    return get_internal_seg_trace(ions_df_i, x_cor_arr, y_cor_arr)


def get_terminal_ion_trace(ions_df_i, x, y) -> go.Scatter:
    """生成终端离子标记"""
    ion_type = ions_df_i["Frag Type"]
    Error = round(ions_df_i["Error"], 4)
    PCC = round(ions_df_i.get("adjust_PCC", 0), 4)
    exp_mass = round(ions_df_i["Observed Mass"], 4)
    the_mass = round(ions_df_i["Theoretical Mass"], 4)
    Charge = int(ions_df_i["Charge"])
    Intensity = round(ions_df_i["Intensity"], 4)
    mz = round(ions_df_i["mz"], 4)

    color = None
    for key, value in ION_TYPE_COLOR_MAP.items():
        if ion_type in value:
            color = key
            break
    if color is None:
        raise ValueError(f"error: {ion_type}")

    # 根据离子类型设置位置和角度
    if ion_type in ["a", "a+1", "a-1"]:
        ion_trace_x = x - 0.1
        ion_trace_y = y + 0.265
        angle = 0
        size = 10
    elif ion_type in ["x", "x+1", "x-1"]:
        ion_trace_x = x + 0.1
        ion_trace_y = y - 0.265
        angle = 0
        size = 10
    elif ion_type in ["b"]:
        ion_trace_x = x - 0.11
        ion_trace_y = y + 0.35
        angle = 30
        size = 12
    elif ion_type in ["y", "y-1", "y-2"]:
        ion_trace_x = x + 0.11
        ion_trace_y = y - 0.35
        angle = 30
        size = 12
    elif ion_type in ["c", "c."]:
        ion_trace_x = x - 0.08
        ion_trace_y = y + 0.39
        angle = 60
        size = 13
    elif ion_type in ["z", "z+1", "z-1"]:
        ion_trace_x = x + 0.08
        ion_trace_y = y - 0.39
        angle = 60
        size = 13
    else:
        raise ValueError(f"error {ion_type}")

    ion_trace = go.Scatter(
        x=[ion_trace_x],
        y=[ion_trace_y],
        mode='markers',
        name=None,
        customdata=[ion_trace_x, ion_trace_y, angle, ion_type, the_mass, PCC, Error, Charge, Intensity, mz],
        marker=dict(
            symbol='line-ew',
            color=color,
            angle=angle,
            size=size,
            line=dict(color=color, width=4)
        ),
        hovertemplate=(
            f'Observed Mass: {exp_mass}Da<br><br>'
            f'Ion Type: {ion_type}<br>'
            f'Theoretical Mass: {the_mass}Da<br>'
            f'PCC: {PCC}<br>'
            f'Error: {Error}ppm<br>'
            f'Charge: {Charge}<br>'
            f'Intensity: {Intensity}<br>'
            f'mz: {mz}<br>'
        )
    )
    return ion_trace


def terminal_ion_trace_constructor(ions_df_i, seqLen, x_cor_arr, y_cor_arr) -> go.Scatter:
    """终端离子构造器"""
    seg_trace_x, seg_trace_y = get_terminal_seg_trace_cor(ions_df_i, seqLen, x_cor_arr, y_cor_arr)
    return get_terminal_ion_trace(ions_df_i, seg_trace_x, seg_trace_y)


def terminal_seg_trace_constructor(ions_df_i, seqLen, x_cor_arr, y_cor_arr) -> go.Scatter:
    """终端片段构造器"""
    seg_trace_x, seg_trace_y = get_terminal_seg_trace_cor(ions_df_i, seqLen, x_cor_arr, y_cor_arr)
    return get_terminal_seg_trace(ions_df_i, seg_trace_x, seg_trace_y)


def post_process_ion_trace(ion_trace_list):
    """后处理离子轨迹排序"""
    return list(sorted(ion_trace_list, key=lambda x: x.marker.angle, reverse=True))


def post_process_seg_trace(seg_trace_list):
    """后处理片段轨迹排序"""
    return list(sorted(seg_trace_list, key=lambda x: x.name, reverse=True))


def merge_overlap_ion_trace(ion_trace_list):
    """合并重叠的离子轨迹"""
    if not ion_trace_list:
        return []

    tmp_list = []
    for trace in ion_trace_list:
        tmp_trace = copy.deepcopy(trace)
        for trace_2 in ion_trace_list:
            if trace is trace_2:
                pass
            else:
                if (trace.customdata[0] == trace_2.customdata[0] and
                        trace.customdata[1] == trace_2.customdata[1] and
                        trace.customdata[2] == trace_2.customdata[2]):
                    ion_type = trace_2.customdata[3]
                    the_mass = trace_2.customdata[4]
                    PCC = trace_2.customdata[5]
                    Error = trace_2.customdata[6]
                    Charge = trace_2.customdata[7]
                    Intensity = trace_2.customdata[8]
                    mz = trace_2.customdata[9]
                    tmp_trace.hovertemplate += (
                        '<br>'
                        f'Ion Type: {ion_type}<br>'
                        f'Theoretical Mass: {the_mass}Da<br>'
                        f'PCC: {PCC}<br>'
                        f'Error: {Error}ppm<br>'
                        f'Charge: {Charge}<br>'
                        f'Intensity: {Intensity}<br>'
                        f'mz: {mz}<br>'
                    )
        tmp_trace.hovertemplate += '<extra></extra>'
        tmp_list.append(tmp_trace)
    return tmp_list


def get_fig_size(x_cor_arr, y_cor_arr):
    """计算图形尺寸"""
    height_px_ori = 864
    width_px_ori = 1679
    height_tick_ori = 11
    width_tick_ori = 25

    height_fold = int(max(y_cor_arr) / height_tick_ori) + 1

    final_height_px = height_px_ori * height_fold
    final_width_px = width_px_ori
    y_tick_limit = height_fold * height_tick_ori
    x_tick_limit = width_tick_ori
    return final_width_px, final_height_px, y_tick_limit, x_tick_limit


def seg_map_plot_main(workplace_dir, ions_df, seq):
    """
    绘制裂解图谱主函数

    Parameters:
    -----------
    workplace_dir : str
        输出目录
    ions_df : pd.DataFrame
        离子匹配结果DataFrame
    seq : str
        蛋白质序列
    """
    import os

    # 确保输出目录存在
    os.makedirs(workplace_dir, exist_ok=True)

    # 检查输入数据
    if ions_df is None or ions_df.empty:
        print("⚠ skipped")
        return

    seqLen = len(seq)
    x_cor_arr, y_cor_arr = get_seq_trace_cor(seq)
    fig_width, fig_height, y_tick_limit, x_tick_limit = get_fig_size(x_cor_arr, y_cor_arr)

    xaxis = go.layout.XAxis(ticks='', showticklabels=False, showline=False, range=[-1, x_tick_limit + 1])
    yaxis = go.layout.YAxis(ticks='', showticklabels=False, showline=False, range=[-1, y_tick_limit])
    layout = go.Layout(
        template='simple_white',
        showlegend=False,
        xaxis=xaxis,
        yaxis=yaxis,
        height=fig_height,
        width=fig_width
    )

    seq_trace = get_seq_trace(seq, x_cor_arr, y_cor_arr)

    # 终端碎片
    terminal_frag_df = get_terminal_frag_df(ions_df, seqLen)
    if not terminal_frag_df.empty:
        #print(f"  绘制终端碎片: {len(terminal_frag_df)} 个")
        terminal_seg_site_trace = list(
            terminal_frag_df.apply(
                lambda x: terminal_seg_trace_constructor(x, seqLen, x_cor_arr, y_cor_arr),
                axis=1
            )
        )
        terminal_seg_site_trace = post_process_seg_trace(terminal_seg_site_trace)

        terminal_ion_site_trace = list(
            terminal_frag_df.apply(
                lambda x: terminal_ion_trace_constructor(x, seqLen, x_cor_arr, y_cor_arr),
                axis=1
            )
        )
        terminal_ion_site_trace = post_process_ion_trace(terminal_ion_site_trace)
        terminal_ion_site_trace = merge_overlap_ion_trace(terminal_ion_site_trace)

        fig1 = go.Figure(
            terminal_seg_site_trace + terminal_ion_site_trace + [seq_trace],
            layout=layout
        )
        plot(
            fig1,
            filename=os.path.join(workplace_dir, "terminal_fragment_cleavage_map.html"),
            auto_open=False,
            include_plotlyjs=True
        )
        print(f"✓ Saved: {os.path.join(workplace_dir, 'terminal_fragment_cleavage_map.html')}")
    else:
        print("  Done")

    # 内部碎片 - 修复bug
    internal_frag_df = get_internal_frag_df(ions_df, seqLen)
    if not internal_frag_df.empty:
        #print(f"  绘制内部碎片: {len(internal_frag_df)} 个")
        internal_seg_site_trace = list(
            internal_frag_df.apply(
                lambda x: internal_seg_trace_constructor(x, x_cor_arr, y_cor_arr),
                axis=1
            )
        )
        # 修复：使用正确的变量名 internal_seg_site_trace 而不是 internal_seg_trace_constructor
        fig3 = go.Figure(internal_seg_site_trace + [seq_trace], layout=layout)
        plot(
            fig3,
            filename=os.path.join(workplace_dir, "internal_fragment_cleavage_map.html"),
            auto_open=False,
            include_plotlyjs=True
        )
        print(f"✓ Saved: {os.path.join(workplace_dir, 'internal_fragment_cleavage_map.html')}")
    else:
        print("  Done")


def classify_internal_support(row, terminal_cleavages):
    """
    分类内部碎片支持类型

    Returns
    -------
    str
        "two_side", "one_side", "unsupported"
    """
    start = int(row["Start AA"])
    end = int(row["End AA"])

    left_cleavage = start - 1
    right_cleavage = end

    left_support = left_cleavage in terminal_cleavages
    right_support = right_cleavage in terminal_cleavages

    if left_support and right_support:
        return "two_side"
    elif left_support or right_support:
        return "one_side"
    else:
        return "unsupported"


def get_terminal_cleavages(matches_df, seqLen):
    """提取终端裂解位点"""
    terminal_mask = (matches_df["Start AA"] == 1) | (matches_df["End AA"] == seqLen)
    terminal_df = matches_df[terminal_mask].copy()

    terminal_cleavages = set()
    for _, row in terminal_df.iterrows():
        start = int(row["Start AA"])
        end = int(row["End AA"])
        if start == 1:
            terminal_cleavages.add(end)
        if end == seqLen:
            terminal_cleavages.add(start - 1)

    return terminal_cleavages


def get_internal_seg_trace_supported(
        ions_df_i,
        x_cor_arr,
        y_cor_arr,
        terminal_cleavages
):
    """
    内部碎片轨迹（带IRS支持颜色）

    Colors:
        darkgreen: two-side supported
        darkorange: one-side supported
        dimgray: unsupported
    """
    start = ions_df_i["Start AA"]
    end = ions_df_i["End AA"]
    ion_type = ions_df_i["Frag Type"]

    Error = round(ions_df_i["Error"], 4)
    PCC = round(ions_df_i.get("adjust_PCC", 0), 4)
    exp_mass = round(ions_df_i["Observed Mass"], 4)
    the_mass = round(ions_df_i["Theoretical Mass"], 4)
    Charge = int(ions_df_i["Charge"])
    Intensity = round(ions_df_i["Intensity"], 4)
    mz = round(ions_df_i["mz"], 4)

    # 支持类型
    support_type = classify_internal_support(ions_df_i, terminal_cleavages)

    if support_type == "two_side":
        color = "darkgreen"
    elif support_type == "one_side":
        color = "darkorange"
    else:
        color = "dimgray"

    # 坐标
    cor_array = get_internal_seg_trace_cor(ions_df_i, x_cor_arr, y_cor_arr)

    trace = go.Scatter(
        x=cor_array[:, 0],
        y=cor_array[:, 1],
        mode='markers',
        marker=dict(
            symbol='line-ns',
            color=color,
            size=25,
            line=dict(color=color, width=4)
        ),
        hovertemplate=(
            f'Support Type: {support_type}<br><br>'
            f'Observed Mass: {exp_mass}Da<br><br>'
            f'AA range: {start},{end}<br>'
            f'Ion Type: {ion_type}<br>'
            f'Theoretical Mass: {the_mass}Da<br>'
            f'PCC: {PCC}<br>'
            f'Error: {Error}ppm<br>'
            f'Charge: {Charge}<br>'
            f'Intensity: {Intensity}<br>'
            f'mz: {mz}<br><extra></extra>'
        ),
        hoveron="points+fills",
        name=support_type
    )
    return trace


def internal_seg_trace_constructor_supported(
        ions_df_i,
        x_cor_arr,
        y_cor_arr,
        terminal_cleavages
):
    """内部碎片支持轨迹构造器"""
    return get_internal_seg_trace_supported(
        ions_df_i, x_cor_arr, y_cor_arr, terminal_cleavages
    )


def plot_internal_fragment_support_map(
        workplace_dir,
        ions_df,
        seq
):
    """
    绘制内部碎片支持图谱（带IRS颜色标记）
    """
    import os

    os.makedirs(workplace_dir, exist_ok=True)

    # 检查输入数据
    if ions_df is None or ions_df.empty:
        #print("⚠ 没有匹配数据，跳过支持图谱绘制")
        return

    seqLen = len(seq)

    # 坐标
    x_cor_arr, y_cor_arr = get_seq_trace_cor(seq)
    fig_width, fig_height, y_tick_limit, x_tick_limit = get_fig_size(x_cor_arr, y_cor_arr)

    xaxis = go.layout.XAxis(
        ticks='',
        showticklabels=False,
        showline=False,
        range=[-1, x_tick_limit + 1]
    )

    yaxis = go.layout.YAxis(
        ticks='',
        showticklabels=False,
        showline=False,
        range=[-1, y_tick_limit]
    )

    layout = go.Layout(
        template='simple_white',
        showlegend=True,
        xaxis=xaxis,
        yaxis=yaxis,
        height=fig_height,
        width=fig_width
    )

    # 序列轨迹
    seq_trace = get_seq_trace(seq, x_cor_arr, y_cor_arr)

    # 内部碎片
    internal_frag_df = get_internal_frag_df(ions_df, seqLen)

    if internal_frag_df.empty:
        #print("⚠ 没有内部碎片，跳过支持图谱绘制")
        return

    #print(f"  绘制内部支持图谱: {len(internal_frag_df)} 个内部碎片")

    # 终端裂解位点
    terminal_cleavages = get_terminal_cleavages(ions_df, seqLen)
    #print(f"  终端裂解位点数: {len(terminal_cleavages)}")

    # 轨迹
    internal_seg_site_trace = list(
        internal_frag_df.apply(
            lambda x: internal_seg_trace_constructor_supported(
                x, x_cor_arr, y_cor_arr, terminal_cleavages
            ),
            axis=1
        )
    )

    # 图例去重
    shown_legend = set()
    for trace in internal_seg_site_trace:
        if trace.name in shown_legend:
            trace.showlegend = False
        else:
            trace.showlegend = True
            shown_legend.add(trace.name)

    seq_trace.showlegend = False

    # 绘图
    fig = go.Figure(internal_seg_site_trace + [seq_trace], layout=layout)

    output_path = os.path.join(workplace_dir, "internal_fragment_support_map.html")
    plot(
        fig,
        filename=output_path,
        auto_open=False,
        include_plotlyjs=True
    )
    print(f"✓ Saved: {output_path}")