"""
数据预处理模块
功能：
1. 加载数据集
2. 数据清洗和转换
3. 特征标准化
4. 训练集和测试集分割
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
import os


def load_data(data_path='data/LungCancerDataset.csv'):
    """
    加载数据集
    
    Args:
        data_path (str): 数据集路径
        
    Returns:
        pd.DataFrame: 加载的数据
    """
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"数据集文件未找到: {data_path}")
    
    df = pd.read_csv(data_path)
    print(f"✓ 数据集已加载: {df.shape[0]} 行, {df.shape[1]} 列")
    return df


def clean_data(df):
    """
    数据清洗
    
    Args:
        df (pd.DataFrame): 原始数据
        
    Returns:
        pd.DataFrame: 清洗后的数据
    """
    # 检查缺失值
    print(f"缺失值统计:\n{df.isnull().sum()}")
    
    # 删除缺失值（如果有）
    df = df.dropna()
    
    # 处理目标变量（YES -> 1, NO -> 0）
    df['PULMONARY_DISEASE'] = df['PULMONARY_DISEASE'].map({'YES': 1, 'NO': 0})
    
    print(f"✓ 数据清洗完成: {df.shape[0]} 行")
    return df


def preprocess_data(df):
    """
    数据预处理：编码和分割
    
    Args:
        df (pd.DataFrame): 清洗后的数据
        
    Returns:
        tuple: (X_train, X_test, y_train, y_test, feature_names, scaler)
    """
    # 分离特征和目标变量
    X = df.drop('PULMONARY_DISEASE', axis=1)
    y = df['PULMONARY_DISEASE']
    
    feature_names = X.columns.tolist()
    
    # 编码分类特征（GENDER）
    le_gender = LabelEncoder()
    X['GENDER'] = le_gender.fit_transform(X['GENDER'])
    
    # 将其他0/1特征转换为整数
    binary_columns = [col for col in X.columns if X[col].nunique() == 2 and set(X[col].unique()).issubset({0, 1, '0', '1', 'YES', 'NO'})]
    for col in binary_columns:
        if col != 'GENDER':
            X[col] = X[col].astype(int)
    
    # 分割数据集 (80% 训练, 20% 测试)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # 标准化特征
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # 转换为DataFrame（保持列名）
    X_train_scaled = pd.DataFrame(X_train_scaled, columns=feature_names)
    X_test_scaled = pd.DataFrame(X_test_scaled, columns=feature_names)
    
    print(f"✓ 数据预处理完成")
    print(f"  - 训练集: {X_train_scaled.shape[0]} 行")
    print(f"  - 测试集: {X_test_scaled.shape[0]} 行")
    print(f"  - 特征数: {X_train_scaled.shape[1]}")
    
    return X_train_scaled, X_test_scaled, y_train, y_test, feature_names, scaler


def prepare_data(data_path='data/LungCancerDataset.csv'):
    """
    数据准备的完整流程
    
    Args:
        data_path (str): 数据集路径
        
    Returns:
        tuple: (X_train, X_test, y_train, y_test, feature_names, scaler)
    """
    df = load_data(data_path)
    df = clean_data(df)
    X_train, X_test, y_train, y_test, feature_names, scaler = preprocess_data(df)
    return X_train, X_test, y_train, y_test, feature_names, scaler
