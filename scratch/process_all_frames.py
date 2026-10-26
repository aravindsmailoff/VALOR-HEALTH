import cv2
import numpy as np
import base64
import os
import glob
import re

print("Starting full pipeline to clean watermarks and stabilize faces...")

def clean_watermark(img):
    h, w = img.shape[:2]
    mask = np.zeros((h, w), dtype=np.uint8)
    
    if w <= 1300: # 1280x720
        cv2.circle(mask, (w - 120, h - 120), 34, 255, -1)
        cv2.circle(mask, (w - 85, h - 85), 28, 255, -1)
        cleaned = cv2.inpaint(img, mask, inpaintRadius=8, flags=cv2.INPAINT_TELEA)
    else: # 1920x1080
        scale = w / 1280.0
        cv2.circle(mask, (int(w - 120 * scale), int(h - 120 * scale)), int(36 * scale), 255, -1)
        cv2.circle(mask, (int(w - 85 * scale), int(h - 85 * scale)), int(30 * scale), 255, -1)
        cleaned = cv2.inpaint(img, mask, inpaintRadius=10, flags=cv2.INPAINT_TELEA)
        
    return cleaned

def apply_cinematic_zoom(img, t, max_zoom=0.10, pan_x=0.0, pan_y=0.0):
    h, w = img.shape[:2]
    scale = 1.0 + max_zoom * t
    new_w = w / scale
    new_h = h / scale
    
    center_x = (w / 2.0) + (pan_x * w * t)
    center_y = (h / 2.0) + (pan_y * h * t)
    
    x1 = max(0, int(center_x - new_w / 2.0))
    y1 = max(0, int(center_y - new_h / 2.0))
    x2 = min(w, int(x1 + new_w))
    y2 = min(h, int(y1 + new_h))
    
    if x2 - x1 < int(new_w):
        x1 = max(0, x2 - int(new_w))
    if y2 - y1 < int(new_h):
        y1 = max(0, y2 - int(new_h))
        
    crop = img[y1:y2, x1:x2]
    return cv2.resize(crop, (w, h), interpolation=cv2.INTER_LANCZOS4)

# 1. Load original frames from preview.html
with open(r'd:\VALOR\Folio Insurance_ single hero preview.html', 'r', encoding='utf-8') as f:
    content = f.read()

m = re.search(r'const FR\s*=\s*\[(.*?)\];', content, re.DOTALL)
if not m:
    print("Could not find FR in preview.html")
    exit(1)

raw_items = m.group(1)
items = re.findall(r'"([^"]+)"', raw_items)
print(f"Loaded {len(items)} original frames from preview.html")

# Decode all original frames
orig_imgs = []
for b64_str in items:
    data = base64.b64decode(b64_str)
    nparr = np.frombuffer(data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    orig_imgs.append(img)

# 2. Process frames
new_frames_b64 = []
output_dir = r'd:\VALOR\folio-app\public\frames'
folio_frames_dir = r'd:\VALOR\folio-app\public\folio_frames'
os.makedirs(output_dir, exist_ok=True)
os.makedirs(folio_frames_dir, exist_ok=True)

# Prepare prime calm images for the people scenes
# Pediatric prime: frame 94
pediatric_base = clean_watermark(orig_imgs[94])
# Senior consultation prime: frame 128
senior_base = clean_watermark(orig_imgs[128])
# Skyline peace of mind prime: frame 158
skyline_base = clean_watermark(orig_imgs[158])

TOTAL_COUNT = 160
for i in range(TOTAL_COUNT):
    if i < 80:
        # Desk & Folders: Keep smooth 3D camera move, inpaint watermark
        cleaned = clean_watermark(orig_imgs[i])
    elif 80 <= i < 94:
        # Tablet dashboard push: inpaint watermark
        cleaned = clean_watermark(orig_imgs[i])
    elif 94 <= i < 121:
        # Pediatric scene (27 frames):
        # Cinematic smooth camera glide without mouth movement
        t = (i - 94) / 26.0
        cleaned = apply_cinematic_zoom(pediatric_base, t, max_zoom=0.10, pan_x=0.01, pan_y=0.01)
    elif 121 <= i < 136:
        # Senior consultation scene (15 frames):
        # Cinematic smooth camera glide into tablet without mouth movement
        t = (i - 121) / 14.0
        cleaned = apply_cinematic_zoom(senior_base, t, max_zoom=0.08, pan_x=-0.02, pan_y=0.01)
    else: # 136 <= i < 160
        # Skyline peace of mind (24 frames):
        # Cinematic smooth slow push towards the sunrise city skyline
        t = (i - 136) / 23.0
        cleaned = apply_cinematic_zoom(skyline_base, t, max_zoom=0.12, pan_x=0.0, pan_y=-0.01)

    # Encode to WebP
    # WebP quality 82 for crisp visuals and fast loading
    encode_params = [int(cv2.IMWRITE_WEBP_QUALITY), 82]
    success, enc_img = cv2.imencode('.webp', cleaned, encode_params)
    if not success:
        print(f"Failed to encode frame {i}")
        continue
    
    webp_bytes = enc_img.tobytes()
    b64_output = base64.b64encode(webp_bytes).decode('ascii')
    new_frames_b64.append(b64_output)
    
    # Save to public/frames and public/folio_frames
    filepath = os.path.join(output_dir, f"frame_{i:03d}.webp")
    filepath2 = os.path.join(folio_frames_dir, f"frame_{i:03d}.webp")
    with open(filepath, 'wb') as wf:
        wf.write(webp_bytes)
    with open(filepath2, 'wb') as wf2:
        wf2.write(webp_bytes)
        
    if i % 30 == 0 or i == 159:
        print(f"Processed frame {i:03d} / {TOTAL_COUNT}")

print(f"Successfully generated {len(new_frames_b64)} cleaned, mouth-still, watermark-free frames!")

# 3. Update preview.html
new_fr_code = 'const FR=[' + ','.join([f'"{b}"' for b in new_frames_b64]) + '];'
updated_html = re.sub(r'const FR\s*=\s*\[(.*?)\];', new_fr_code, content, flags=re.DOTALL)

with open(r'd:\VALOR\Folio Insurance_ single hero preview.html', 'w', encoding='utf-8') as f:
    f.write(updated_html)

print("Updated d:\\VALOR\\Folio Insurance_ single hero preview.html with new clean frames!")
