import cv2
import numpy as np

img0 = cv2.imread(r'd:\VALOR\scratch\preview_inspect\frame_000.jpg')
h, w = img0.shape[:2]
# frame 000 is 1280x720
crop0 = img0[h-200:h, w-200:w]
grid0 = crop0.copy()
for x in range(0, 200, 20):
    cv2.line(grid0, (x, 0), (x, 200), (0, 255, 0), 1)
    cv2.putText(grid0, str(x), (x, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 255, 0), 1)
for y in range(0, 200, 20):
    cv2.line(grid0, (0, y), (200, y), (0, 255, 0), 1)
    cv2.putText(grid0, str(y), (5, y), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 255, 0), 1)

cv2.imwrite(r'd:\VALOR\scratch\preview_inspect\grid_crop0.jpg', grid0)
print("Saved grid_crop0.jpg")
