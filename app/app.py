"""
肺癌风险预测Streamlit应用
功能：
1. 用户输入患者特征
2. 显示预测结果和风险等级
3. 展示可视化分析
4. 显示模型性能指标
"""

import streamlit as st
import pandas as pd
import numpy as np
import pickle
import os
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import roc_curve, auc, confusion_matrix
import sys

# 添加src目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.preprocess import prepare_data
from src.predict import LungCancerPredictor

# 设置页面配置
st.set_page_config(
    page_title="肺癌风险预测系统",
    page_icon="🫁",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义样式
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
    }
    </style>
    """, unsafe_allow_html=True)

# 初始化会话状态
@st.cache_resource
def load_models_and_data():
    """加载模型和数据"""
    try:
        # 加载预测器
        predictor = LungCancerPredictor('models')
        
        # 加载模型性能数据
        performance_path = 'models/model_performance.csv'
        if os.path.exists(performance_path):
            performance_df = pd.read_csv(performance_path)
        else:
            performance_df = None
        
        # 加载原始数据用于可视化
        data_path = 'data/LungCancerDataset.csv'
        if os.path.exists(data_path):
            df = pd.read_csv(data_path)
        else:
            df = None
        
        return predictor, performance_df, df
    except Exception as e:
        st.error(f"加载模型失败: {e}")
        return None, None, None

# 加载数据
predictor, performance_df, raw_data = load_models_and_data()

# 页面标题
st.title("🫁 肺癌风险预测系统")
st.markdown("---")

# 侧边栏配置
st.sidebar.title("📋 病患信息输入")

# 特征输入
with st.sidebar:
    age = st.slider("年龄", min_value=18, max_value=100, value=50, step=1)
    gender = st.selectbox("性别", options=[0, 1], format_func=lambda x: "男性" if x == 1 else "女性")
    smoking = st.selectbox("吸烟", options=[0, 1], format_func=lambda x: "是" if x == 1 else "否")
    finger_discoloration = st.selectbox("手指变色", options=[0, 1], format_func=lambda x: "是" if x == 1 else "否")
    mental_stress = st.selectbox("精神压力", options=[0, 1], format_func=lambda x: "是" if x == 1 else "否")
    pollution_exposure = st.selectbox("污染暴露", options=[0, 1], format_func=lambda x: "是" if x == 1 else "否")
    long_term_illness = st.selectbox("长期疾病", options=[0, 1], format_func=lambda x: "是" if x == 1 else "否")
    
    st.markdown("---")
    
    energy_level = st.slider("能量水平", min_value=0.0, max_value=100.0, value=60.0, step=1.0)
    immune_weakness = st.selectbox("免疫力弱", options=[0, 1], format_func=lambda x: "是" if x == 1 else "否")
    breathing_issue = st.selectbox("呼吸问题", options=[0, 1], format_func=lambda x: "是" if x == 1 else "否")
    alcohol_consumption = st.selectbox("饮酒", options=[0, 1], format_func=lambda x: "是" if x == 1 else "否")
    throat_discomfort = st.selectbox("喉咙不适", options=[0, 1], format_func=lambda x: "是" if x == 1 else "否")
    
    st.markdown("---")
    
    oxygen_saturation = st.slider("血氧饱和度 (%)", min_value=80.0, max_value=100.0, value=95.0, step=0.5)
    chest_tightness = st.selectbox("胸部紧张", options=[0, 1], format_func=lambda x: "是" if x == 1 else "否")
    family_history = st.selectbox("家族史", options=[0, 1], format_func=lambda x: "是" if x == 1 else "否")
    smoking_family_history = st.selectbox("吸烟家族史", options=[0, 1], format_func=lambda x: "是" if x == 1 else "否")
    stress_immune = st.selectbox("应激免疫", options=[0, 1], format_func=lambda x: "是" if x == 1 else "否")
    
    st.markdown("---")
    
    # 选择模型
    model_choice = st.selectbox(
        "选择预测模型",
        options=['Stacking', 'RandomForest', 'XGBoost', 'LogisticRegression'],
        help="选择要使用的机器学习模型"
    )
    
    # 预测按钮
    predict_button = st.button("🔍 进行预测", use_container_width=True)

# 主要内容
tab1, tab2, tab3, tab4 = st.tabs(["📊 预测结果", "📈 可视化分析", "📉 模型性能", "ℹ️ 关于系统"])

# Tab 1: 预测结果
with tab1:
    if predict_button:
        # 创建输入数据
        input_data = {
            'AGE': age,
            'GENDER': gender,
            'SMOKING': smoking,
            'FINGER_DISCOLORATION': finger_discoloration,
            'MENTAL_STRESS': mental_stress,
            'EXPOSURE_TO_POLLUTION': pollution_exposure,
            'LONG_TERM_ILLNESS': long_term_illness,
            'ENERGY_LEVEL': energy_level,
            'IMMUNE_WEAKNESS': immune_weakness,
            'BREATHING_ISSUE': breathing_issue,
            'ALCOHOL_CONSUMPTION': alcohol_consumption,
            'THROAT_DISCOMFORT': throat_discomfort,
            'OXYGEN_SATURATION': oxygen_saturation,
            'CHEST_TIGHTNESS': chest_tightness,
            'FAMILY_HISTORY': family_history,
            'SMOKING_FAMILY_HISTORY': smoking_family_history,
            'STRESS_IMMUNE': stress_immune
        }
        
        # 进行预测
        try:
            result = predictor.predict(input_data, model_name=model_choice)
            
            # 显示结果
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(
                    label="肺癌概率",
                    value=f"{result['probability']:.2%}",
                    delta=None
                )
            
            with col2:
                st.metric(
                    label="预测结果",
                    value="患病" if result['prediction'] == 1 else "未患病"
                )
            
            with col3:
                st.metric(
                    label="风险等级",
                    value=result['risk_level'].split(maxsplit=1)[1]
                )
            
            # 显示详细结果
            st.markdown("---")
            
            # 风险等级详细说明
            with st.container():
                col1, col2 = st.columns([3, 1])
                with col1:
                    if result['probability'] >= 0.7:
                        st.error(f"⚠️ **高风险患者** - 概率: {result['probability']:.2%}")
                        st.write("建议立即进行专业医学检查和评估。")
                    elif result['probability'] >= 0.5:
                        st.warning(f"⚠️ **中等风险患者** - 概率: {result['probability']:.2%}")
                        st.write("建议进行进一步的医学检查。")
                    else:
                        st.success(f"✅ **低风险患者** - 概率: {result['probability']:.2%}")
                        st.write("继续定期体检和健康监测。")
                
                with col2:
                    # 显示概率进度条
                    st.markdown(f"<div style='background-color: #f0f0f0; border-radius: 5px; padding: 10px;'>"
                               f"<div style='background-color: {'#d32f2f' if result['probability'] >= 0.7 else '#f57c00' if result['probability'] >= 0.5 else '#388e3c'}; "
                               f"width: {result['probability']*100}%; height: 20px; border-radius: 3px;'></div>"
                               f"</div>", unsafe_allow_html=True)
            
            st.markdown("---")
            
            # 特征摘要
            st.subheader("📝 输入特征摘要")
            feature_summary = pd.DataFrame({
                '特征': ['年龄', '性别', '吸烟', '手指变色', '精神压力', '污染暴露', '长期疾病', 
                        '能量水平', '免疫力弱', '呼吸问题', '饮酒', '喉咙不适', '血氧饱和度', 
                        '胸部紧张', '家族史', '吸烟家族史', '应激免疫'],
                '值': [age, '男' if gender == 1 else '女', '是' if smoking == 1 else '否',
                      '是' if finger_discoloration == 1 else '否', '是' if mental_stress == 1 else '否',
                      '是' if pollution_exposure == 1 else '否', '是' if long_term_illness == 1 else '否',
                      f"{energy_level:.1f}", '是' if immune_weakness == 1 else '否',
                      '是' if breathing_issue == 1 else '否', '是' if alcohol_consumption == 1 else '否',
                      '是' if throat_discomfort == 1 else '否', f"{oxygen_saturation:.1f}%",
                      '是' if chest_tightness == 1 else '否', '是' if family_history == 1 else '否',
                      '是' if smoking_family_history == 1 else '否', '是' if stress_immune == 1 else '否']
            })
            st.dataframe(feature_summary, use_container_width=True, hide_index=True)
        
        except Exception as e:
            st.error(f"预测失败: {e}")
    
    else:
        st.info("👆 请在左侧输入患者信息，然后点击「进行预测」按钮")

# Tab 2: 可视化分析
with tab2:
    st.subheader("📊 数据可视化分析")
    
    if raw_data is not None:
        # 转换目标变量
        raw_data['PULMONARY_DISEASE_NUM'] = raw_data['PULMONARY_DISEASE'].map({'YES': 1, 'NO': 0})
        
        viz_col1, viz_col2 = st.columns(2)
        
        # 1. 相关性热力图
        with viz_col1:
            st.markdown("### 1️⃣ 相关性热力图")
            try:
                fig, ax = plt.subplots(figsize=(10, 8))
                correlation = raw_data.drop('PULMONARY_DISEASE', axis=1).corr()
                sns.heatmap(correlation, annot=False, cmap='coolwarm', center=0, 
                           square=True, ax=ax, cbar_kws={'label': 'Correlation'})
                ax.set_title('特征相关性热力图', fontsize=14, fontweight='bold')
                st.pyplot(fig)
            except Exception as e:
                st.error(f"无法生成热力图: {e}")
        
        # 2. 吸烟与肺癌分布
        with viz_col2:
            st.markdown("### 2️⃣ 吸烟vs肺癌分布")
            try:
                fig, ax = plt.subplots(figsize=(8, 6))
                smoking_disease = pd.crosstab(raw_data['SMOKING'], raw_data['PULMONARY_DISEASE'], normalize='index') * 100
                smoking_disease.plot(kind='bar', ax=ax, color=['#4CAF50', '#F44336'])
                ax.set_xlabel('吸烟状态', fontsize=12)
                ax.set_ylabel('百分比 (%)', fontsize=12)
                ax.set_title('吸烟与肺癌相关性', fontsize=14, fontweight='bold')
                ax.set_xticklabels(['否', '是'], rotation=0)
                ax.legend(['正常', '患病'], loc='upper right')
                plt.tight_layout()
                st.pyplot(fig)
            except Exception as e:
                st.error(f"无法生成图表: {e}")
        
        viz_col3, viz_col4 = st.columns(2)
        
        # 3. 年龄分布
        with viz_col3:
            st.markdown("### 3️⃣ 患者年龄分布")
            try:
                fig, ax = plt.subplots(figsize=(8, 6))
                raw_data['AGE'].hist(bins=30, ax=ax, color='#2196F3', edgecolor='black', alpha=0.7)
                ax.set_xlabel('年龄', fontsize=12)
                ax.set_ylabel('患者数量', fontsize=12)
                ax.set_title('患者年龄分布', fontsize=14, fontweight='bold')
                ax.grid(alpha=0.3)
                st.pyplot(fig)
            except Exception as e:
                st.error(f"无法生成图表: {e}")
        
        # 4. 血氧饱和度分布
        with viz_col4:
            st.markdown("### 4️⃣ 血氧饱和度分布")
            try:
                fig, ax = plt.subplots(figsize=(8, 6))
                raw_data['OXYGEN_SATURATION'].hist(bins=30, ax=ax, color='#FF9800', edgecolor='black', alpha=0.7)
                ax.set_xlabel('血氧饱和度 (%)', fontsize=12)
                ax.set_ylabel('患者数量', fontsize=12)
                ax.set_title('血氧饱和度分布', fontsize=14, fontweight='bold')
                ax.grid(alpha=0.3)
                st.pyplot(fig)
            except Exception as e:
                st.error(f"无法生成图表: {e}")
        
        # 5. 缺陷的风险因素分布
        st.markdown("### 5️⃣ 主要风险因素分布")
        risk_factors = ['SMOKING', 'FINGER_DISCOLORATION', 'MENTAL_STRESS', 
                       'EXPOSURE_TO_POLLUTION', 'LONG_TERM_ILLNESS']
        
        try:
            fig, axes = plt.subplots(1, len(risk_factors), figsize=(15, 4))
            for idx, factor in enumerate(risk_factors):
                disease_by_factor = pd.crosstab(raw_data[factor], raw_data['PULMONARY_DISEASE'], normalize='index') * 100
                disease_by_factor.plot(kind='bar', ax=axes[idx], color=['#4CAF50', '#F44336'])
                axes[idx].set_title(factor.replace('_', ' '), fontsize=10, fontweight='bold')
                axes[idx].set_xlabel('')
                axes[idx].set_ylabel('百分比 (%)')
                axes[idx].set_xticklabels(['否', '是'], rotation=0)
                axes[idx].legend(['正常', '患病'], loc='best', fontsize=8)
            
            plt.tight_layout()
            st.pyplot(fig)
        except Exception as e:
            st.error(f"无法生成图表: {e}")
    
    else:
        st.warning("⚠️ 无法加载数据进行可视化分析")

# Tab 3: 模型性能
with tab3:
    st.subheader("📉 模型性能评估")
    
    if performance_df is not None:
        # 显示性能对比表
        st.markdown("### 模型性能指标对比")
        st.dataframe(performance_df, use_container_width=True, hide_index=True)
        
        # 可视化性能对比
        col1, col2, col3 = st.columns(3)
        
        with col1:
            fig_acc, ax_acc = plt.subplots(figsize=(8, 6))
            ax_acc.bar(performance_df['Model'], performance_df['Accuracy'], color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A'])
            ax_acc.set_ylabel('Accuracy', fontsize=12)
            ax_acc.set_title('模型准确率比较', fontsize=14, fontweight='bold')
            ax_acc.set_ylim([0, 1])
            for i, v in enumerate(performance_df['Accuracy']):
                ax_acc.text(i, v + 0.02, f'{v:.3f}', ha='center', va='bottom', fontweight='bold')
            plt.xticks(rotation=45, ha='right')
            st.pyplot(fig_acc)
        
        with col2:
            fig_auc, ax_auc = plt.subplots(figsize=(8, 6))
            ax_auc.bar(performance_df['Model'], performance_df['AUC'], color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A'])
            ax_auc.set_ylabel('AUC Score', fontsize=12)
            ax_auc.set_title('模型AUC比较', fontsize=14, fontweight='bold')
            ax_auc.set_ylim([0, 1])
            for i, v in enumerate(performance_df['AUC']):
                ax_auc.text(i, v + 0.02, f'{v:.3f}', ha='center', va='bottom', fontweight='bold')
            plt.xticks(rotation=45, ha='right')
            st.pyplot(fig_auc)
        
        with col3:
            fig_f1, ax_f1 = plt.subplots(figsize=(8, 6))
            ax_f1.bar(performance_df['Model'], performance_df['F1-Score'], color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A'])
            ax_f1.set_ylabel('F1-Score', fontsize=12)
            ax_f1.set_title('模型F1评分比较', fontsize=14, fontweight='bold')
            ax_f1.set_ylim([0, 1])
            for i, v in enumerate(performance_df['F1-Score']):
                ax_f1.text(i, v + 0.02, f'{v:.3f}', ha='center', va='bottom', fontweight='bold')
            plt.xticks(rotation=45, ha='right')
            st.pyplot(fig_f1)
        
        # 最佳模型推荐
        st.markdown("---")
        best_model_idx = performance_df['AUC'].idxmax()
        best_model = performance_df.iloc[best_model_idx]
        
        st.success(f"⭐ **最佳模型**: {best_model['Model']} (AUC: {best_model['AUC']:.4f})")
        
    else:
        st.warning("⚠️ 无法加载模型性能数据")

# Tab 4: 关于系统
with tab4:
    st.markdown("""
    ## 📖 关于肺癌风险预测系统
    
    ### 🎯 系统目的
    本系统使用机器学习模型，根据患者的症状和体检数据预测肺癌患病风险。
    
    ### 🤖 使用的模型
    - **逻辑回归 (Logistic Regression)**: 快速、可解释的线性模型
    - **随机森林 (Random Forest)**: 集成学习方法，处理特征交互
    - **梯度提升 (XGBoost)**: 强大的梯度提升树模型
    - **堆叠集成 (Stacking Ensemble)**: 综合上述三个模型的预测
    
    ### 📊 输入特征说明
    - **年龄**: 患者年龄（18-100岁）
    - **性别**: 男性或女性
    - **吸烟**: 是否有吸烟习惯
    - **手指变色**: 手指是否有变色迹象
    - **精神压力**: 是否有长期精神压力
    - **污染暴露**: 是否长期污染暴露
    - **长期疾病**: 是否患有长期疾病
    - **能量水平**: 日常能量水平（0-100）
    - **免疫力弱**: 是否免疫力较弱
    - **呼吸问题**: 是否有呼吸问题
    - **饮酒**: 是否有饮酒习惯
    - **喉咙不适**: 是否有喉咙不适症状
    - **血氧饱和度**: 血液中氧饱和度百分比（80-100%）
    - **胸部紧张**: 是否有胸部紧张感
    - **家族史**: 是否有肺癌家族史
    - **吸烟家族史**: 是否有家族吸烟史
    - **应激免疫**: 应激状态下免疫系统反应
    
    ### ⚠️ 免责声明
    本系统仅供参考，**不能替代专业医学诊断**。任何医学决定都应咨询专业医疗人士。
    
    ### 🔍 风险等级说明
    - 🟢 **低风险** (概率 < 50%): 继续定期体检
    - 🟠 **中等风险** (50% ≤ 概率 < 70%): 建议进一步医学检查
    - 🔴 **高风险** (概率 ≥ 70%): 建议立即专业医学检查
    
    ### 📧 联系方式
    如有问题或建议，请联系开发团队。
    """)
    
    st.markdown("---")
    st.info("最后更新: 2026年4月1日")

# 页脚
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #666; padding: 20px;'>
    <p>🫁 肺癌风险预测系统 v1.0</p>
    <p>使用机器学习预测肺癌风险 | 仅供参考，请咨询专业医疗人士</p>
    </div>
    """, unsafe_allow_html=True)
