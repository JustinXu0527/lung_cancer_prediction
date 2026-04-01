"""
主要训练脚本
功能：
1. 加载和预处理数据
2. 训练所有模型
3. 保存模型和标准化器
4. 生成性能报告
"""

import os
import sys
import pickle
import pandas as pd
from pathlib import Path

# 添加src目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from src.preprocess import prepare_data
from src.train import ModelTrainer


def main():
    """
    主要执行函数
    """
    print("="*70)
    print(" 🫁 肺癌风险预测系统 - 模型训练")
    print("="*70)
    
    # 1. 准备数据
    print("\n[1/4] 数据准备阶段...")
    try:
        X_train, X_test, y_train, y_test, feature_names, scaler = prepare_data(
            data_path='data/LungCancerDataset.csv'
        )
        print("✅ 数据准备完成\n")
    except Exception as e:
        print(f"❌ 数据准备失败: {e}")
        return
    
    # 2. 保存Scaler
    print("[2/4] 保存标准化器...")
    try:
        os.makedirs('models', exist_ok=True)
        scaler_path = 'models/scaler.pkl'
        with open(scaler_path, 'wb') as f:
            pickle.dump(scaler, f)
        print(f"✅ 标准化器已保存: {scaler_path}\n")
    except Exception as e:
        print(f"⚠️  无法保存标准化器: {e}\n")
    
    # 3. 训练模型
    print("[3/4] 模型训练阶段...")
    try:
        trainer = ModelTrainer(output_dir='models')
        results_df = trainer.train_all_models(X_train, X_test, y_train, y_test)
        print("\n✅ 模型训练完成\n")
    except Exception as e:
        print(f"❌ 模型训练失败: {e}")
        return
    
    # 4. 保存模型
    print("[4/4] 保存事权模型...")
    try:
        trainer.save_models()
        print("✅ 所有模型已保存\n")
    except Exception as e:
        print(f"⚠️  无法保存模型: {e}\n")
    
    # 总结
    print("="*70)
    print("🎉 训练完成!")
    print("="*70)
    print("\n📁 输出文件：")
    print("  - models/LogisticRegression.pkl")
    print("  - models/RandomForest.pkl")
    print("  - models/XGBoost.pkl")
    print("  - models/stacking_model.pkl")
    print("  - models/scaler.pkl")
    print("  - models/model_performance.csv")
    print("\n🚀 启动Streamlit应用：")
    print("  streamlit run app/app.py")
    print("="*70)


if __name__ == '__main__':
    main()
