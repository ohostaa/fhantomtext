import streamlit as st
import text
from io import BytesIO

st.set_page_config(page_title="Neon Text Generator", layout="wide")

# タイトルを少し控えめに
st.markdown("### ファントムパレード風ネオンテキスト生成")

# ■ キャッシュ機能を追加 ■
# 同じパラメータなら再計算せず、メモリから結果を呼び出す（高速化）
@st.cache_data(show_spinner=False) 
def get_neon_image(texti, preset, custom_color, spacing, shake, glow, fontsize, transparent, shake_pattern):
    return text.generate_neon_image(
        text=texti,
        gradient_preset=preset if preset != "custom" else "default",
        custom_color=custom_color,
        spacing=spacing,
        shake=shake,
        glow=glow,
        fontsize=fontsize,
        transparent=transparent,
        pattern=shake_pattern
    )

# 2カラムレイアウト（左：設定、右：プレビュー）
col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("##### 設定")
    # 変数名を user_text に変更して競合回避
    user_text = st.text_area("テキスト", "サンプル\nテキスト", height=100)
    
    preset = st.selectbox("カラープリセット", ["default", "fire", "ice", "custom"])
    
    custom_color = None
    if preset == "custom":
        custom_color = st.color_picker("カスタムカラー", "#FFFFFF")
    
    shake_pattern = st.selectbox("揺れパターン", ["random", "sin", "fixed"])
    shake = st.slider("揺れ幅", 0, 20, 2)
    glow = st.slider("発光強度", 0.0, 1.0, 0.28)
    spacing = st.slider("文字間隔", 0, 20, 3)
    
    fontsize = st.number_input("フォントサイズ (0=自動)", value=0, min_value=0)
    transparent = st.checkbox("背景透過", value=False)

with col2:
    # ボタン判定をやめ、常に実行するように変更
    if user_text:
        try:
            # キャッシュ付き関数を呼び出し
            img = get_neon_image(
                user_text, preset, custom_color, spacing, shake, glow, fontsize, transparent, shake_pattern
            )
            
            # 画像表示
            st.image(img, caption="プレビュー", use_container_width=False)
            
            # ダウンロードボタン
            buf = BytesIO()
            img.save(buf, format="PNG")
            byte_im = buf.getvalue()
            
            st.download_button(
                label="画像を保存 (PNG)",
                data=byte_im,
                file_name="neon_text.png",
                mime="image/png"
            )
        except Exception as e:
            st.error(f"エラーが発生しました: {e}")
    else:
        st.info("テキストを入力してください")
