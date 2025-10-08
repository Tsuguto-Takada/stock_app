import streamlit as st
import yfinance as yf
import math

def format_market_cap(market_cap):
    """
    時価総額を日本の単位（兆、億）を使ってフォーマットする関数
    """
    if market_cap is None:
        return "データなし"
    
    oku = 10**8
    cho = 10**12
    
    if market_cap >= cho:
        cho_part = int(market_cap / cho)
        oku_part = int((market_cap % cho) / oku)
        if oku_part > 0:
            return f"{cho_part}兆{oku_part}億円"
        else:
            return f"{cho_part}兆円"
    elif market_cap >= oku:
        oku_part = int(market_cap / oku)
        return f"{oku_part}億円"
    else:
        return f"{market_cap:,.0f}円"

# --- Streamlit App ---

st.title("横浜フィナンシャルグループ 株価情報")

# 証券コード
ticker_symbol = "7186.T"

try:
    # yfinanceで株価情報を取得
    ticker = yf.Ticker(ticker_symbol)
    info = ticker.info

    # データが取得できたか確認
    if not info or 'currentPrice' not in info or 'marketCap' not in info:
        st.error("株価データを取得できませんでした。証券コードが正しいか確認してください。")
    else:
        # 最新の株価と時価総額を取得
        latest_price = info['currentPrice']
        market_cap = info['marketCap']

        # フォーマットされた時価総額
        formatted_cap = format_market_cap(market_cap)

        # 画面に表示
        st.header(f"{info.get('longName', ticker_symbol)} の株価情報")
        
        st.metric(label="現在の株価", value=f"{latest_price:,.2f} 円")
        st.metric(label="時価総額", value=formatted_cap)

        st.write("---")
        st.write("取得元: Yahoo Finance")

except Exception as e:
    st.error(f"エラーが発生しました: {e}")
