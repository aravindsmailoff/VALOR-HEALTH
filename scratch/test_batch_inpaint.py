import cv2
import numpy as np
import glob
import os

def clean_watermark(img):
    h, w = img.shape[:2]
    mask = np.zeros((h, w), dtype=np.uint8)
    
    if w <= 1300: # 1280x720
        # Star 1 (larger top-left star)
        cv2.circle(mask, (w - 120, h - 120), 32, 255, -1)
        # Star 2 (smaller bottom-right star)
        cv2.circle(mask, (w - 85, h - 85), 26, 255, -1)
        # Inpaint
        cleaned = cv2.inpaint(img, mask, inpaintRadius=8, flags=cv2.INPAINT_TELEA)
    else: # 1920x1080
        # Star 1
        cv2.circle(mask, (w - 180, h - 180), 48, 255, -1)
        # Star 2
        cv2.circle(mask, (w - 128, h - 128), 38, 255, -1)
        cleaned = cv2.inpaint(img, mask, inpaintRadius=10, flags=cv2.INPAINT_TELEA)
        
    return cleaned

# Test on 000, 080, 094, 128, 158
for idx in [0, 80, 94, 128, 158]:
    p = rf'd:\VALOR\scratch\preview_inspect\pick_{idx:03d}.jpg'
    if os.path.exists(p):
        img = cv2.imread(p)
        cleaned = clean_watermark(img)
        cv2.imwrite(rf'd:\VALOR\scratch\preview_inspect\cleaned_{idx:03d}.jpg', cleaned)

print("Batch inpaint test finished.")
