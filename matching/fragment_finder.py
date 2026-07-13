import numpy as np
import pandas as pd
from tqdm import tqdm
from matching.protein_classes import Clip, Ion, Mod
from data.mgf_parser import get_matched_index
from utils.common import *

def construct_CM_series(mass_series, protein, start, end, ion_type, fixed_mod_list, unloc_mod_list):
    """构造CM输出序列"""


    return pd.Series([
        ion_type,
        mass_series.iloc[0],
        protein.MASS,
        start,
        end,
        cal_ppm(mass_series.iloc[0], protein.MASS),
        get_fixed_mod_list_name(fixed_mod_list) or 0,
        get_unloc_mod_list_name(unloc_mod_list) or 0,
        protein.seq,
        mass_series.iloc[1],
        protein.FORMULA,
        mass_series.iloc[2],
        mass_series.iloc[3]
    ])


def get_internal_CM_output(mono_mass_arr, protein, ion_type_list, ppm, unloc_mod_df):
    """获取内部碎片匹配输出"""
    seqLen = protein.SEQLEN
    results = []
    total_iterations = sum(1 for start in range(2, seqLen) for end in range(start, seqLen))

    with tqdm(total=total_iterations, desc="Processing internal fragments") as pbar:
        for start in range(2, seqLen):
            for end in range(start, seqLen):
                pep = Clip(protein).clip(start, end)
                for ion_type in ion_type_list:
                    ion = Ion(pep).ionization(ion_type)
                    matched_mass_index = get_matched_index(mono_mass_arr, ion, ppm)
                    matched_mass_df = mono_mass_arr[matched_mass_index]
                    for _, matched_mass_series in matched_mass_df.iterrows():
                        results.append(construct_CM_series(
                            matched_mass_series, ion, start, end, ion_type,
                            list(pep.mod_list.values()), []
                        ))
                pbar.update(1)

    if len(results) == 0:
        return pd.DataFrame(columns=["Frag Type", "Observed Mass", "Theoretical Mass",
                                     "Start AA", "End AA", "Error", "Fixed Mod",
                                     "Unloc Mod", "Sequence", "Intensity", "Formula",
                                     "Charge", "mz"])
    df = pd.DataFrame(results)
    df.columns = ["Frag Type", "Observed Mass", "Theoretical Mass", "Start AA", "End AA",
                  "Error", "Fixed Mod", "Unloc Mod", "Sequence", "Intensity",
                  "Formula", "Charge", "mz"]
    return df


def get_Nterminal_CM_output(mono_mass_arr, protein, ion_type_list, ppm, unloc_mod_df):
    """获取N端碎片匹配输出"""
    seqLen = protein.SEQLEN
    results = []
    start = 1

    with tqdm(total=seqLen - 1, desc="Processing N-terminal fragments") as pbar:
        for end in range(1, seqLen):
            pep = Clip(protein).clip(start, end)
            for ion_type in ion_type_list:
                ion = Ion(pep).ionization(ion_type)
                matched_mass_index = get_matched_index(mono_mass_arr, ion, ppm)
                matched_mass_df = mono_mass_arr[matched_mass_index]
                for _, matched_mass_series in matched_mass_df.iterrows():
                    results.append(construct_CM_series(
                        matched_mass_series, ion, start, end, ion_type,
                        list(pep.mod_list.values()), []
                    ))
            pbar.update(1)

    if len(results) == 0:
        return pd.DataFrame(columns=["Frag Type", "Observed Mass", "Theoretical Mass",
                                     "Start AA", "End AA", "Error", "Fixed Mod",
                                     "Unloc Mod", "Sequence", "Intensity", "Formula",
                                     "Charge", "mz"])
    df = pd.DataFrame(results)
    df.columns = ["Frag Type", "Observed Mass", "Theoretical Mass", "Start AA", "End AA",
                  "Error", "Fixed Mod", "Unloc Mod", "Sequence", "Intensity",
                  "Formula", "Charge", "mz"]
    return df


def get_Cterminal_CM_output(mono_mass_arr, protein, ion_type_list, ppm, unloc_mod_df):
    """获取C端碎片匹配输出"""
    seqLen = protein.SEQLEN
    results = []
    end = seqLen

    with tqdm(total=seqLen - 1, desc="Processing C-terminal fragments") as pbar:
        for start in range(2, seqLen + 1):
            pep = Clip(protein).clip(start, end)
            for ion_type in ion_type_list:
                ion = Ion(pep).ionization(ion_type)
                matched_mass_index = get_matched_index(mono_mass_arr, ion, ppm)
                matched_mass_df = mono_mass_arr[matched_mass_index]
                for _, matched_mass_series in matched_mass_df.iterrows():
                    results.append(construct_CM_series(
                        matched_mass_series, ion, start, end, ion_type,
                        list(pep.mod_list.values()), []
                    ))
            pbar.update(1)

    if len(results) == 0:
        return pd.DataFrame(columns=["Frag Type", "Observed Mass", "Theoretical Mass",
                                     "Start AA", "End AA", "Error", "Fixed Mod",
                                     "Unloc Mod", "Sequence", "Intensity", "Formula",
                                     "Charge", "mz"])
    df = pd.DataFrame(results)
    df.columns = ["Frag Type", "Observed Mass", "Theoretical Mass", "Start AA", "End AA",
                  "Error", "Fixed Mod", "Unloc Mod", "Sequence", "Intensity",
                  "Formula", "Charge", "mz"]
    return df