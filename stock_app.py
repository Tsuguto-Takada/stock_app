import streamlit as st
import yfinance as yf

# ----------------------------------------------------------------
# ユーティリティ関数
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
# Streamlit アプリケーション
# ----------------------------------------------------------------

# ページの基本設定 (最初に呼び出す)
st.set_page_config(
    page_title="横浜FG 株価情報",
    page_icon="🏦",
    layout="centered" # スマホ表示に適したレイアウト
)

st.title("🏦 横浜フィナンシャルグループ 株価情報")

# 証券コード
ticker_symbol = "7186.T"

try:
    with st.spinner('最新の株価データを取得中です...'):
        # yfinance Tickerオブジェクトを作成
        ticker = yf.Ticker(ticker_symbol)
        
        # 企業情報を一括で取得
        info = ticker.info

    # info辞書が空、または主要なキーがない場合はエラーとする
    if not info or 'longName' not in info:
        st.error("株価データを取得できませんでした。証券コードが正しいか、または一時的な問題が発生している可能性があります。")
    else:
        # --- メイン情報の表示 ---
        st.header(f"{info.get('longName', ticker_symbol)}")

        # st.columns を使ってPCとスマホの表示を最適化
        col1, col2 = st.columns(2)

        with col1:
            current_price = info.get('currentPrice')
            previous_close = info.get('previousClose')
            
            if current_price and previous_close:
                delta = current_price - previous_close
                st.metric(
                    label="現在の株価", 
                    value=f"{current_price:,.2f} 円", 
                    delta=f"{delta:,.2f} 円"
                )
            else:
                st.metric(label="現在の株価", value="取得不可")

        with col2:
            market_cap = info.get('marketCap')
            st.metric(label="時価総額", value=format_market_cap(market_cap))
        
        st.divider() # 水平線

        # --- 詳細情報の表示 (折りたたみ) ---
        with st.expander("企業概要を見る"):
            st.markdown(f"""
            - **業種**: {info.get('industry', 'N/A')}
            - **ウェブサイト**: {info.get('website', 'N/A')}
            """)
            st.write(info.get('longBusinessSummary', '事業概要のデータがありません。'))
        
        st.caption("データ取得元: Yahoo Finance")

except Exception as e:
    st.error(f"予期せぬエラーが発生しました。ページを再読み込みしてください。")
    st.error(f"エラー詳細: {e}")
