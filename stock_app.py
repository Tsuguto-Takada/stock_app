import streamlit as st
import yfinance as yf
from datetime import datetime

# ----------------------------------------------------------------
# ページの基本設定 (このコマンドはスクリプトの最初に一度だけ呼び出す)
# ----------------------------------------------------------------
st.set_page_config(
    page_title="横浜FG 株価チェッカー",
    page_icon="🏦",
    layout="centered"  # スマートフォン表示に適した中央寄せレイアウト
)

# ----------------------------------------------------------------
# ヘルパー関数
# ----------------------------------------------------------------
def format_market_cap(market_cap):
    """
    時価総額を日本の単位（兆、億）を使って分かりやすくフォーマットする関数
    """
    if not isinstance(market_cap, (int, float)):
        return "---"
    
    oku = 10**8
    cho = 10**12
    
    if market_cap >= cho:
        cho_part = int(market_cap / cho)
        oku_part = int((market_cap % cho) / oku)
        return f"{cho_part}兆 {oku_part}億円" if oku_part > 0 else f"{cho_part}兆円"
    elif market_cap >= oku:
        return f"{int(market_cap / oku)}億円"
    else:
        return f"{market_cap:,.0f}円"

# ----------------------------------------------------------------
# メインのデータ取得・表示関数
# ----------------------------------------------------------------
def display_stock_info():
    """
    株価情報を取得して画面に表示するメインの関数
    """
    # 証券コード
    ticker_symbol = "7186.T"

    try:
        # データ取得中にスピナーを表示
        with st.spinner(f"ティッカー'{ticker_symbol}'の最新データを取得中..."):
            ticker = yf.Ticker(ticker_symbol)
            # .infoは時間がかかることがあるため、キャッシュを使わずに毎回取得する
            info = ticker.info

        # --- データ取得の成功チェック ---
        # info辞書が空、または株価情報が含まれていない場合はエラーとみなす
        if not info or 'currentPrice' not in info or info.get('longName') is None:
            st.error("データを取得できませんでした。時間をおいて再読み込みするか、証券コードが正しいか確認してください。")
            st.warning("Yahoo Financeがメンテナンス中の可能性もあります。")
            return # ここで処理を中断

        # --- データの表示 ---
        
        # 会社名と更新時刻
        st.header(info.get('longName', ticker_symbol))
        st.caption(f"最終更新: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        st.divider() # 水平線

        # 1. 株価
        st.subheader("現在の株価")
        current_price = info.get('currentPrice')
        previous_close = info.get('previousClose')

        if current_price and previous_close:
            # Markdownを使って大きな文字で表示
            st.markdown(f"## {current_price:,.2f} 円")
            
            delta = current_price - previous_close
            delta_percent = (delta / previous_close) * 100
            
            # 前日比を色付きで表示
            if delta > 0:
                st.markdown(f'前日比: <span style="color:green;">+{delta:,.2f}円 ({delta_percent:.2f}%)</span>', unsafe_allow_html=True)
            else:
                st.markdown(f'前日比: <span style="color:red;">{delta:,.2f}円 ({delta_percent:.2f}%)</span>', unsafe_allow_html=True)
        else:
            st.markdown("## ---")

        # 2. 時価総額
        st.subheader("時価総額")
        market_cap = info.get('marketCap')
        st.markdown(f"## {format_market_cap(market_cap)}")
        
        st.divider()

        # 3. 企業概要 (折りたたみ形式)
        with st.expander("企業概要を見る"):
            st.write(info.get('longBusinessSummary', '事業概要のデータがありません。'))
            st.write(f"**ウェブサイト**: {info.get('website', 'N/A')}")
            st.write(f"**業種**: {info.get('industry', 'N/A')}")

    except Exception as e:
        # 予期せぬエラーが発生した場合
        st.error("予期せぬエラーが発生しました。インターネット接続を確認して、ページを再読み込みしてください。")
        # 開発者向けにエラー詳細を表示したい場合は以下のコメントを外す
        # st.exception(e)

# ----------------------------------------------------------------
# アプリの実行部分
# ----------------------------------------------------------------
st.title("株価チェッカー")

# メインの表示関数を呼び出す
display_stock_info()

st.divider()
if st.button("最新情報に更新"):
    st.rerun() # ページを再実行して情報を更新する

st.caption("データ取得元: Yahoo Finance")

