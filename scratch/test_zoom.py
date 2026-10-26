import cv2
import numpy as np

def apply_cinematic_zoom(img, t, max_zoom=0.10, pan_x=0.0, pan_y=0.0):
    """
    t: float from 0.0 to 1.0
    Smoothly zooms and pans the image.
    """
    h, w = img.shape[:2]
    scale = 1.0 + max_zoom * t
    new_w = w / scale
    new_h = h / scale
    
    # Calculate crop coordinates with subtle pan
    center_x = (w / 2.0) + (pan_x * w * t)
    center_y = (h / 2.0) + (pan_y * h * t)
    
    x1 = max(0, int(center_x - new_w / 2.0))
    y1 = max(0, int(center_y - new_h / 2.0))
    x2 = min(w, int(x1 + new_w))
    y2 = min(h, int(y1 + new_h))
    
    # Adjust in case of boundary overflow
    if x2 - x1 < int(new_w):
        x1 = max(0, x2 - int(new_w))
    if y2 - y1 < int(new_h):
        y1 = max(0, y2 - int(new_h))
        
    crop = img[y1:y2, x1:x2]
    zoomed = cv2.resize(crop, (w, h), interpolation=cv2.INTER_LANCZOS4)
    return zoomed

# Test on clean128
img128 = cv2.imread(r'd:\VALOR\scratch\preview_inspect\clean128.jpg')
z0 = apply_cinematic_zoom(img128, 0.0)
z5 = apply_cinematic_zoom(img128, 0.5, pan_x=-0.02)
z1 = apply_cinematic_zoom(img128, 1.0, pan_x=-0.04)

cv2.imwrite(r'd:\VALOR\scratch\preview_inspect\zoom_0.jpg', z0)
cv2.imwrite(r'd:\VALOR\scratch\preview_inspect\zoom_5.jpg', z5)
cv2.imwrite(r'd:\VALOR\scratch\preview_inspect\zoom_1.jpg', z1)
print("Zoom test generated successfully.")
