"""
模型训练模块
功能：
1. 训练多个分类模型 (Logistic Regression, Random Forest, XGBoost)
2. 构建Stacking集成模型
3. 评估模型性能
4. 保存模型和评估结果
"""

import pandas as pd
import numpy as np
import pickle
import os
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, auc, roc_curve, f1_score, roc_auc_score, confusion_matrix
from xgboost import XGBClassifier
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')


class ModelTrainer:
    def __init__(self, output_dir='models'):
        """
        初始化模型训练器
        
        Args:
            output_dir (str): 模型保存目录
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        self.models = {}
        self.predictions = {}
        self.metrics = {}
    
    def train_logistic_regression(self, X_train, y_train):
        """
        训练逻辑回归模型
        
        Args:
            X_train: 训练特征
            y_train: 训练标签
            
        Returns:
            LogisticRegression: 训练好的模型
        """
        print("\n📊 训练逻辑回归模型...")
        model = LogisticRegression(max_iter=1000, random_state=42)
        model.fit(X_train, y_train)
        self.models['LogisticRegression'] = model
        print("✓ 逻辑回归模型训练完成")
        return model
    
    def train_random_forest(self, X_train, y_train):
        """
        训练随机森林模型
        
        Args:
            X_train: 训练特征
            y_train: 训练标签
            
        Returns:
            RandomForestClassifier: 训练好的模型
        """
        print("\n🌲 训练随机森林模型...")
        model = RandomForestClassifier(
            n_estimators=100,
            max_depth=15,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42,
            n_jobs=-1
        )
        model.fit(X_train, y_train)
        self.models['RandomForest'] = model
        print("✓ 随机森林模型训练完成")
        return model
    
    def train_xgboost(self, X_train, y_train):
        """
        训练XGBoost模型
        
        Args:
            X_train: 训练特征
            y_train: 训练标签
            
        Returns:
            XGBClassifier: 训练好的模型
        """
        print("\n⚡ 训练XGBoost模型...")
        model = XGBClassifier(
            n_estimators=100,
            max_depth=7,
            learning_rate=0.1,
            subsample=0.8,
            colsample_bytree=0.8,
            random_state=42,
            verbosity=0
        )
        model.fit(X_train, y_train)
        self.models['XGBoost'] = model
        print("✓ XGBoost模型训练完成")
        return model
    
    def create_stacking_model(self, X_train, y_train):
        """
        创建Stacking集成模型
        使用逻辑回归、随机森林、XGBoost作为基础模型
        使用逻辑回归作为元模型
        
        Args:
            X_train: 训练特征
            y_train: 训练标签
            
        Returns:
            dict: 包含基础模型和元模型的字典
        """
        print("\n🔗 构建Stacking集成模型...")
        
        # 确保基础模型已训练
        if 'LogisticRegression' not in self.models:
            self.train_logistic_regression(X_train, y_train)
        if 'RandomForest' not in self.models:
            self.train_random_forest(X_train, y_train)
        if 'XGBoost' not in self.models:
            self.train_xgboost(X_train, y_train)
        
        # 基础模型
        base_models = [
            ('lr', self.models['LogisticRegression']),
            ('rf', self.models['RandomForest']),
            ('xgb', self.models['XGBoost'])
        ]
        
        # 生成基础模型的预测 (用于训练元模型)
        cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
        meta_features = np.zeros((X_train.shape[0], len(base_models)))
        
        for fold, (train_idx, val_idx) in enumerate(cv.split(X_train, y_train)):
            X_train_fold = X_train.iloc[train_idx]
            y_train_fold = y_train.iloc[train_idx]
            X_val_fold = X_train.iloc[val_idx]
            
            for i, (name, model) in enumerate(base_models):
                # 在折叠训练数据上训练
                temp_model = type(model)(**model.get_params())
                temp_model.fit(X_train_fold, y_train_fold)
                # 预测验证数据
                meta_features[val_idx, i] = temp_model.predict_proba(X_val_fold)[:, 1]
        
        # 训练元模型
        meta_model = LogisticRegression(max_iter=1000, random_state=42)
        meta_model.fit(meta_features, y_train)
        
        stacking_model = {
            'base_models': base_models,
            'meta_model': meta_model,
            'model_names': ['LogisticRegression', 'RandomForest', 'XGBoost']
        }
        
        self.models['Stacking'] = stacking_model
        print("✓ Stacking集成模型构建完成")
        return stacking_model
    
    def evaluate_model(self, model, X_test, y_test, model_name):
        """
        评估单个模型
        
        Args:
            model: 模型对象
            X_test: 测试特征
            y_test: 测试标签
            model_name (str): 模型名称
            
        Returns:
            dict: 性能指标字典
        """
        # 处理Stacking模型
        if isinstance(model, dict):
            # 这是Stacking模型
            meta_features = self._get_stacking_features(model, X_test)
            y_pred_proba = model['meta_model'].predict_proba(meta_features)[:, 1]
            y_pred = (y_pred_proba >= 0.5).astype(int)
        else:
            # 普通模型
            y_pred = model.predict(X_test)
            y_pred_proba = model.predict_proba(X_test)[:, 1] if hasattr(model, 'predict_proba') else y_pred
        
        # 计算指标
        accuracy = accuracy_score(y_test, y_pred)
        auc_score = roc_auc_score(y_test, y_pred_proba)
        f1 = f1_score(y_test, y_pred)
        
        metrics = {
            'Model': model_name,
            'Accuracy': accuracy,
            'AUC': auc_score,
            'F1-Score': f1
        }
        
        self.metrics[model_name] = metrics
        self.predictions[model_name] = {
            'y_pred': y_pred,
            'y_pred_proba': y_pred_proba
        }
        
        print(f"\n📈 {model_name} 性能指标:")
        print(f"  - Accuracy: {accuracy:.4f}")
        print(f"  - AUC:      {auc_score:.4f}")
        print(f"  - F1-Score: {f1:.4f}")
        
        return metrics
    
    def _get_stacking_features(self, stacking_model, X):
        """
        获取Stacking模型的输入特征
        
        Args:
            stacking_model (dict): Stacking模型
            X: 输入特征
            
        Returns:
            np.ndarray: 基础模型的预测概率
        """
        base_models = stacking_model['base_models']
        meta_features = np.zeros((X.shape[0], len(base_models)))
        
        for i, (name, model) in enumerate(base_models):
            meta_features[:, i] = model.predict_proba(X)[:, 1]
        
        return meta_features
    
    def train_all_models(self, X_train, X_test, y_train, y_test):
        """
        训练所有模型并评估
        
        Args:
            X_train: 训练特征
            X_test: 测试特征
            y_train: 训练标签
            y_test: 测试标签
        """
        print("="*60)
        print("🚀 开始模型训练和评估")
        print("="*60)
        
        # 训练基础模型
        self.train_logistic_regression(X_train, y_train)
        self.train_random_forest(X_train, y_train)
        self.train_xgboost(X_train, y_train)
        
        # 创建Stacking模型
        self.create_stacking_model(X_train, y_train)
        
        # 评估所有模型
        print("\n" + "="*60)
        print("📊 模型评估")
        print("="*60)
        
        metrics_list = []
        for model_name in ['LogisticRegression', 'RandomForest', 'XGBoost', 'Stacking']:
            metrics = self.evaluate_model(
                self.models[model_name],
                X_test,
                y_test,
                model_name
            )
            metrics_list.append(metrics)
        
        # 保存结果
        results_df = pd.DataFrame(metrics_list)
        results_df.to_csv(os.path.join(self.output_dir, 'model_performance.csv'), index=False)
        
        print("\n" + "="*60)
        print("📋 模型性能对比")
        print("="*60)
        print(results_df.to_string(index=False))
        
        return results_df
    
    def save_models(self):
        """
        保存所有训练的模型
        """
        print("\n💾 保存模型...")
        
        # 保存基础模型
        for model_name in ['LogisticRegression', 'RandomForest', 'XGBoost']:
            model_path = os.path.join(self.output_dir, f'{model_name}.pkl')
            with open(model_path, 'wb') as f:
                pickle.dump(self.models[model_name], f)
            print(f"  ✓ {model_name}.pkl 已保存")
        
        # 保存Stacking模型
        stacking_path = os.path.join(self.output_dir, 'stacking_model.pkl')
        with open(stacking_path, 'wb') as f:
            pickle.dump(self.models['Stacking'], f)
        print(f"  ✓ stacking_model.pkl 已保存")
    
    def get_feature_importance(self, X_train):
        """
        获取RandomForest和XGBoost的特征重要性
        
        Args:
            X_train: 训练特征
            
        Returns:
            tuple: (rf_importance, xgb_importance, feature_names)
        """
        feature_names = X_train.columns.tolist()
        
        # Random Forest特征重要性
        rf_model = self.models.get('RandomForest')
        rf_importance = rf_model.feature_importances_ if rf_model else None
        
        # XGBoost特征重要性
        xgb_model = self.models.get('XGBoost')
        xgb_importance = xgb_model.feature_importances_ if xgb_model else None
        
        return rf_importance, xgb_importance, feature_names
