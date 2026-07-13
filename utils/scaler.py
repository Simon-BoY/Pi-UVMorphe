import pickle
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from typing import Optional, List, Union


def create_standard_scaler_from_df(
        df: pd.DataFrame,
        feature_cols: List[str] = ['Mass', 'Intensity', 'Charge', 'mz'],
        save_path: Optional[str] = None
) -> StandardScaler:
    """
    从DataFrame创建StandardScaler并可选保存

    Parameters:
    -----------
    df : pd.DataFrame
        包含特征列的数据框
    feature_cols : List[str]
        要标准化的特征列名
    save_path : Optional[str]
        保存scaler的路径（.pkl文件）

    Returns:
    --------
    StandardScaler
        训练好的scaler对象
    """
    scaler = StandardScaler()
    scaler.fit(df[feature_cols])

    if save_path:
        with open(save_path, 'wb') as f:
            pickle.dump(scaler, f)
        print(f"✓ Scaler saved to: {save_path}")

    return scaler


def load_standard_scaler(file_path: str) -> StandardScaler:
    """
    加载保存的StandardScaler

    Parameters:
    -----------
    file_path : str
        .pkl文件路径

    Returns:
    --------
    StandardScaler
        加载的scaler对象
    """
    with open(file_path, 'rb') as f:
        scaler = pickle.load(f)
    print(f"✓ Scaler loaded: {file_path}")
    return scaler


def normalize_tabular_features(
        df: pd.DataFrame,
        scaler: StandardScaler,
        feature_cols: List[str] = ['Mass', 'Intensity', 'Charge', 'mz'],
        inplace: bool = False
) -> pd.DataFrame:
    """
    标准化表格特征

    Parameters:
    -----------
    df : pd.DataFrame
        包含特征列的数据框
    scaler : StandardScaler
        已训练的scaler
    feature_cols : List[str]
        要标准化的特征列名
    inplace : bool
        是否原地修改

    Returns:
    --------
    pd.DataFrame
        标准化后的数据框
    """
    if inplace:
        df[feature_cols] = scaler.transform(df[feature_cols])
        return df
    else:
        df_copy = df.copy()
        df_copy[feature_cols] = scaler.transform(df_copy[feature_cols])
        return df_copy


def inverse_normalize_tabular_features(
        df: pd.DataFrame,
        scaler: StandardScaler,
        feature_cols: List[str] = ['Mass', 'Intensity', 'Charge', 'mz'],
        inplace: bool = False
) -> pd.DataFrame:
    """
    反标准化表格特征（恢复原始尺度）

    Parameters:
    -----------
    df : pd.DataFrame
        标准化后的数据框
    scaler : StandardScaler
        已训练的scaler
    feature_cols : List[str]
        要反标准化的特征列名
    inplace : bool
        是否原地修改

    Returns:
    --------
    pd.DataFrame
        反标准化后的数据框
    """
    if inplace:
        df[feature_cols] = scaler.inverse_transform(df[feature_cols])
        return df
    else:
        df_copy = df.copy()
        df_copy[feature_cols] = scaler.inverse_transform(df_copy[feature_cols])
        return df_copy


def get_scaler_params(scaler: StandardScaler) -> dict:
    """
    获取StandardScaler的参数信息

    Parameters:
    -----------
    scaler : StandardScaler
        已训练的scaler

    Returns:
    --------
    dict
        包含均值和标准差的字典
    """
    return {
        'mean': scaler.mean_.tolist() if hasattr(scaler, 'mean_') else None,
        'scale': scaler.scale_.tolist() if hasattr(scaler, 'scale_') else None,
        'n_features': scaler.n_features_in_ if hasattr(scaler, 'n_features_in_') else None,
        'feature_names': getattr(scaler, 'feature_names_in_', None)
    }


# =========================================================
# 使用示例
# =========================================================
if __name__ == "__main__":
    # 创建示例数据
    sample_df = pd.DataFrame({
        'Mass': [100.0, 150.0, 200.0, 250.0],
        'Intensity': [1000, 2000, 3000, 4000],
        'Charge': [1, 2, 3, 4],
        'mz': [100.0, 150.0, 200.0, 250.0]
    })

    # 创建并保存scaler
    scaler = create_standard_scaler_from_df(
        sample_df,
        save_path='scaler_example.pkl'
    )

    # 查看参数
    params = get_scaler_params(scaler)
    print(f"均值: {params['mean']}")
    print(f"标准差: {params['scale']}")

    # 标准化
    normalized = normalize_tabular_features(sample_df, scaler)
    print("\n标准化后:")
    print(normalized)

    # 反标准化
    restored = inverse_normalize_tabular_features(normalized, scaler)
    print("\n反标准化后:")
    print(restored)