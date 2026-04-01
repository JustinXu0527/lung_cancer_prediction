"""
预测模块
功能：
1. 加载训练好的模型
2. 获取单个样本的预测
3. 风险分级
"""

import pickle
import numpy as np
import pandas as pd
import os


class LungCancerPredictor:
    def __init__(self, models_dir='models'):
        """
        初始化预测器
        
        Args:
            models_dir (str): 模型保存目录
        """
        self.models_dir = models_dir
        self.models = {}
        self.scaler = None
        self.feature_names = None
        self.load_models()
    
    def load_models(self):
        """
        加载所有训练好的模型
        """
        try:
            # 加载基础模型
            for model_name in ['LogisticRegression', 'RandomForest', 'XGBoost']:
                model_path = os.path.join(self.models_dir, f'{model_name}.pkl')
                if os.path.exists(model_path):
                    with open(model_path, 'rb') as f:
                        self.models[model_name] = pickle.load(f)
            
            # 加载Stacking模型
            stacking_path = os.path.join(self.models_dir, 'stacking_model.pkl')
            if os.path.exists(stacking_path):
                with open(stacking_path, 'rb') as f:
                    self.models['Stacking'] = pickle.load(f)
            
            # 加载Scaler
            scaler_path = os.path.join(self.models_dir, 'scaler.pkl')
            if os.path.exists(scaler_path):
                with open(scaler_path, 'rb') as f:
                    self.scaler = pickle.load(f)
            
            print(f"✓ 模型已加载: {list(self.models.keys())}")
        except Exception as e:
            print(f"⚠️ 加载模型时出错: {e}")
    
    def set_feature_names(self, feature_names):
        """
        设置特征名称
        
        Args:
            feature_names (list): 特征名称列表
        """
        self.feature_names = feature_names
    
    def predict(self, input_data, model_name='Stacking', use_scaler=True):
        """
        进行预测
        
        Args:
            input_data (dict or np.ndarray): 输入数据
            model_name (str): 使用的模型名称 ('Stacking', 'RandomForest', 'XGBoost', 'LogisticRegression')
            use_scaler (bool): 是否使用Scaler进行标准化
            
        Returns:
            dict: 预测结果和风险等级
        """
        # 转换输入数据为DataFrame
        if isinstance(input_data, dict):
            X = pd.DataFrame([input_data])
        else:
            X = pd.DataFrame(input_data, columns=self.feature_names)
        
        # 标准化数据
        if use_scaler and self.scaler is not None:
            X_scaled = self.scaler.transform(X)
            X_scaled = pd.DataFrame(X_scaled, columns=X.columns)
        else:
            X_scaled = X
        
        # 获取模型
        model = self.models.get(model_name)
        if model is None:
            raise ValueError(f"模型 '{model_name}' 未找到")
        
        # 进行预测
        if isinstance(model, dict):
            # Stacking模型
            meta_features = self._get_stacking_features(model, X_scaled)
            probability = model['meta_model'].predict_proba(meta_features)[0, 1]
            prediction = (probability >= 0.5).astype(int)
        else:
            # 普通模型
            prediction = model.predict(X_scaled)[0]
            probability = model.predict_proba(X_scaled)[0, 1]
        
        # 确定风险等级
        if probability >= 0.7:
            risk_level = "🔴 High Risk"
            risk_color = "red"
        elif probability >= 0.5:
            risk_level = "🟠 Medium Risk"
            risk_color = "orange"
        else:
            risk_level = "🟢 Low Risk"
            risk_color = "green"
        
        result = {
            'prediction': prediction,
            'probability': probability,
            'risk_level': risk_level,
            'risk_color': risk_color,
            'model_used': model_name
        }
        
        return result
    
    def predict_batch(self, input_data, model_name='Stacking'):
        """
        批量预测
        
        Args:
            input_data (pd.DataFrame): 批量输入数据
            model_name (str): 使用的模型名称
            
        Returns:
            pd.DataFrame: 预测结果
        """
        # 标准化数据
        if self.scaler is not None:
            X_scaled = self.scaler.transform(input_data)
            X_scaled = pd.DataFrame(X_scaled, columns=input_data.columns)
        else:
            X_scaled = input_data
        
        # 获取模型
        model = self.models.get(model_name)
        if model is None:
            raise ValueError(f"模型 '{model_name}' 未找到")
        
        # 进行预测
        if isinstance(model, dict):
            # Stacking模型
            meta_features = self._get_stacking_features(model, X_scaled)
            probabilities = model['meta_model'].predict_proba(meta_features)[:, 1]
            predictions = (probabilities >= 0.5).astype(int)
        else:
            # 普通模型
            predictions = model.predict(X_scaled)
            probabilities = model.predict_proba(X_scaled)[:, 1]
        
        # 创建结果数据框
        results = pd.DataFrame({
            'Prediction': predictions,
            'Probability': probabilities,
            'Risk_Level': ['High Risk' if p >= 0.7 else 'Medium Risk' if p >= 0.5 else 'Low Risk' 
                          for p in probabilities]
        })
        
        return results
    
    def _get_stacking_features(self, stacking_model, X):
        """
        获取Stacking模型的输入特征 (元特征)
        
        Args:
            stacking_model (dict): Stacking模型
            X (pd.DataFrame): 输入特征
            
        Returns:
            np.ndarray: 基础模型的预测概率矩阵
        """
        base_models = stacking_model['base_models']
        meta_features = np.zeros((X.shape[0], len(base_models)))
        
        for i, (name, model) in enumerate(base_models):
            meta_features[:, i] = model.predict_proba(X)[:, 1]
        
        return meta_features
    
    def get_available_models(self):
        """
        获取可用的模型列表
        
        Returns:
            list: 已加载的模型名称列表
        """
        return list(self.models.keys())


def create_predictor(models_dir='models', scaler=None):
    """
    创建预测器实例的便捷函数
    
    Args:
        models_dir (str): 模型保存目录
        scaler: StandardScaler实例
        
    Returns:
        LungCancerPredictor: 预测器实例
    """
    predictor = LungCancerPredictor(models_dir)
    if scaler is not None:
        predictor.scaler = scaler
    return predictor
