import streamlit as st
import yfinance as yf

# ----------------------------------------------------------------
# ユーティリティ関数（変更なし）
# ----------------------------------------------------------------
def format_market_cap(market_cap):
    """
    時価総額を日本の単位（兆、億）を使って分かりやすくフォーマットする関数
    """
    if market_cap is None:
        return "データなし"
    
    oku = 10**8
    cho = 10**12
    
    if market_cap >= cho:
        cho_part = int(market_cap / cho)
        oku_part = int((market_cap % cho) / oku)
        if oku_part > 0:
            return f"{cho_part}兆 {oku_part}億円"
        else:
            return f"{cho_part}兆円"
    elif market_cap >= oku:
        oku_part = int(market_cap / oku)
        return f"{oku_part}億円"
    else:
        return f"{market_cap:,.0f}円"

# ----------------------------------------------------------------
# Streamlit アプリケーション（表示方法を大幅にシンプル化）
# ----------------------------------------------------------------

# ページの基本設定
st.set_page_config(page_title="横浜FG 株価情報", layout="centered")

st.title("🏦 横浜フィナンシャルグループ 株価情報")

# 証券コード
ticker_symbol = "7186.T"

try:
    with st.spinner('株価データを取得中です...'):
        ticker = yf.Ticker(ticker_symbol)
        info = ticker.info

    if not info or 'longName' not in info:
        st.error("株価データを取得できませんでした。時間をおいて再読み込みしてください。")
    else:
        # --- ここから表示方法を最もシンプルな形式に変更 ---

        st.header(info.get('longName', ticker_symbol))
        st.markdown("---")

        # 1. 現在の株価
        st.subheader("現在の株価")
        current_price = info.get('currentPrice')
        previous_close = info.get('previousClose')
        
        if current_price and previous_close:
            price_text = f"## {current_price:,.2f} 円"
            st.markdown(price_text)
            
            delta = current_price - previous_close
            delta_text = f"前日比: {delta:,.2f} 円"
            st.write(delta_text)
        else:
            st.write("取得不可")

        # 2. 時価総額
        st.subheader("時価総額")
        market_cap = info.get('marketCap')
        cap_text = f"## {format_market_cap(market_cap)}"
        st.markdown(cap_text)
        
        st.markdown("---")

        # 3. 企業概要
        st.subheader("企業概要")
        st.write(f"**業種**: {info.get('industry', 'N/A')}")
        st.write(f"**ウェブサイト**: {info.get('website', 'N/A')}")
        st.write(info.get('longBusinessSummary', '事業概要のデータがありません。'))
        
        st.caption("データ取得元: Yahoo Finance")

except Exception as e:
    st.error("エラーが発生しました。アプリの管理者に連絡してください。")
    # st.error(f"エラー詳細: {e}") # ユーザーには詳細を見せない方が親切な場合も

