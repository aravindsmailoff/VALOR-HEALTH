import cv2
import glob

# Crop doctor face and patient face in senior consultation
for i in [121, 125, 128, 133, 140]:
    img = cv2.imread(rf'd:\VALOR\scratch\mouth_inspect\senior_{i:03d}.jpg')
    # Doctor face is around x: 500..800, y: 150..450
    doc = img[150:450, 500:800]
    # Senior face is around x: 1200..1550, y: 220..550
    pat = img[220:550, 1200:1550]
    cv2.imwrite(rf'd:\VALOR\scratch\mouth_inspect\senior_doc_{i:03d}.jpg', doc)
    cv2.imwrite(rf'd:\VALOR\scratch\mouth_inspect\senior_pat_{i:03d}.jpg', pat)

print("Face crops saved")
