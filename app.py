import streamlit as st
import streamlit.components.v1 as components

# ページ設定
st.set_page_config(page_title="Neon Text Generator (JS ver)", layout="wide")

# HTML/JSコードを文字列として定義
# ※ さきほどのコードを少し修正して、Streamlitの枠内に収まるようにしています
html_code = """
<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<style>
    body { background-color: #0e1117; color: white; font-family: sans-serif; margin: 0; padding: 0; }
    .container { display: flex; flex-direction: column; gap: 20px; padding: 20px; }
    .controls { 
        display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px;
        background: #262730; padding: 15px; border-radius: 8px;
    }
    .preview-area {
        text-align: center; background: #000; padding: 10px; border-radius: 8px; border: 1px solid #333;
        overflow: auto; min-height: 300px; display: flex; align-items: center; justify-content: center;
    }
    canvas { max-width: 100%; height: auto; }
    label { display: block; font-size: 0.85em; color: #fafafa; margin-bottom: 5px; }
    input, select, textarea { 
        width: 100%; background: #333; color: white; border: 1px solid #555; padding: 8px; border-radius: 4px; box-sizing: border-box;
    }
    button {
        background: #ff4b4b; color: white; border: none; padding: 10px 20px; border-radius: 4px; cursor: pointer; font-weight: bold; margin-top: 10px;
    }
    button:hover { background: #ff2b2b; }
</style>
<!-- フォント読み込み -->
<link href="https://fonts.googleapis.com/css2?family=Shippori+Mincho+B1:wght@800&display=swap" rel="stylesheet">
</head>
<body>

<div class="container">
    <div class="controls">
        <div><label>テキスト</label><textarea id="t" rows="3">サンプル\nテキスト</textarea></div>
        <div><label>カラー</label>
            <select id="p"><option value="default">Default</option><option value="fire">Fire</option><option value="ice">Ice</option><option value="custom">Custom</option></select>
            <input type="color" id="c" value="#ffffff" style="display:none; margin-top:5px; height:40px;">
        </div>
        <div><label>揺れ (0-20)</label><input type="range" id="s" min="0" max="20" value="2" step="0.5"></div>
        <div><label>発光 (0-1)</label><input type="range" id="g" min="0" max="1" value="0.3" step="0.05"></div>
        <div><label>間隔 (-5-30)</label><input type="range" id="sp" min="-5" max="30" value="3"></div>
        <div><label>サイズ (20-300)</label><input type="range" id="fs" min="20" max="300" value="100"></div>
        <div><label>背景透過</label><input type="checkbox" id="tr"></div>
    </div>
    
    <div class="preview-area">
        <canvas id="cvs"></canvas>
    </div>
    
    <button id="dl">画像を保存 (PNG)</button>
</div>

<script>
    const cvs = document.getElementById('cvs');
    const ctx = cvs.getContext('2d');
    const WIDTH=1920, HEIGHT=1080;
    
    // 入力取得
    const getId = (id) => document.getElementById(id);
    const inputs = ['t','p','c','s','g','sp','fs','tr'].map(getId);
    
    const GRADIENTS = {
        'default': ["#4896A0", "#714A9D", "#984B93"],
        'fire': ["#FF0000", "#FF6600", "#FFFF00"],
        'ice': ["#0099FF", "#00CCFF", "#FFFFFF"]
    };

    function hexToRgb(hex) {
        const bigint = parseInt(hex.slice(1), 16);
        return { r: (bigint >> 16) & 255, g: (bigint >> 8) & 255, b: bigint & 255 };
    }

    function interpolate(c1, c2, f) {
        return {
            r: Math.round(c1.r + (c2.r - c1.r) * f),
            g: Math.round(c1.g + (c2.g - c1.g) * f),
            b: Math.round(c1.b + (c2.b - c1.b) * f)
        };
    }

    function draw() {
        cvs.width = WIDTH; cvs.height = HEIGHT;
        const text = inputs[0].value;
        const preset = inputs[1].value;
        const customC = inputs[2].value;
        const shake = parseFloat(inputs[3].value);
        const glow = parseFloat(inputs[4].value);
        const space = parseInt(inputs[5].value);
        const fsize = parseInt(inputs[6].value);
        const trans = inputs[7].checked;

        // 背景
        if(!trans) { ctx.fillStyle="#000"; ctx.fillRect(0,0,WIDTH,HEIGHT); }
        else { ctx.clearRect(0,0,WIDTH,HEIGHT); }

        ctx.font = fsize + "px 'Shippori Mincho B1'";
        ctx.textBaseline = 'middle';
        
        let colors = (preset === 'custom') ? [hexToRgb(customC), hexToRgb(customC), hexToRgb(customC)] : GRADIENTS[preset].map(hexToRgb);
        
        const lines = text.split('\\n');
        const lineHeight = fsize * 1.15;
        const startY = (HEIGHT - (lines.length * lineHeight)) / 2 + lineHeight/2;
        let totalChars = text.replace(/\\n/g, '').length || 1;
        let charCnt = 0;

        // 描画モード
        ctx.globalCompositeOperation = trans ? 'source-over' : 'lighter';

        lines.forEach((line, li) => {
            let lw = 0;
            for(let c of line) lw += ctx.measureText(c).width + space;
            if(line.length) lw -= space;
            
            let cx = (WIDTH - lw)/2;
            let cy = startY + (li * lineHeight);

            for(let char of line) {
                // 色計算
                let prog = charCnt / Math.max(totalChars-1, 1);
                let colObj = (prog < 0.5) ? interpolate(colors[0], colors[1], prog*2) : interpolate(colors[1], colors[2], (prog-0.5)*2);
                let colStr = `rgb(${colObj.r},${colObj.g},${colObj.b})`;
                
                // 揺れ
                let seed = charCnt * 12.34;
                let rnd = Math.sin(seed); 
                let yOff = (charCnt%2==0?-1:1) * (2 + shake * (0.5+Math.abs(rnd)));

                // グロー描画
                [60,40,20,10].forEach((blur, bi) => {
                    ctx.shadowBlur = blur;
                    ctx.shadowColor = colStr;
                    ctx.fillStyle = colStr;
                    ctx.globalAlpha = [0.4,0.5,0.8,1.0][bi] * glow;
                    ctx.fillText(char, cx, cy+yOff);
                });

                // 本体描画（白）
                ctx.shadowBlur = 0;
                ctx.globalAlpha = 1.0;
                ctx.fillStyle = "#FFF";
                ctx.fillText(char, cx, cy+yOff);

                cx += ctx.measureText(char).width + space;
                charCnt++;
            }
        });
    }

    // イベント
    inputs.forEach(i => i.addEventListener('input', () => {
        if(i.id==='p') inputs[2].style.display = (i.value==='custom')?'block':'none';
        draw();
    }));
    
    getId('dl').onclick = () => {
        const a = document.createElement('a');
        a.download = 'neon_text.png';
        a.href = cvs.toDataURL();
        a.click();
    };

    // 初期化
    document.fonts.ready.then(draw);
    setTimeout(draw, 500); // フォント読み込み遅延対策
</script>
</body>
</html>
"""

# HTMLを埋め込む (高さは適宜調整してください)
components.html(html_code, height=900, scrolling=True)
