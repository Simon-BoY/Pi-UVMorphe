"""
碎片匹配模块 - 包含蛋白质类、碎片匹配、后处理、可靠性分析和可视化
"""

from .protein_classes import (
    Mod,
    NTermMod,
    CTermMod,
    AMod,
    BMod,
    CMod,
    XMod,
    YMod,
    ZMod,
    C_HMod,
    N_HMod,
    Protein,
    Clip,
    Ion
)

from .fragment_finder import (
    construct_CM_series,
    get_internal_CM_output,
    get_Nterminal_CM_output,
    get_Cterminal_CM_output
)

from .post_processing import (
    get_terminal_frag_df,
    get_internal_frag_df,
    get_low_Error_df,
    process_terminal_rep_match,
    process_rep_match,
    post_process,
    get_cleavage_coverage
)

from .reliability import (
    get_terminal_cleavages,
    classify_internal_support,
    calculate_internal_reliability_score
)

from .visualization import (
    seg_map_plot_main,
    plot_internal_fragment_support_map,
    get_seq_trace_cor,
    get_seq_trace,
    get_fig_size
)

from .abundance_plot import (
    fragment_abundance_plot_main,
    get_TIC,
    get_terminal_relative_AA_site,
    split_internal_to_terminal
)

__all__ = [
    # protein_classes
    'Mod',
    'NTermMod',
    'CTermMod',
    'AMod',
    'BMod',
    'CMod',
    'XMod',
    'YMod',
    'ZMod',
    'C_HMod',
    'N_HMod',
    'Protein',
    'Clip',
    'Ion',
    # fragment_finder
    'construct_CM_series',
    'get_internal_CM_output',
    'get_Nterminal_CM_output',
    'get_Cterminal_CM_output',
    # post_processing
    'get_terminal_frag_df',
    'get_internal_frag_df',
    'get_low_Error_df',
    'process_terminal_rep_match',
    'process_rep_match',
    'post_process',
    'get_cleavage_coverage',
    # reliability
    'get_terminal_cleavages',
    'classify_internal_support',
    'calculate_internal_reliability_score',
    # visualization
    'seg_map_plot_main',
    'plot_internal_fragment_support_map',
    'get_seq_trace_cor',
    'get_seq_trace',
    'get_fig_size',
    # abundance_plot
    'fragment_abundance_plot_main',
    'get_TIC',
    'get_terminal_relative_AA_site',
    'split_internal_to_terminal'
]