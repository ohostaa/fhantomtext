import streamlit as st
import main
from io import BytesIO

st.set_page_config(page_title="Neon Text Generator", layout="wide")

st.title("ファンパレコラ画像生成ツール")

# サイドバーに入力フォームを配置
with st.sidebar:
    st.header("設定")
    text = st.text_area("テキスト", "サンプル\nテキスト")
    
    preset = st.selectbox("グラデーション", ["default", "fire", "ice", "custom"])
    
    custom_color = None
    if preset == "custom":
        custom_color = st.color_picker("カスタムカラー", "#FFFFFF")
    
    shake_pattern = st.selectbox("揺れパターン", ["random", "sin", "fixed"])
    shake = st.slider("揺れ幅", 0, 20, 2)
    glow = st.slider("発光強度", 0.0, 1.0, 0.28)
    spacing = st.slider("文字間隔", 0, 20, 3)
    
    fontsize = st.number_input("フォントサイズ (0=自動)", value=0, min_value=0)
    transparent = st.checkbox("背景透過", value=False)
    
    generate_btn = st.button("生成する")

# メインエリアに画像表示
if generate_btn:
    with st.spinner("生成中..."):
        try:
            # text2.pyの関数を呼び出し
            img = text2.generate_neon_image(
                text=text,
                gradient_preset=preset if preset != "custom" else "default",
                custom_color=custom_color,
                spacing=spacing,
                shake=shake,
                glow=glow,
                fontsize=fontsize,
                transparent=transparent,
                pattern=shake_pattern
            )
            
            # 画像を表示
            st.image(img, caption="Generated Image", use_container_width=True)
            
            # ダウンロードボタン用バッファ
            buf = BytesIO()
            img.save(buf, format="PNG")
            byte_im = buf.getvalue()
            
            st.download_button(
                label="画像をダウンロード",
                data=byte_im,
                file_name="neon_text.png",
                mime="image/png"
            )
            
        except Exception as e:
            st.error(f"エラーが発生しました")
