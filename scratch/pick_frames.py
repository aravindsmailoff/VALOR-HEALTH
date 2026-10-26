import cv2
import glob

frames = sorted(glob.glob(r'd:\VALOR\folio-app\public\frames\frame_*.webp'))

# Let's save frames 94, 98, 102, 110, 115, 120
for idx in [94, 98, 102, 110, 115, 120, 121, 124, 128, 132, 136, 142, 150, 158]:
    if idx < len(frames):
        img = cv2.imread(frames[idx])
        cv2.imwrite(rf'd:\VALOR\scratch\preview_inspect\pick_{idx:03d}.jpg', img)

print("Saved picks for inspection")
