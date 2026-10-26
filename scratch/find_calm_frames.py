import cv2
import glob
import os

frames = sorted(glob.glob(r'd:\VALOR\folio-app\public\frames\frame_*.webp'))

os.makedirs(r'd:\VALOR\scratch\mouth_inspect', exist_ok=True)

# Scene 1: frames 94 to 110 (pediatric)
for i in [94, 96, 98, 100, 102, 104, 108, 112, 116, 120]:
    if i < len(frames):
        img = cv2.imread(frames[i])
        cv2.imwrite(rf'd:\VALOR\scratch\mouth_inspect\pediatric_{i:03d}.jpg', img)

# Scene 2: frames 121 to 145 (senior consultation)
for i in [121, 123, 125, 128, 130, 133, 136, 140, 145]:
    if i < len(frames):
        img = cv2.imread(frames[i])
        cv2.imwrite(rf'd:\VALOR\scratch\mouth_inspect\senior_{i:03d}.jpg', img)

print("Saved mouth inspect frames")
