import streamlit as st
import pandas as pd
import ccxt
from datetime import datetime

st.set_page_config(page_title="Crypto Arbitrage Live & Auto-Trader", layout="wide")

st.title("🚀 AI 加密货币跨市场套利监控与自动模拟交易台")
st.markdown("正在通过 `ccxt` 实时连接 **Coinbase** 与 **Kraken** 获取真实盘口，并在后台执行自动化价差监控...")

# 初始化 Session State 用于记录模拟交易日志
if "trade_logs" not in st.session_state:
    st.session_state.trade_logs = []

@st.cache_data(ttl=10)
def get_prices():
    try:
        coinbase = ccxt.coinbase({'enableRateLimit': True})
        kraken = ccxt.kraken({'enableRateLimit': True})
        
        c_ticker = coinbase.fetch_ticker('BTC/USD')
        k_ticker = kraken.fetch_ticker('BTC/USD')
        
        c_ask = c_ticker['ask'] or 0.0
        c_bid = c_ticker['bid'] or 0.0
        k_ask = k_ticker['ask'] or 0.0
        k_bid = k_ticker['bid'] or 0.0
        
        # 路径1: Coinbase 买入, Kraken 卖出
        spread_1 = ((k_bid - c_ask) / c_ask) * 100 if c_ask > 0 else 0
        # 路径2: Kraken 买入, Coinbase 卖出
        spread_2 = ((c_bid - k_ask) / k_ask) * 100 if k_ask > 0 else 0
        
        return {
            "status": "🟢 实盘连接与监控正常",
            "c_ask": c_ask, "c_bid": c_bid,
            "k_ask": k_ask, "k_bid": k_bid,
            "spread_1": round(spread_1, 4),
            "spread_2": round(spread_2, 4)
        }
    except Exception as e:
        return {
            "status": f"🔴 异常: {str(e)}",
            "c_ask": 0, "c_bid": 0, "k_ask": 0, "k_bid": 0,
            "spread_1": 0, "spread_2": 0
        }

d = get_prices()

# 顶部指标
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("系统状态", d["status"])
with col2:
    st.metric("Coinbase 卖一价", f"${d['c_ask']:,.2f}")
with col3:
    st.metric("Kraken 买一价", f"${d['k_bid']:,.2f}")
with col4:
    max_spread = max(d["spread_1"], d["spread_2"])
    st.metric("当前最大净价差", f"{max_spread}%")

st.divider()

# 盘口与控制面板
col_left, col_right = st.columns([2, 1])

with col_left:
    st.subheader("📊 实时盘口数据对比")
    df = pd.DataFrame({
        "交易所": ["Coinbase (C网)", "Kraken (K网)"],
        "买一价 (Bid)": [d["c_bid"], d["k_bid"]],
        "卖一价 (Ask)": [d["c_ask"], d["k_ask"]]
    })
    st.dataframe(df, use_container_width=True)

with col_right:
    st.subheader("⚙️ 自动化策略配置")
    position_size = st.slider("单笔模拟仓位 (USD)", 100, 2000, 500, 100)
    threshold = st.slider("自动触发套利阈值 (%)", 0.01, 0.50, 0.05, 0.01)
    
    auto_trade_enabled = st.toggle("启用自动模拟下单监控", value=True)

# 自动触发下单核心逻辑检测
if auto_trade_enabled and d["status"].startswith("🟢"):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 检查方向1: Coinbase买入 -> Kraken卖出
    if d["spread_1"] >= threshold:
        log_entry = {
            "时间": current_time,
            "方向": "Coinbase 买入 ➡️ Kraken 卖出",
            "触发价差": f"{d['spread_1']}%",
            "模拟金额": f"${position_size}",
            "状态": "模拟成交 ✅"
        }
        if not st.session_state.trade_logs or st.session_state.trade_logs[0]["触发价差"] != f"{d['spread_1']}%":
            st.session_state.trade_logs.insert(0, log_entry)
            
    # 检查方向2: Kraken买入 -> Coinbase卖出
    elif d["spread_2"] >= threshold:
        log_entry = {
            "时间": current_time,
            "方向": "Kraken 买入 ➡️ Coinbase 卖出",
            "触发价差": f"{d['spread_2']}%",
            "模拟金额": f"${position_size}",
            "状态": "模拟成交 ✅"
        }
        if not st.session_state.trade_logs or st.session_state.trade_logs[0]["触发价差"] != f"{d['spread_2']}%":
            st.session_state.trade_logs.insert(0, log_entry)

st.divider()

# 底部策略运行与成交日志
col_log1, col_log2 = st.columns([4, 1])
with col_log1:
    st.subheader("📝 自动化策略运行与模拟成交日志")
with col_log2:
    if st.button("🗑️ 清空日志"):
        st.session_state.trade_logs = []
        st.rerun()

if st.session_state.trade_logs:
    log_df = pd.DataFrame(st.session_state.trade_logs)
    st.dataframe(log_df, use_container_width=True)
else:
    st.info("💡 监控中：当实时价差达到或超过上方设定的阈值时，系统将自动记录模拟成交事件。你可以把阈值调低一点（如 0.01%）来测试触发效果。")

if st.button("🔄 立即强制刷新行情"):
    st.rerun()
