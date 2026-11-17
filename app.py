import streamlit as st
import pandas as pd
import random
import time

# 1. 页面基本配置（适配平板和手机全屏）
st.set_page_config(
    page_title="Crypto Arbitrage Dashboard",
    page_icon="📈",
    layout="wide"
)

# 2. 页面顶部标题与指标看板
st.title("🚀 AI 加密货币跨市场套利监控台")
st.markdown("实时监控 **Binance** 与 **Kraken** 的 `BTC/USDT` 价差，并运行模拟纸上交易（Paper Trading）。")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("模拟账户总资产", "$1,045.50 USDT", "+$45.50 (+4.55%)")
with col2:
    st.metric("已捕捉套利机会", "12 次", "过去 24 小时")
with col3:
    st.metric("当前最高净价差", "0.24%", "Binance ➡️ Kraken")
with col4:
    st.metric("系统运行状态", "🟢 正常监控中", "延迟: 42ms")

st.divider()

# 3. 中间区域：左侧实时行情表，右侧控制面板
col_left, col_right = st.columns([2, 1])

with col_left:
    st.subheader("📊 实时跨交易所盘口对比")
    chart_data = pd.DataFrame({
        "时间": ["12:00:01", "12:00:04", "12:00:07", "12:00:10", "12:00:13"],
        "Binance 卖一价": [91200.5, 91210.0, 91195.0, 91220.0, 91215.5],
        "Kraken 买一价": [91180.0, 91205.0, 91200.0, 91218.0, 91210.0],
        "扣费后净价差 (%)": [-0.08, -0.05, 0.02, -0.03, -0.01]
    })
    st.dataframe(chart_data, use_container_width=True)

with col_right:
    st.subheader("⚙️ 机器人控制面板")
    st.slider("单笔模拟仓位 (USDT)", 50, 1000, 100, 50)
    st.slider("最小触发净价差阈值 (%)", 0.05, 0.50, 0.15, 0.01)
    
    if st.button("🔄 立即手动扫描一次", use_container_width=True):
        st.toast("扫描完成：当前未发现符合条件的套利空间", icon="🔍")

    if st.button("🛑 紧急停止监控", type="primary", use_container_width=True):
        st.warning("监控已暂停")

st.divider()

# 4. 底部区域：模拟交易账本明细
st.subheader("📝 模拟交易成交日志 (Paper Trading Ledger)")
log_data = pd.DataFrame({
    "成交时间": ["2026-03-31 11:45:10", "2026-03-31 11:32:05", "2026-03-31 11:10:22"],
    "方向": ["Binance ➡️ Kraken", "Kraken ➡️ Binance", "Binance ➡️ Kraken"],
    "投入资金 (USDT)": [100.0, 100.0, 100.0],
    "净收益率 (%)": ["+0.18%", "+0.22%", "+0.15%"],
    "获利金额 (USDT)": ["+$0.18", "+$0.22", "+$0.15"],
    "账户余额": ["$1,045.50", "$1,045.32", "$1,045.10"]
})
st.table(log_data)
