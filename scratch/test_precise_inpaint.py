import cv2
import numpy as np

def remove_watermark(img):
    h, w = img.shape[:2]
    mask = np.zeros((h, w), dtype=np.uint8)
    
    # Coordinates normalized
    # Star 1 center: (w - int(w * 0.09375), h - int(h * 0.1667))
    # Star 2 center: (w - int(w * 0.0664), h - int(h * 0.1185))
    if w == 1280:
        cv2.circle(mask, (w - 120, h - 120), 32, 255, -1)
        cv2.circle(mask, (w - 85, h - 85), 26, 255, -1)
    else: # 1920x1080 or other
        scale = w / 1280.0
        cv2.circle(mask, (int(w - 120 * scale), int(h - 120 * scale)), int(34 * scale), 255, -1)
        cv2.circle(mask, (int(w - 85 * scale), int(h - 85 * scale)), int(28 * scale), 255, -1)
    
    # Inpaint using Navier-Stokes or Telea
    cleaned = cv2.inpaint(img, mask, inpaintRadius=7, flags=cv2.INPAINT_TELEA)
    return cleaned

img0 = cv2.imread(r'd:\VALOR\scratch\preview_inspect\frame_000.jpg')
clean0 = remove_watermark(img0)
cv2.imwrite(r'd:\VALOR\scratch\preview_inspect\clean0.jpg', clean0)

img128 = cv2.imread(r'd:\VALOR\scratch\preview_inspect\frame_128.jpg')
clean128 = remove_watermark(img128)
cv2.imwrite(r'd:\VALOR\scratch\preview_inspect\clean128.jpg', clean128)

print("Inpainting complete.")
