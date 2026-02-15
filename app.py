import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Neon Text Generator", layout="wide")

# HTML/CSS/JS (UI改善版)
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
        height: 100vh;
        overflow: hidden; /* 全体スクロール禁止 */
    }
    
    /* レイアウト: 左サイドバー(設定) + 右メイン(プレビュー) */
    .app-container {
        display: flex;
        height: 100vh;
    }

    /* --- 左側: 設定パネル --- */
    .sidebar {
        width: 320px;
        min-width: 320px;
        background: var(--panel-bg);
        border-right: 1px solid var(--border-color);
        padding: 20px;
        overflow-y: auto; /* 設定が多い場合はスクロール */
        display: flex;
        flex-direction: column;
        gap: 20px;
    }
    
    .group-title {
        font-size: 0.85em;
        font-weight: bold;
        color: #888;
        border-bottom: 1px solid #444;
        padding-bottom: 5px;
        margin-bottom: 10px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .control-item { margin-bottom: 15px; }
    
    label { 
        display: flex; justify-content: space-between;
        font-size: 0.9em; margin-bottom: 6px; color: #ccc; 
    }
    .val-display { color: var(--accent-color); font-weight: bold; }

    input[type="text"], textarea, select {
        width: 100%;
        background: #2b2b2b;
        border: 1px solid #444;
        color: white;
        padding: 8px;
        border-radius: 4px;
        box-sizing: border-box;
        font-size: 14px;
    }
    textarea { resize: vertical; min-height: 80px; }
    
    input[type="range"] {
        width: 100%; cursor: pointer;
    }

    /* --- 右側: プレビューエリア --- */
    .main-area {
        flex: 1;
        display: flex;
        flex-direction: column;
        background: #121212;
        padding: 20px;
        position: relative;
    }
    
    .canvas-wrapper {
        flex: 1;
        background-image: 
            linear-gradient(45deg, #222 25%, transparent 25%), 
            linear-gradient(-45deg, #222 25%, transparent 25%), 
            linear-gradient(45deg, transparent 75%, #222 75%), 
            linear-gradient(-45deg, transparent 75%, #222 75%);
        background-size: 20px 20px;
        background-position: 0 0, 0 10px, 10px -10px, -10px 0px;
        border-radius: 8px;
        border: 1px solid #333;
        display: flex;
        align-items: center;
        justify-content: center;
        overflow: hidden; /* はみ出し防止 */
        box-shadow: inset 0 0 20px #000;
    }

    canvas {
        max-width: 95%;
        max-height: 95%;
        object-fit: contain;
        box-shadow: 0 0 10px rgba(0,0,0,0.5);
    }

    .action-bar {
        padding-top: 20px;
        display: flex;
        justify-content: flex-end;
    }

    button.download-btn {
        background: var(--accent-color);
        color: white;
        border: none;
        padding: 12px 30px;
        border-radius: 6px;
        font-weight: bold;
        cursor: pointer;
        transition: background 0.2s;
        font-size: 1em;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    button.download-btn:hover { background: #5abac6; }

    /* カスタムカラーの表示切り替え */
    #custom-color-group { display: none; margin-top: 10px; }
    input[type="color"] { width: 100%; height: 40px; border: none; padding: 0; cursor: pointer; }

</style>
<link href="https://fonts.googleapis.com/css2?family=Shippori+Mincho+B1:wght@800&display=swap" rel="stylesheet">
</head>
<body>

<div class="app-container">
    <!-- 設定サイドバー -->
    <div class="sidebar">
        
        <!-- グループ1: 基本設定 -->
        <div class="group-title">Text & Font</div>
        
        <div class="control-item">
            <label>テキスト内容</label>
            <textarea id="textInput">サンプル\nテキスト</textarea>
        </div>

        <div class="control-item">
            <label>フォントサイズ <span id="v_fs" class="val-display">100</span></label>
            <input type="range" id="fontSize" min="20" max="400" value="100">
        </div>

        <div class="control-item">
            <label>文字間隔 (Spacing) <span id="v_sp" class="val-display">3</span></label>
            <input type="range" id="spacing" min="-10" max="50" value="3">
        </div>

        <!-- グループ2: 色とスタイル -->
        <div class="group-title">Color & Style</div>

        <div class="control-item">
            <label>カラープリセット</label>
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

        <div class="control-item" style="display:flex; align-items:center; gap:10px;">
            <input type="checkbox" id="transparent" style="width:auto;">
            <label style="margin:0; cursor:pointer;" for="transparent">背景を透過する</label>
        </div>

        <!-- グループ3: エフェクト -->
        <div class="group-title">Effects</div>

        <div class="control-item">
            <label>揺れ幅 (Shake) <span id="v_sh" class="val-display">2.0</span></label>
            <!-- 上限を50に変更 -->
            <input type="range" id="shake" min="0" max="50" value="2" step="0.5">
        </div>

        <div class="control-item">
            <label>発光強度 (Glow) <span id="v_gl" class="val-display">0.3</span></label>
            <input type="range" id="glow" min="0" max="1.5" value="0.3" step="0.05">
        </div>

    </div>

    <!-- メインプレビュー -->
    <div class="main-area">
        <div class="canvas-wrapper">
            <canvas id="mainCanvas"></canvas>
        </div>
        <div class="action-bar">
            <button id="downloadBtn" class="download-btn">画像を保存 (PNG)</button>
        </div>
    </div>
</div>

<script>
    const cvs = document.getElementById('mainCanvas');
    const ctx = cvs.getContext('2d');
    
    // 定数
    const WIDTH = 1920;
    const HEIGHT = 1080;
    
    // 入力要素
    const els = {
        text: document.getElementById('textInput'),
        fs: document.getElementById('fontSize'),
        sp: document.getElementById('spacing'),
        preset: document.getElementById('preset'),
        customC: document.getElementById('customColor'),
        trans: document.getElementById('transparent'),
        shake: document.getElementById('shake'),
        glow: document.getElementById('glow'),
        dl: document.getElementById('downloadBtn'),
        customGrp: document.getElementById('custom-color-group')
    };

    // 数値表示用マップ
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
        // キャンバスサイズ固定
        cvs.width = WIDTH;
        cvs.height = HEIGHT;

        const text = els.text.value;
        const fontSize = parseInt(els.fs.value);
        const spacing = parseInt(els.sp.value);
        const shakeVal = parseFloat(els.shake.value);
        const glowVal = parseFloat(els.glow.value);
        const isTrans = els.trans.checked;
        const preset = els.preset.value;

        // 背景描画
        if (!isTrans) {
            ctx.fillStyle = "#000000";
            ctx.fillRect(0, 0, WIDTH, HEIGHT);
        } else {
            ctx.clearRect(0, 0, WIDTH, HEIGHT);
        }

        ctx.font = `${fontSize}px 'Shippori Mincho B1'`;
        ctx.textBaseline = 'middle';

        // カラー設定
        let colors;
        if (preset === 'custom') {
            const c = hexToRgb(els.customC.value);
            colors = [c, c, c];
        } else {
            colors = GRADIENTS[preset].map(hexToRgb);
        }

        const lines = text.split('\\n');
        const lineHeight = fontSize * 1.15;
        // 垂直中央配置
        const totalHeight = lines.length * lineHeight;
        const startY = (HEIGHT - totalHeight) / 2 + lineHeight / 2;
        
        let totalChars = 0;
        lines.forEach(l => totalChars += l.length);
        if (totalChars === 0) totalChars = 1;

        let charCounter = 0;
        
        // 合成モード設定
        ctx.globalCompositeOperation = isTrans ? 'source-over' : 'lighter';

        // 行ループ
        lines.forEach((line, lineIdx) => {
            // 行幅計算 (中央揃えのため)
            let lineWidth = 0;
            for (let char of line) lineWidth += ctx.measureText(char).width + spacing;
            if (line.length > 0) lineWidth -= spacing;
            
            let currentX = (WIDTH - lineWidth) / 2;
            const baseY = startY + (lineIdx * lineHeight);

            // 文字ループ
            for (let char of line) {
                // グラデーション計算
                let progress = charCounter / Math.max(totalChars - 1, 1);
                let col;
                if (progress < 0.5) {
                    col = interpolate(colors[0], colors[1], progress * 2);
                } else {
                    col = interpolate(colors[1], colors[2], (progress - 0.5) * 2);
                }
                const colorStr = `rgb(${col.r},${col.g},${col.b})`;

                // 揺れ計算 (Random)
                const seed = charCounter * 99.99;
                const rnd = Math.sin(seed); 
                // 揺れ幅が0のときは完全に0にする
                let yOffset = 0;
                if (shakeVal > 0) {
                    const direction = (charCounter % 2 === 0) ? -1 : 1;
                    yOffset = direction * (shakeVal * (0.8 + Math.abs(rnd))); 
                }

                // ■ グロー描画 (重ねがけ)
                // [blur半径, アルファ倍率]
                const passes = [
                    [60, 0.4], [40, 0.5], [20, 0.8], [10, 1.0]
                ];
                
                passes.forEach(([blur, alphaMul]) => {
                    ctx.shadowBlur = blur;
                    ctx.shadowColor = colorStr;
                    ctx.fillStyle = colorStr;
                    ctx.globalAlpha = alphaMul * glowVal;
                    ctx.fillText(char, currentX, baseY + yOffset);
                });

                // ■ 本体描画 (白文字)
                ctx.shadowBlur = 0;
                ctx.globalAlpha = 1.0;
                ctx.fillStyle = "#FFFFFF";
                ctx.fillText(char, currentX, baseY + yOffset);

                // 次の文字へ
                currentX += ctx.measureText(char).width + spacing;
                charCounter++;
            }
        });
    }

    // イベントリスナー設定
    Object.keys(els).forEach(key => {
        if (!els[key] || key === 'customGrp' || key === 'dl') return;
        
        els[key].addEventListener('input', (e) => {
            // 数値更新
            if (valDisplays[key]) valDisplays[key].textContent = e.target.value;
            // カスタムカラー表示制御
            if (key === 'preset') {
                els.customGrp.style.display = (e.target.value === 'custom') ? 'block' : 'none';
            }
            draw();
        });
    });

    els.dl.addEventListener('click', () => {
        const link = document.createElement('a');
        link.download = 'neon_text.png';
        link.href = cvs.toDataURL('image/png');
        link.click();
    });

    // 初期化
    document.fonts.ready.then(draw);
    setTimeout(draw, 500); 

</script>
</body>
</html>
"""

# 全画面表示で埋め込み (スクロールバーが出ないように高さを十分に取る)
components.html(html_code, height=1000, scrolling=False)
