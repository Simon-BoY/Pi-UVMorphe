import numpy as np
import pandas as pd
import copy
from utils.common import *

def extract_ms_info_from_mgf(file, spectra_info_length=14, h_ion_mass=1.00782503207):
    """从MGF文件中提取质谱信息"""
    fulltxt = file.read()
    fulltxt_list = fulltxt.split("\n")
    fulltxt_list = np.asarray(fulltxt_list)

    StartIndex = np.argwhere(fulltxt_list == 'BEGIN IONS')
    EndIndex = np.argwhere(fulltxt_list == 'END IONS')
    DeconvIonInfoRange = np.hstack([StartIndex, EndIndex])

    mono_list = []
    for i in DeconvIonInfoRange:
        i_range = range(i[0] + spectra_info_length, i[1])
        mono_list.append(fulltxt_list[i_range])

    mono_arr = []
    for mono_list_i in mono_list:
        mono_arr.append(np.asarray(list(map(lambda x: x.split("\t"), mono_list_i))).astype(float))
    mono_arr = np.asarray(mono_arr, dtype="object")

    spectra_dfs = []
    for spec_num_i in range(len(mono_arr)):
        tmp_arr = copy.deepcopy(mono_arr[spec_num_i])
        mz_arr = tmp_arr[:, 0] / tmp_arr[:, 2] + h_ion_mass
        tmp_arr[:, 0] += h_ion_mass
        tmp_arr = np.hstack([tmp_arr, mz_arr[:, np.newaxis]])
        df = pd.DataFrame(tmp_arr, columns=["Mass", "Intensity", "Charge", "mz"])
        spectra_dfs.append(df)

    return mono_arr, spectra_dfs


def find_intersection(dfs, mz_col='mz', ppm=5, min_matched=2):
    """找到多个质谱数据在指定ppm范围内的m/z交集"""

    matched_indices_per_df = [set() for _ in range(len(dfs))]
    base_df = dfs[0].copy()
    matches = []

    for idx, row in base_df.iterrows():
        base_mz = row[mz_col]
        base_mass = row.get('Mass', None)
        matched_mzs = [base_mz]
        matched_masses = [base_mass]
        matched_sources = [0]
        matched_original_indices = [idx]

        for i in range(1, len(dfs)):
            current_df = dfs[i]
            tolerance = base_mz * ppm / 1e6
            mz_diff = (current_df[mz_col] - base_mz).abs()
            min_diff_idx = mz_diff.idxmin()
            min_diff = mz_diff[min_diff_idx]

            if min_diff <= tolerance:
                matched_mzs.append(current_df.loc[min_diff_idx, mz_col])
                matched_mass = current_df.loc[min_diff_idx, 'Mass'] if 'Mass' in current_df.columns else None
                matched_masses.append(matched_mass)
                matched_sources.append(i)
                matched_original_indices.append(min_diff_idx)

        if len(matched_mzs) >= min_matched:
            match_info = {
                mz_col: base_mz,
                'mz_average': sum(matched_mzs) / len(matched_mzs),
                'matched_count': len(matched_mzs),
            }
            for i, mz in enumerate(matched_mzs):
                match_info[f'mz_source_{i}' if i == 0 else f'mz_{i}'] = mz
            for i, mass in enumerate(matched_masses):
                match_info[f'mass_source_{i}' if i == 0 else f'mass_{i}'] = mass
            matches.append(match_info)

            for src_idx, orig_idx in zip(matched_sources, matched_original_indices):
                matched_indices_per_df[src_idx].add(orig_idx)

    if matches:
        result_df = pd.DataFrame(matches)
        for col in ['matched_mzs', 'matched_masses', 'sources']:
            if col in result_df.columns:
                result_df = result_df.drop(columns=[col])
    else:
        columns = [mz_col, 'mz_average', 'matched_count']
        if any('mass' in df.columns for df in dfs):
            columns.extend(['mass_source_0', 'mass_1', 'mass_2', 'mass_3'])
        result_df = pd.DataFrame(columns=columns)

    updated_dfs = []
    for i, df in enumerate(dfs):
        df_copy = df.copy()
        df_copy['label'] = 0
        for idx in matched_indices_per_df[i]:
            df_copy.loc[idx, 'label'] = 1
        updated_dfs.append(df_copy)

    return result_df, updated_dfs

def get_matched_index(mono_mass_arr, ion, ppm):
    left, right = mz_tolerance(ion.MASS, ppm)
    matched_mass_index = (mono_mass_arr.iloc[:, 0] <= right) & (mono_mass_arr.iloc[:, 0] >= left)
    return matched_mass_index

