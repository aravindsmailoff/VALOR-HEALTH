import cv2
import numpy as np

crop = cv2.imread(r'd:\VALOR\scratch\preview_inspect\watermark_crop_128.jpg')
# crop is 250 high x 300 wide
# Let's find the star in this crop:
# In crop coordinates (0..250, 0..300):
# The star is located around x=80..160, y=30..110
print("Crop shape:", crop.shape)

# Let's save a grid with coordinates marked
grid = crop.copy()
for x in range(0, 300, 20):
    cv2.line(grid, (x, 0), (x, 250), (0, 255, 0), 1)
    cv2.putText(grid, str(x), (x, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 255, 0), 1)
for y in range(0, 250, 20):
    cv2.line(grid, (0, y), (300, y), (0, 255, 0), 1)
    cv2.putText(grid, str(y), (5, y), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 255, 0), 1)

cv2.imwrite(r'd:\VALOR\scratch\preview_inspect\grid_crop.jpg', grid)
print("Saved grid_crop.jpg")
