import cv2
import numpy as np

img = cv2.imread(r'd:\VALOR\scratch\preview_inspect\frame_128.jpg')
h, w = img.shape[:2]

# Let's inspect coordinates on 1920x1080:
# In frame 128:
# The star is located around x: 1700..1760, y: 880..945
# Also notice in frame 000 (1280x720):
# The star is in the same relative position (around w*0.9, h*0.85)

mask = np.zeros((h, w), dtype=np.uint8)

# We can find the star by looking at all frames or creating a polygon/circle mask over that specific zone
# Star center on 1920x1080:
cx, cy = 1728, 915
r = 55
cv2.circle(mask, (cx, cy), r, 255, -1)

# Also there might be a second smaller star below/right:
# In frame 000: cx2, cy2 = 1175, 650 on 1280x720 -> scaled to 1920: cx2 ~ 1762, cy2 ~ 975
cv2.circle(mask, (1762, 975), 45, 255, -1)

inpainted = cv2.inpaint(img, mask, inpaintRadius=12, flags=cv2.INPAINT_TELEA)

crop = inpainted[h-250:h, w-300:w]
cv2.imwrite(r'd:\VALOR\scratch\preview_inspect\clean_watermark_128.jpg', crop)
print("Saved clean crop")
