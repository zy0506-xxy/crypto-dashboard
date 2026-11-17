import streamlit as st
import pandas as pd
import ccxt

st.set_page_config(page_title="Crypto Arbitrage Live", layout="wide")

st.title("🚀 AI 加密货币跨市场套利监控台 (实盘版)")
st.markdown("正在通过 `ccxt` 实时连接 **Binance** 与 **Kraken** 获取真实盘口数据...")

@st.cache_data(ttl=10)
def get_prices():
    try:
        binance = ccxt.binance({'enableRateLimit': True})
        kraken = ccxt.kraken({'enableRateLimit': True})
        
        b_ticker = binance.fetch_ticker('BTC/USDT')
        k_ticker = kraken.fetch_ticker('BTC/USDT')
        
        b_ask = b_ticker['ask'] or 0.0
        b_bid = b_ticker['bid'] or 0.0
        k_ask = k_ticker['ask'] or 0.0
        k_bid = k_ticker['bid'] or 0.0
        
        spread = ((k_bid - b_ask) / b_ask) * 100 if b_ask > 0 else 0
        
        return {
            "status": "🟢 实盘连接正常",
            "b_ask": b_ask, "b_bid": b_bid,
            "k_ask": k_ask, "k_bid": k_bid,
            "spread": round(spread, 4)
        }
    except Exception as e:
        return {"status": f"🔴 异常: {str(e)}", "b_ask": 0, "b_bid": 0, "k_ask": 0, "k_bid": 0, "spread": 0}

d = get_prices()

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("系统状态", d["status"])
with col2:
    st.metric("Binance 卖一价", f"${d['b_ask']:,.2f}")
with col3:
    st.metric("Kraken 买一价", f"${d['k_bid']:,.2f}")
with col4:
    st.metric("当前净价差", f"{d['spread']}%")

st.divider()

st.subheader("📊 实时盘口数据对比")
df = pd.DataFrame({
    "交易所": ["Binance (币安)", "Kraken (K网)"],
    "买一价 (Bid)": [d["b_bid"], d["k_bid"]],
    "卖一价 (Ask)": [d["b_ask"], d["k_ask"]]
})
st.dataframe(df, use_container_width=True)

if st.button("🔄 刷新行情"):
    st.rerun()
