import streamlit as st
import streamlit.components.v1 as components

# ページ設定
st.set_page_config(page_title="Neon Text Generator", layout="wide", initial_sidebar_state="collapsed")

# ■ CSSハック: 全画面固定・スクロール禁止設定 ■
st.markdown("""
<style>
    /* ヘッダー・フッター・パディング全削除 */
    header, footer { visibility: hidden; display: none; }
    
    .block-container {
        padding: 0 !important;
        max-width: 100% !important;
    }
    
    /* アプリ全体のスクロール禁止 */
    body {
        overflow: hidden !important;
        margin: 0 !important;
    }
    
    /* Streamlitのメインコンテナのスクロール禁止 */
    .stApp {
        overflow: hidden !important;
    }

    /* iframeを画面いっぱいに広げる */
    iframe {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw !important;
        height: 100vh !important;
        border: none;
        z-index: 9999;
    }
</style>
""", unsafe_allow_html=True)

# HTML/JSコード（内容は変更なし）
html_code = """
<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<style>
    :root {
        --bg-color: #0e1117;
        --panel-bg: #1e1e1e;
        --border-color: #333;
        --accent-color: #4896A0;
        --text-color: #e0e0e0;
    }
    body { 
        background-color: var(--bg-color); 
        color: var(--text-color); 
        font-family: "Helvetica Neue", Arial, sans-serif;
        margin: 0; padding: 0;
        width: 100vw; height: 100vh;
        overflow: hidden; /* ブラウザ自体のスクロール禁止 */
    }
    
    .app-container {
        display: flex;
        width: 100%;
        height: 100%;
    }

    /* 左: 設定パネル (縦スクロール許可) */
    .sidebar {
        width: 340px;
        min-width: 340px;
        background: var(--panel-bg);
        border-right: 1px solid var(--border-color);
        padding: 20px;
        overflow-y: auto; /* ここだけスクロール可能 */
        height: 100%; 
        box-sizing: border-box;
        display: flex; flex-direction: column; gap: 20px;
        z-index: 10;
    }
    
    /* スクロールバー装飾 */
    .sidebar::-webkit-scrollbar { width: 8px; }
    .sidebar::-webkit-scrollbar-track { background: #1e1e1e; }
    .sidebar::-webkit-scrollbar-thumb { background: #555; border-radius: 4px; }

    .group-title {
        font-size: 0.85em; font-weight: bold; color: #888;
        border-bottom: 1px solid #444; padding-bottom: 5px;
        margin-bottom: 10px; text-transform: uppercase; letter-spacing: 1px;
        margin-top: 10px;
    }
    .group-title:first-child { margin-top: 0; }

    .control-item { margin-bottom: 15px; }
    
    label { 
        display: flex; justify-content: space-between;
        font-size: 0.9em; margin-bottom: 6px; color: #ccc; 
    }
    .val-display { color: var(--accent-color); font-weight: bold; }

    input[type="text"], textarea, select {
        width: 100%; background: #2b2b2b; border: 1px solid #444;
        color: white; padding: 10px; border-radius: 6px; box-sizing: border-box; font-size: 14px;
        font-family: inherit;
    }
    textarea { resize: vertical; min-height: 100px; }
    input[type="range"] { width: 100%; cursor: pointer; margin-top: 5px; }

    /* 右: プレビューエリア (完全固定) */
    .main-area {
        flex: 1;
        display: flex;
        flex-direction: column;
        background: #000;
        position: relative;
        height: 100%;
        overflow: hidden;
    }
    
    .canvas-container {
        flex: 1;
        display: flex;
        align-items: center;
        justify-content: center;
        background-image: 
            linear-gradient(45deg, #1a1a1a 25%, transparent 25%), 
            linear-gradient(-45deg, #1a1a1a 25%, transparent 25%), 
            linear-gradient(45deg, transparent 75%, #1a1a1a 75%), 
            linear-gradient(-45deg, transparent 75%, #1a1a1a 75%);
        background-size: 24px 24px;
        overflow: hidden;
        position: relative;
    }

    canvas {
        max-width: 90%; 
        max-height: 90%; 
        object-fit: contain;
        box-shadow: 0 0 30px rgba(0,0,0,0.8);
        border: 1px solid #333;
    }

    .toolbar {
        height: 60px;
        background: #111;
        border-top: 1px solid #333;
        display: flex;
        align-items: center;
        justify-content: flex-end;
        padding: 0 20px;
        box-sizing: border-box;
    }

    button.download-btn {
        background: var(--accent-color); color: white; border: none;
        padding: 10px 24px; border-radius: 6px; font-weight: bold;
        cursor: pointer; transition: all 0.2s; font-size: 0.95em;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        display: flex; align-items: center; gap: 8px;
    }
    button.download-btn:hover { background: #5abac6; transform: translateY(-1px); }
    button.download-btn:active { transform: translateY(1px); }

    #custom-color-group { display: none; margin-top: 10px; }
    input[type="color"] { width: 100%; height: 40px; border: none; padding: 0; cursor: pointer; border-radius: 4px; }

</style>
<link href="https://fonts.googleapis.com/css2?family=Shippori+Mincho+B1:wght@800&display=swap" rel="stylesheet">
</head>
<body>

<div class="app-container">
    <div class="sidebar">
        <h2 style="margin:0 0 10px 0; font-size:1.2em; color:#fff;">Neon Generator</h2>
        
        <div class="group-title">Content</div>
        <div class="control-item">
            <label>Text</label>
            <textarea id="textInput" spellcheck="false">サンプル\\nテキスト</textarea>
        </div>
        
        <div class="group-title">Style & Color</div>
        <div class="control-item">
            <label>Color Preset</label>
            <select id="preset">
                <option value="default">Default (Blue/Purple)</option>
                <option value="fire">Fire (Red/Yellow)</option>
                <option value="ice">Ice (Blue/Cyan)</option>
                <option value="custom">Custom Color</option>
            </select>
            <div id="custom-color-group">
                <input type="color" id="customColor" value="#ffffff">
            </div>
        </div>
        <div class="control-item" style="display:flex; align-items:center; gap:10px; background:#252525; padding:10px; border-radius:6px;">
            <input type="checkbox" id="transparent" style="width:20px; height:20px; margin:0; cursor:pointer;">
            <label style="margin:0; cursor:pointer; color:#fff;" for="transparent">Transparent Background</label>
        </div>

        <div class="group-title">Typography</div>
        <div class="control-item">
            <label>Font Size <span id="v_fs" class="val-display">120</span></label>
            <input type="range" id="fontSize" min="20" max="400" value="120">
        </div>
        <div class="control-item">
            <label>Letter Spacing <span id="v_sp" class="val-display">3</span></label>
            <input type="range" id="spacing" min="-10" max="50" value="3">
        </div>

        <div class="group-title">Animation Effects</div>
        <div class="control-item">
            <label>Shake Pattern</label>
            <select id="shakePattern">
                <option value="random">Random Noise</option>
                <option value="sin">Sine Wave</option>
                <option value="fixed">Fixed Alternating</option>
            </select>
        </div>
        <div class="control-item">
            <label>Shake Intensity <span id="v_sh" class="val-display">2.0</span></label>
            <input type="range" id="shake" min="0" max="50" value="2" step="0.5">
        </div>
        <div class="control-item">
            <label>Neon Glow <span id="v_gl" class="val-display">0.3</span></label>
            <input type="range" id="glow" min="0" max="1.5" value="0.3" step="0.05">
        </div>
        
        <div style="height:100px;"></div>
    </div>

    <div class="main-area">
        <div class="canvas-container">
            <canvas id="mainCanvas"></canvas>
        </div>
    </div>
</div>

<script>
    const cvs = document.getElementById('mainCanvas');
    const ctx = cvs.getContext('2d');
    const WIDTH = 1920;
    const HEIGHT = 1080;
    
    const els = {
        text: document.getElementById('textInput'),
        fs: document.getElementById('fontSize'),
        sp: document.getElementById('spacing'),
        preset: document.getElementById('preset'),
        customC: document.getElementById('customColor'),
        trans: document.getElementById('transparent'),
        shake: document.getElementById('shake'),
        pattern: document.getElementById('shakePattern'),
        glow: document.getElementById('glow'),
        dl: document.getElementById('downloadBtn'),
        customGrp: document.getElementById('custom-color-group')
    };

    const valDisplays = {
        fs: document.getElementById('v_fs'),
        sp: document.getElementById('v_sp'),
        shake: document.getElementById('v_sh'),
        glow: document.getElementById('v_gl')
    };

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
        cvs.width = WIDTH;
        cvs.height = HEIGHT;

        const text = els.text.value;
        const fontSize = parseInt(els.fs.value);
        const spacing = parseInt(els.sp.value);
        const shakeVal = parseFloat(els.shake.value);
        const pattern = els.pattern.value;
        const glowVal = parseFloat(els.glow.value);
        const isTrans = els.trans.checked;
        const preset = els.preset.value;

        if (!isTrans) {
            ctx.fillStyle = "#000000";
            ctx.fillRect(0, 0, WIDTH, HEIGHT);
        } else {
            ctx.clearRect(0, 0, WIDTH, HEIGHT);
        }

        ctx.font = `${fontSize}px 'Shippori Mincho B1'`;
        ctx.textBaseline = 'middle';

        let colors;
        if (preset === 'custom') {
            const c = hexToRgb(els.customC.value);
            colors = [c, c, c];
        } else {
            colors = GRADIENTS[preset].map(hexToRgb);
        }

        const lines = text.split('\\\\n');
        const lineHeight = fontSize * 1.15;
        const totalHeight = lines.length * lineHeight;
        const startY = (HEIGHT - totalHeight) / 2 + lineHeight / 2;
        
        let totalChars = 0;
        lines.forEach(l => totalChars += l.length);
        if (totalChars === 0) totalChars = 1;

        let charCounter = 0;
        ctx.globalCompositeOperation = isTrans ? 'source-over' : 'lighter';

        lines.forEach((line, lineIdx) => {
            let lineWidth = 0;
            for (let char of line) lineWidth += ctx.measureText(char).width + spacing;
            if (line.length > 0) lineWidth -= spacing;
            
            let currentX = (WIDTH - lineWidth) / 2;
            const baseY = startY + (lineIdx * lineHeight);

            for (let char of line) {
                let progress = charCounter / Math.max(totalChars - 1, 1);
                let col = (progress < 0.5) 
                    ? interpolate(colors[0], colors[1], progress * 2)
                    : interpolate(colors[1], colors[2], (progress - 0.5) * 2);
                const colorStr = `rgb(${col.r},${col.g},${col.b})`;

                let yOffset = 0;
                if (shakeVal > 0) {
                    if (pattern === 'fixed') {
                        yOffset = (charCounter % 2 === 0 ? -1 : 1) * shakeVal;
                    } else if (pattern === 'sin') {
                        yOffset = Math.sin(charCounter * 0.8) * shakeVal;
                    } else { 
                        const seed = charCounter * 99.99;
                        const rnd = Math.sin(seed); 
                        const direction = (charCounter % 2 === 0) ? -1 : 1;
                        yOffset = direction * (shakeVal * (0.8 + Math.abs(rnd))); 
                    }
                }

                const passes = [[60, 0.4], [40, 0.5], [20, 0.8], [10, 1.0]];
                passes.forEach(([blur, alphaMul]) => {
                    ctx.shadowBlur = blur;
                    ctx.shadowColor = colorStr;
                    ctx.fillStyle = colorStr;
                    ctx.globalAlpha = alphaMul * glowVal;
                    ctx.fillText(char, currentX, baseY + yOffset);
                });

                ctx.shadowBlur = 0;
                ctx.globalAlpha = 1.0;
                ctx.fillStyle = "#FFFFFF";
                ctx.fillText(char, currentX, baseY + yOffset);

                currentX += ctx.measureText(char).width + spacing;
                charCounter++;
            }
        });
    }

    Object.keys(els).forEach(key => {
        if (!els[key] || key === 'customGrp' || key === 'dl') return;
        els[key].addEventListener('input', (e) => {
            if (valDisplays[key]) valDisplays[key].textContent = e.target.value;
            if (key === 'preset') els.customGrp.style.display = (e.target.value === 'custom') ? 'block' : 'none';
            draw();
        });
    });

    els.dl.addEventListener('click', () => {
        const link = document.createElement('a');
        link.download = 'neon_text.png';
        link.href = cvs.toDataURL('image/png');
        link.click();
    });

    // リサイズ対応
    window.addEventListener('resize', draw);
    
    document.fonts.ready.then(draw);
    setTimeout(draw, 500); 

</script>
</body>
</html>
"""

components.html(html_code, height=2000, scrolling=False)
