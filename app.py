import streamlit as st
import pandas as pd
import ccxt

st.set_page_config(page_title="Coinbase Live Monitor", layout="wide")

st.title("🚀 Coinbase 加密货币实时行情监控台")
st.markdown("正在通过 `ccxt` 实时连接 **Coinbase** 获取 BTC/USD 真实盘口数据...")

@st.cache_data(ttl=10)
def get_coinbase_price():
    try:
        coinbase = ccxt.coinbase({'enableRateLimit': True})
        ticker = coinbase.fetch_ticker('BTC/USD')
        
        ask = ticker['ask'] or 0.0
        bid = ticker['bid'] or 0.0
        last = ticker['last'] or 0.0
        
        return {
            "status": "🟢 Coinbase 连接正常",
            "ask": ask,
            "bid": bid,
            "last": last
        }
    except Exception as e:
        return {"status": f"🔴 异常: {str(e)}", "ask": 0, "bid": 0, "last": 0}

d = get_coinbase_price()

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("系统状态", d["status"])
with col2:
    st.metric("卖一价 (Ask)", f"${d['ask']:,.2f}")
with col3:
    st.metric("买一价 (Bid)", f"${d['bid']:,.2f}")
with col4:
    st.metric("最新成交价 (Last)", f"${d['last']:,.2f}")

st.divider()

st.subheader("📊 Coinbase 盘口明细")
df = pd.DataFrame({
    "交易对": ["BTC/USD"],
    "买一价 (Bid)": [d["bid"]],
    "卖一价 (Ask)": [d["ask"]],
    "最新价": [d["last"]]
})
st.dataframe(df, use_container_width=True)

if st.button("🔄 刷新行情"):
    st.rerun()
