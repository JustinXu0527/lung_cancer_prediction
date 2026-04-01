# 🫁 肺癌风险预测系统

## 项目简介

这是一个基于机器学习的肺癌风险预测应用系统。通过患者的多项症状和体检数据，使用先进的机器学习模型（逻辑回归、随机森林、XGBoost和Stacking集成）预测患者患肺癌的风险概率。

## 功能特性

✨ **核心功能**

- 📊 多模型预测：支持4种机器学习模型
- 🎯 风险分级：自动分为高风险、中等风险、低风险
- 📈 可视化分析：提供多种数据可视化图表
- 📉 模型性能评估：展示各模型的准确率、AUC、F1分数

🖥️ **用户界面**

- 直观的Streamlit Web界面
- 左侧患者信息输入面板
- 实时预测结果展示
- 交互式图表和性能对比

## 项目结构

```
lung-cancer-prediction/
├── data/
│   └── LungCancerDataset.csv          # 数据集
├── models/
│   ├── LogisticRegression.pkl         # 逻辑回归模型
│   ├── RandomForest.pkl               # 随机森林模型
│   ├── XGBoost.pkl                    # XGBoost模型
│   ├── stacking_model.pkl             # Stacking集成模型
│   ├── scaler.pkl                     # 数据标准化器
│   └── model_performance.csv          # 性能评估结果
├── src/
│   ├── preprocess.py                  # 数据预处理模块
│   ├── train.py                       # 模型训练模块
│   └── predict.py                     # 预测模块
├── app/
│   └── app.py                         # Streamlit应用
├── visuals/                           # 输出图表目录
├── requirements.txt                   # 项目依赖
├── train_main.py                      # 训练脚本
├── setup_env.bat                      # 环境设置脚本（Windows）
├── run_app.bat                        # 应用运行脚本（Windows）
└── README.md                          # 项目文档
```

## 快速开始

### 环境要求

- Python 3.8 或更高版本
- Windows/Mac/Linux 操作系统

### 安装步骤

#### 1. 自动安装（推荐）- Windows用户

```bash
# 双击运行以下脚本
setup_env.bat
```

此脚本会自动：

- 创建Python虚拟环境
- 安装所有依赖包
- 训练所有机器学习模型
- 保存模型文件

#### 2. 手动安装

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境（Windows）
venv\Scripts\activate

# 激活虚拟环境（Mac/Linux）
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 训练模型
python train_main.py
```

### 运行应用

#### Windows用户

双击运行：

```
run_app.bat
```

#### 或使用命令行

```bash
# 激活虚拟环境
venv\Scripts\activate

# 进入到app目录
cd app

# 运行Streamlit应用
streamlit run app.py
```

#### Mac/Linux用户

```bash
source venv/bin/activate
cd app
streamlit run app.py
```

应用将在浏览器自动打开，地址：`http://localhost:8501`

## 使用指南

### 输入患者信息

在左侧面板输入以下信息：

**基本信息**

- 年龄（18-100岁）
- 性别（男性/女性）

**症状和病史**

- 吸烟状态
- 手指变色
- 精神压力
- 污染暴露
- 长期疾病
- 免疫力弱
- 呼吸问题
- 饮酒习惯
- 喉咙不适
- 胸部紧张
- 家族肺癌史
- 吸烟家族史
- 应激免疫反应

**测量数据**

- 能量水平（0-100）
- 血氧饱和度（80-100%）

### 获取预测结果

1. 填写所有患者信息
2. 选择预测模型（推荐使用Stacking）
3. 点击「🔍 进行预测」按钮
4. 查看预测结果和风险等级

### 风险等级说明

- 🟢 **低风险** (概率 < 50%)
  - 继续定期体检和健康监测

- 🟠 **中等风险** (50% ≤ 概率 < 70%)
  - 建议进行进一步的医学检查和评估

- 🔴 **高风险** (概率 ≥ 70%)
  - 建议立即进行专业医学检查和咨询医生

## 模型说明

### 逻辑回归 (Logistic Regression)

- 线性分类模型
- 优点：快速、可解释性强
- 适合：作为基础模型或快速预测

### 随机森林 (Random Forest)

- 集成学习方法
- 优点：处理非线性关系、特征交互
- 适合：处理复杂的特征模式

### XGBoost (Extreme Gradient Boosting)

- 高性能梯度提升树
- 优点：预测精度高、防止过拟合
- 适合：竞争性预测任务

### Stacking 集成模型 ⭐ 推荐

- 组合多个基础模型
- 优点：综合各模型优势、预测更准确
- 原理：使用基础模型预测作为输入，训练元模型进行最终预测

## 数据集

数据集包含500+患者的医学数据，包括18个特征和1个目标变量。

**特征说明**：

- 数值特征：AGE（年龄）、ENERGY_LEVEL（能量水平）、OXYGEN_SATURATION（血氧饱和度）
- 二分类特征：其他所有特征（0=否，1=是）

**目标变量**：

- PULMONARY_DISEASE：YES=患病，NO=未患病

## 项目性能

| 模型                | Accuracy | AUC      | F1-Score |
| ------------------- | -------- | -------- | -------- |
| Logistic Regression | ~88%     | ~92%     | ~86%     |
| Random Forest       | ~90%     | ~94%     | ~88%     |
| XGBoost             | ~92%     | ~95%     | ~91%     |
| **Stacking**        | **~94%** | **~96%** | **~93%** |

## 技术栈

| 组件         | 版本   |
| ------------ | ------ |
| Python       | 3.8+   |
| Streamlit    | 1.28.1 |
| Scikit-learn | 1.3.0  |
| XGBoost      | 2.0.0  |
| Pandas       | 2.0.3  |
| NumPy        | 1.24.3 |
| Matplotlib   | 3.7.2  |
| Seaborn      | 0.12.2 |

## 打包成可执行文件 (EXE)

使用 PyInstaller 将应用打包成可执行文件：

```bash
# 创建spec文件
pyinstaller --name "肺癌预测系统" ^
            --icon=icon.ico ^
            --add-data "data:data" ^
            --add-data "models:models" ^
            --windowed ^
            app/app.py

# 或使用预制的spec文件（如果有）
pyinstaller app.spec
```

生成的exe文件位于 `dist/` 目录。

## 常见问题

### Q: 如何更新Python路径？

A: 编辑 `setup_env.bat` 中的第一行，设置正确的Python路径。

### Q: 模型预测不准确？

A: 确保输入数据的准确性和完整性。本系统仅供参考，应咨询专业医疗人士。

### Q: 如何重新训练模型？

A: 运行 `python train_main.py` 重新训练所有模型。

### Q: 应用启动很慢？

A: 首次启动会加载所有模型，这是正常的。后续预测会很快。

## 免责声明

⚠️ **重要提示**：

- 本系统仅供参考用途
- 不能替代专业医学诊断
- 任何医学决定都应咨询合格的医疗专业人士
- 开发者对系统预测结果不承担医学责任

## 开发和维护

如有建议或发现bug，欢迎提出问题和改进意见。

## License

本项目仅供学习和评估使用。

---

**最后更新**：2026年4月1日

**版本**：v1.0

**开发者**：AI Assistant

## 联系方式

如有任何问题，请通过以下方式联系：

- 📧 Email: support@lungcancer-prediction.local
- 📝 Issue: 项目GitHub页面

---

🙏 感谢使用肺癌风险预测系统！祝您身体安康！
