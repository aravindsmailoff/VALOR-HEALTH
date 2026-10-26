import cv2
import numpy as np

# Load frame_128.jpg (1920x1080)
img = cv2.imread(r'd:\VALOR\scratch\preview_inspect\frame_128.jpg')
h, w = img.shape[:2]

# The watermark is in the bottom-right corner.
# Let's crop the corner to find exact coordinates
crop = img[h-250:h, w-300:w]
cv2.imwrite(r'd:\VALOR\scratch\preview_inspect\watermark_crop_128.jpg', crop)

# Create mask for the watermark
# The watermark consists of light gray/white star shapes
gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
# Threshold bright watermark pixels
_, mask = cv2.threshold(gray, 140, 255, cv2.THRESH_BINARY)
# Dilate slightly to cover edges
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
mask = cv2.dilate(mask, kernel, iterations=2)

cv2.imwrite(r'd:\VALOR\scratch\preview_inspect\watermark_mask_128.jpg', mask)

# Inpaint
inpainted_crop = cv2.inpaint(crop, mask, inpaintRadius=9, flags=cv2.INPAINT_TELEA)
cv2.imwrite(r'd:\VALOR\scratch\preview_inspect\watermark_inpainted_128.jpg', inpainted_crop)

print("Watermark test complete.")
