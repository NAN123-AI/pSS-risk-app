import streamlit as st
import numpy as np
from scipy.interpolate import interp1d

# 设置网页标题与布局
st.set_page_config(page_title="干燥综合征血小板减少风险预测", layout="centered")

# 页面标题
st.title("🔬 原发性干燥综合征患者血小板减少风险预测")
st.markdown("""
请根据下列指标填写数据，系统将预测您发生**血小板减少**的概率。  
此工具基于列线图模型设计，结合口干眼干症状、抗SSA抗体水平、ProGRP浓度来计算风险。
""")

# --- 用户输入 ---
dry = st.checkbox("是否存在口干眼干症状？", value=False)
anti_ssa = st.slider("抗SSA抗体水平（单位：AU/mL）", min_value=0.0, max_value=300.0, value=150.0, step=1.0)
progrp = st.slider("胃泌素释放肽前体 ProGRP（单位：pg/mL）", min_value=0.0, max_value=65.0, value=30.0, step=1.0)

# --- 风险计算函数 ---
def calculate_points(dry_mouth_eye: int, anti_ssa: float, progrp: float):
    points_dry = 20 if dry_mouth_eye == 1 else 0
    points_ssa = min(anti_ssa / 3, 100)
    points_progrp = min((65 - progrp) / 65 * 100, 100)
    total_points = points_dry + points_ssa + points_progrp
    return points_dry, points_ssa, points_progrp, total_points

def points_to_risk(points: float):
    # 插值法将总分映射为概率
    point_list = [0, 60, 100, 140, 180]
    risk_list = [0.1, 0.3, 0.5, 0.7, 0.9]
    interpolate = interp1d(point_list, risk_list, kind='linear', fill_value="extrapolate")
    return float(interpolate(points))

# --- 预测执行 ---
if st.button("🔎 计算预测风险"):
    dry_val = 1 if dry else 0
    p_dry, p_ssa, p_progrp, total = calculate_points(dry_val, anti_ssa, progrp)
    risk = points_to_risk(total)

    # 展示预测结果
    st.subheader("📊 预测结果")
    st.metric("口干眼干得分", f"{p_dry:.1f}")
    st.metric("抗SSA抗体得分", f"{p_ssa:.1f}")
    st.metric("ProGRP得分", f"{p_progrp:.1f}")
    st.metric("总得分", f"{total:.1f}")

    st.markdown("### 🎯 血小板减少预测概率")
    st.progress(min(risk, 1.0))
    st.success(f"预测风险概率为：**{risk*100:.1f}%**")
