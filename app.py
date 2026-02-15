import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Neon Text Generator", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
    header, footer { visibility: hidden; display: none; }
    
    .block-container {
        padding: 0 !important;
        max-width: 100% !important;
    }

    body {
        overflow: hidden !important;
        margin: 0 !important;
    }
    
    .stApp {
        overflow: hidden !important;
    }

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

html_code = """
<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
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
        overflow: hidden; 
    }
    
    .app-container {
        display: flex;
        width: 100%;
        height: 100%;
        flex-direction: row; 
    }

    .sidebar {
        width: 340px;
        min-width: 340px;
        background: var(--panel-bg);
        border-right: 1px solid var(--border-color);
        padding: 20px;
        overflow-y: auto; 
        height: 100%; 
        box-sizing: border-box;
        display: flex; flex-direction: column; gap: 20px;
        z-index: 10;
        scrollbar-width: thin;
        scrollbar-color: #555 #1e1e1e;
    }
    
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

    @media screen and (max-width: 768px) {
        input[type="text"], textarea, select { font-size: 16px; }
    }

    textarea { resize: vertical; min-height: 80px; }
    input[type="range"] { width: 100%; cursor: pointer; margin-top: 5px; }

    .main-area {
        flex: 1;
        display: flex;
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
        padding: 10px;
        box-sizing: border-box;
    }

    canvas {
        max-width: 100%; 
        max-height: 100%; 
        object-fit: contain;
        box-shadow: 0 0 30px rgba(0,0,0,0.8);
        border: 2px dashed #4896A0; 
        box-sizing: border-box;
    }

    #custom-color-group { display: none; margin-top: 10px; }
    input[type="color"] { width: 100%; height: 40px; border: none; padding: 0; cursor: pointer; border-radius: 4px; }

    @media screen and (max-width: 768px) {
        .app-container {
            flex-direction: column-reverse; 
        }

        .sidebar {
            width: 100%;   
            min-width: 0;  
            height: 60%;     
            border-right: none;
            border-top: 1px solid var(--border-color);
            padding: 15px;
            -webkit-overflow-scrolling: touch; 
        }

        .main-area {
            width: 100%;
            height: 40%;    
            flex: none;      
        }    

        h2 { font-size: 1.0em !important; }
        
        .canvas-container { background-size: 16px 16px; }
    }

</style>
<link href="https://fonts.googleapis.com/css2?family=Shippori+Mincho+B1:wght@800&display=swap" rel="stylesheet">
</head>
<body>

<div class="app-container">
    <div class="sidebar">
        <h2 style="margin:0 0 10px 0; font-size:1.2em; color:#fff;">ファンパレ風文字画像作成ツール</h2>
        
        <div class="group-title">Content</div>
        <div class="control-item">
            <label>テキスト</label>
            <textarea id="textInput" spellcheck="false">これがこれからの世界だよ</textarea>
        </div>
        
        <div class="group-title">Style & Color</div>
        <div class="control-item">
            <label>色設定</label>
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
            <label style="margin:0; cursor:pointer; color:#fff;" for="transparent">背景透過</label>
        </div>

        <div class="group-title">Typography</div>
        <div class="control-item">
            <label>フォントサイズ <span id="v_fs" class="val-display">60</span></label>
            <input type="range" id="fontSize" min="10" max="400" value="60">
        </div>
        <div class="control-item">
            <label>文字間隔 <span id="v_sp" class="val-display">3</span></label>
            <input type="range" id="spacing" min="-10" max="50" value="3">
        </div>

        <div class="group-title">Effects</div>
        <div class="control-item">
            <label>揺れ設定</label>
            <select id="shakePattern">
                <option value="random">ランダム</option>
                <option value="fixed">ジグザグ</option>
                <option value="sin">Sine Wave</option>
            </select>
        </div>
        <div class="control-item">
            <label>揺れ強度 <span id="v_sh" class="val-display">2.0</span></label>
            <input type="range" id="shake" min="0" max="100" value="2" step="0.5">
        </div>
        <div class="control-item">
            <label>発光強度 <span id="v_gl" class="val-display">0.8</span></label>
            <input type="range" id="glow" min="0" max="1" value="0.8" step="0.05">
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

        ctx.lineJoin = 'round';
        ctx.lineCap = 'round';

        let palette;
        if (preset === 'custom') {
            const c = els.customC.value;
            palette = [c, c, c];
        } else {
            palette = GRADIENTS[preset];
        }
        
        const lines = text.split('\\\\\\\\n'); 
        
        const lineHeight = fontSize * 1.15;
        const totalHeight = lines.length * lineHeight;
        const startY = (HEIGHT - totalHeight) / 2 + lineHeight / 2;
        
        let charCounter = 0;
        ctx.globalCompositeOperation = isTrans ? 'source-over' : 'lighter';

        lines.forEach((line, lineIdx) => {
            let lineWidth = 0;
            for (let char of line) lineWidth += ctx.measureText(char).width + spacing;
            if (line.length > 0) lineWidth -= spacing;
            
            let currentX = (WIDTH - lineWidth) / 2;
            const baseY = startY + (lineIdx * lineHeight);

            for (let char of line) {
                // 揺れ計算
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

                // 文字ごとの縦方向グラデーションを作成
                // 文字の上端(top)から下端(bottom)にかけてグラデーション
                // 「下からグラデーション」なので、0.0を下側の色、1.0を上側の色とするか、
                // あるいは下(yMax)から上(yMin)へ座標指定する。
                // ここでは Canvasの座標系(上が0)にあわせて、下(baseY + fontSize/2) から 上(baseY - fontSize/2) へ定義。
                const topY = baseY + yOffset - fontSize * 0.55;
                const bottomY = baseY + yOffset + fontSize * 0.55;
                
                // 下から上へのグラデーションを作成
                const grad = ctx.createLinearGradient(0, bottomY, 0, topY);
                
                // パレット色を割り当て (配列の先頭が「下」に来るように0.0に設定)
                if (palette.length === 1) {
                    grad.addColorStop(0, palette[0]);
                    grad.addColorStop(1, palette[0]);
                } else {
                    palette.forEach((color, i) => {
                        grad.addColorStop(i / (palette.length - 1), color);
                    });
                }

                // 発光 (Stroke重ねがけ)
                // shadowBlurは単色制限があるため、ここではStroke自体のグラデーションで発光を表現する
                const passes = [[40, 0.15], [20, 0.2], [10, 0.4]]; // 太さ, 透明度
                
                // 1. 強い発光層 (太いストローク)
                passes.forEach(([width, alpha]) => {
                    ctx.strokeStyle = grad;
                    ctx.lineWidth = width;
                    ctx.globalAlpha = alpha * glowVal;
                    ctx.strokeText(char, currentX, baseY + yOffset);
                });

                // 2. 文字本体 (塗りつぶし)
                // ここもグラデーションで塗ることで「文字色自体がグラデーション」になる
                ctx.fillStyle = grad;
                ctx.globalAlpha = 1.0; 
                
                // 少し白を混ぜて芯を明るく見せるための重ね塗り
                // まずグラデーションで塗る
                ctx.fillText(char, currentX, baseY + yOffset);
                
                // さらに、うっすら白を重ねて「発光体っぽさ」を出す (オプション)
                ctx.fillStyle = "#FFFFFF";
                ctx.globalAlpha = 0.3; // 白の不透明度
                ctx.fillText(char, currentX, baseY + yOffset);

                currentX += ctx.measureText(char).width + spacing;
                charCounter++;
            }
        });
    }

    Object.keys(els).forEach(key => {
        if (!els[key] || key === 'customGrp') return;
        els[key].addEventListener('input', (e) => {
            if (valDisplays[key]) valDisplays[key].textContent = e.target.value;
            if (key === 'preset') els.customGrp.style.display = (e.target.value === 'custom') ? 'block' : 'none';
            draw();
        });
    });

    cvs.addEventListener('click', async () => {
        if (window.innerWidth > 768) return;
        
        cvs.toBlob(async (blob) => {
            if (!blob) return;
            const fileName = 'neon_text.png';
            const file = new File([blob], fileName, { type: 'image/png' });
            
            if (navigator.canShare && navigator.canShare({ files: [file] })) {
                try {
                    await navigator.share({ files: [file], title: 'Neon Text' });
                } catch (err) {}
            } else {
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = fileName;
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
                URL.revokeObjectURL(url);
            }
        }, 'image/png');
    });

    window.addEventListener('resize', draw);
    
    document.fonts.ready.then(draw);
    setTimeout(draw, 500); 

</script>
</body>
</html>
"""

components.html(html_code, height=2000, scrolling=False)
