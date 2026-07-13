import numpy as np
import pandas as pd
import copy


def get_terminal_frag_df(ions_df, seqLen):
    """获取终端离子碎片"""
    ions_df = copy.deepcopy(ions_df)
    flag_index = ions_df[["Start AA", "End AA"]] == np.array([1, seqLen])
    return ions_df[np.any(flag_index, axis=1)]


def get_internal_frag_df(ions_df, seqLen):
    """获取内部离子碎片"""
    ions_df = copy.deepcopy(ions_df)
    flag_index = ions_df[["Start AA", "End AA"]] != np.array([1, seqLen])
    return ions_df[np.all(flag_index, axis=1)]


def get_low_Error_df(ions_df):
    """获取误差最小的离子"""
    lowest_er = sorted(abs(ions_df["Error"]))[0]
    return ions_df[abs(ions_df["Error"]) == lowest_er]


def process_terminal_rep_match(ions_df):
    """处理终端重复匹配"""
    return get_low_Error_df(ions_df)


def process_rep_match(ions_df, seqLen):
    """按策略处理重复匹配"""
    terminal_df = get_terminal_frag_df(ions_df, seqLen)
    internal_df = get_internal_frag_df(ions_df, seqLen)

    if len(terminal_df) == 1:
        return terminal_df
    elif len(terminal_df) > 1:
        return process_terminal_rep_match(terminal_df)

    if len(internal_df) == 1:
        return internal_df
    elif len(internal_df) > 1:
        return process_terminal_rep_match(internal_df)

    return internal_df


def post_process(ions_df, seqLen):
    """后处理：去重和过滤"""
    all_columns = ions_df.columns
    group_columns = ['Observed Mass', "Intensity", "Charge", "mz"]

    g = ions_df.groupby(group_columns)
    result_list = []

    for name, _ in g:
        group_ions_df = g.get_group(name)
        if len(group_ions_df) == 1:
            tmp_ions_df = group_ions_df
        else:
            tmp_ions_df = process_rep_match(group_ions_df, seqLen)
        result_list.append(tmp_ions_df)

    if result_list:
        final_df = pd.concat(result_list, ignore_index=True)
        if not final_df.empty:
            global_min_start = final_df["Start AA"].min()
            global_max_end = final_df["End AA"].max()
            cond_to_drop = (final_df["Start AA"] > global_min_start) & (final_df["End AA"] < global_max_end) & (final_df["label"] == 0)
            final_df = final_df[~cond_to_drop]
        return final_df
    else:
        return pd.DataFrame(columns=all_columns)


def get_cleavage_coverage(filtered_df, seqLen):
    """计算片段覆盖率"""
    if filtered_df.empty:
        return 0.0, "0.00%"

    start_col = "Start_AA" if "Start_AA" in filtered_df.columns else "Start AA"
    end_col = "End_AA" if "End_AA" in filtered_df.columns else "End AA"

    seg_site_arr = np.zeros(shape=seqLen - 1, dtype=int)

    for _, row in filtered_df.iterrows():
        start = int(row[start_col])
        end = int(row[end_col])

        if start == 1 and end < seqLen:
            seg_site_arr[end - 1] += 1
        elif start > 1 and end == seqLen:
            seg_site_arr[start - 2] += 1
        elif start > 1 and end < seqLen:
            seg_site_arr[end - 1] += 1
            seg_site_arr[start - 2] += 1

    covered_sites_count = np.sum(seg_site_arr > 0)
    total_possible_sites = len(seg_site_arr)
    coverage_ratio = covered_sites_count / total_possible_sites
    coverage_str = f"{coverage_ratio * 100:.2f}%"

    return coverage_ratio, coverage_str