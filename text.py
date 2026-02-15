# -*- coding: utf-8 -*-
import os
import random
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# デフォルト設定
DEFAULT_FONT_PATH = "ShipporiMincho-ExtraBold.ttf" # 同じフォルダに置く
BASE_FONT_SIZE = 60
BG_COLOR = (0, 0, 0)
OFFSET_BASE = 2
WIDTH = 1920
HEIGHT = 1080
LETTER_SPACING = 3

GRADIENT_PRESETS = {
    'default': ["#4896A0", "#714A9D", "#984B93"],
    'fire': ["#FF0000", "#FF6600", "#FFFF00"],
    'ice': ["#0099FF", "#00CCFF", "#FFFFFF"],
}

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def interpolate_color(color1, color2, factor):
    return tuple(int(color1[i] + (color2[i] - color1[i]) * factor) for i in range(3))

def create_master_text_layer(width, height, text_full, font, line_height, gradient_rgb, offset_base, offset_variation, letter_spacing, shake_pattern='random', is_white_overlay=False):
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    lines = text_full.split('\n')
    total_text_height = len(lines) * line_height
    start_y = (height - total_text_height) // 2
    
    # 全文字数をカウント（プログレス計算用）
    total_chars = sum(len(line) for line in lines)
    char_counter = 0
    random.seed(42)

    for line_idx, line_text in enumerate(lines):
        # 行幅計算
        line_width = 0
        for char in line_text:
            try:
                char_bbox = draw.textbbox((0, 0), char, font=font)
                char_w = char_bbox[2] - char_bbox[0]
            except:
                char_w = font.size // 2
            line_width += char_w + letter_spacing
        if len(line_text) > 0:
            line_width -= letter_spacing

        current_x = (width - line_width) // 2
        base_y = start_y + (line_idx * line_height)

        for char in line_text:
            # 色決定
            if is_white_overlay:
                color = (255, 255, 255)
            else:
                progress = char_counter / max(total_chars - 1, 1)
                if progress < 0.5:
                    color = interpolate_color(gradient_rgb[0], gradient_rgb[1], progress * 2)
                else:
                    color = interpolate_color(gradient_rgb[1], gradient_rgb[2], (progress - 0.5) * 2)

            # 揺れ計算
            if shake_pattern == 'fixed':
                direction = -1 if char_counter % 2 == 0 else 1
                y_offset = direction * offset_variation
            elif shake_pattern == 'sin':
                y_offset = int(offset_variation * math.sin(char_counter * 0.8))
            else: # random
                direction = -1 if char_counter % 2 == 0 else 1
                random_scale = random.uniform(0.5, 1.5)
                base = OFFSET_BASE * random_scale
                var = offset_variation * random_scale
                y_offset = int(direction * (base + var))

            y_pos = base_y + y_offset
            draw.text((current_x, y_pos), char, font=font, fill=color + (255,))

            try:
                char_bbox = draw.textbbox((0, 0), char, font=font)
                char_w = char_bbox[2] - char_bbox[0]
            except:
                char_w = font.size // 2
            
            current_x += char_w + letter_spacing
            char_counter += 1
            
    return img

def process_glow(master_arr, blur_radius, brightness, strength, accumulator_rgb, accumulator_alpha):
    temp_img = Image.fromarray(master_arr.astype(np.uint8))
    blurred_img = temp_img.filter(ImageFilter.GaussianBlur(blur_radius))
    blurred_arr = np.array(blurred_img).astype(np.float32)
    glow_rgb = blurred_arr[:, :, :3] * brightness
    accumulator_rgb += glow_rgb * strength
    np.maximum(accumulator_alpha, blurred_arr[:, :, 3], out=accumulator_alpha)

def generate_neon_image(text, gradient_preset='default', custom_color=None, spacing=3, shake=2, glow=0.28, fontsize=0, transparent=False, pattern='random'):
    # フォント設定
    threshold = 15
    decay_rate = 1.0
    
    if fontsize > 0:
        font_size = fontsize
    else:
        lines = text.split('\n')
        max_line_len = max(len(line) for line in lines) if lines else 0
        if max_line_len <= threshold:
            font_size = BASE_FONT_SIZE
        else:
            ratio = threshold / max_line_len
            scale_factor = ratio ** decay_rate
            font_size = max(15, int(BASE_FONT_SIZE * scale_factor))
    
    line_height = int(font_size * 1.15)

    # フォントロード（フォントファイルがない場合はデフォルトを使用）
    try:
        font = ImageFont.truetype(DEFAULT_FONT_PATH, font_size)
    except:
        font = ImageFont.load_default()

    # カラー設定
    if custom_color:
        c = custom_color
        gradient_rgb = [hex_to_rgb(c), hex_to_rgb(c), hex_to_rgb(c)]
    else:
        gradient_colors = GRADIENT_PRESETS.get(gradient_preset, GRADIENT_PRESETS['default'])
        gradient_rgb = [hex_to_rgb(c) for c in gradient_colors]

    # マスターレイヤー作成
    master_img = create_master_text_layer(
        WIDTH, HEIGHT, text, font, line_height, gradient_rgb, OFFSET_BASE, shake, spacing, pattern, is_white_overlay=False
    )

    master_arr = np.array(master_img).astype(np.float32)
    accumulator_rgb = np.zeros((HEIGHT, WIDTH, 3), dtype=np.float32)
    accumulator_alpha = np.zeros((HEIGHT, WIDTH), dtype=np.float32)

    if not transparent:
        accumulator_rgb[:] = BG_COLOR
        accumulator_alpha[:] = 255

    # グロー処理
    for i in range(3):
        process_glow(master_arr, 60 + (i * 20), 0.4 / (i + 1), glow, accumulator_rgb, accumulator_alpha)
    for i in range(5):
        blur = 30 - (i * 5)
        if blur > 0: process_glow(master_arr, blur, 0.8 + (i * 0.1), glow, accumulator_rgb, accumulator_alpha)
    for i in range(3):
        blur = 10 - (i * 3)
        if blur > 0: process_glow(master_arr, blur, 1.2 + (i * 0.15), glow * 0.8, accumulator_rgb, accumulator_alpha)

    # ホワイトオーバーレイ
    white_text_img = create_master_text_layer(
        WIDTH, HEIGHT, text, font, line_height, gradient_rgb, OFFSET_BASE, shake, spacing, pattern, is_white_overlay=True
    )
    white_arr = np.array(white_text_img).astype(np.float32)
    accumulator_rgb += white_arr[:, :, :3]
    np.maximum(accumulator_alpha, white_arr[:, :, 3], out=accumulator_alpha)

    # 合成
    final_rgb = np.clip(accumulator_rgb, 0, 255).astype(np.uint8)
    
    if transparent:
        max_rgb = np.max(accumulator_rgb, axis=2)
        final_alpha = np.maximum(accumulator_alpha, max_rgb)
        final_alpha = np.clip(final_alpha, 0, 255)
        
        # アルファチャンネルの安全な除算
        safe_alpha = final_alpha.copy()
        safe_alpha[safe_alpha == 0] = 1
        safe_alpha_expanded = safe_alpha[:, :, np.newaxis]
        
        final_rgb_t = accumulator_rgb * 255.0 / safe_alpha_expanded
        final_rgb_t = np.clip(final_rgb_t, 0, 255).astype(np.uint8)
        
        final_img = np.dstack((final_rgb_t, final_alpha.astype(np.uint8)))
        return Image.fromarray(final_img, 'RGBA')
    else:
        return Image.fromarray(final_rgb, 'RGB')
