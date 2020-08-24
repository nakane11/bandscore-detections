import cv2
import numpy as np
from matplotlib import pyplot as plt

img_rgb = cv2.imread('lasperanza_page-0005.jpg')
img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
y1 = np.array([])
y2 = np.array([])

template = cv2.imread('a.png',0)
w, h = template.shape[::-1]
res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
threshold = 0.7
loc = np.where( res >= threshold)
y1 = np.insert(y1,len(y1),loc[0])
height = np.array([h]*len(loc[0]))
y2 = np.insert(y2,len(y2),height)


template = cv2.imread('b.png',0)
w, h = template.shape[::-1]
res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
threshold = 0.7
loc = np.where( res >= threshold)
loc = np.where( res >= threshold)
y1 = np.insert(y1,len(y1),loc[0])
height = np.array([h]*len(loc[0]))
y2 = np.insert(y2,len(y2),height)

template = cv2.imread('c.png',0)
w, h = template.shape[::-1]
res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
threshold = 0.7
loc = np.where( res >= threshold)
loc = np.where( res >= threshold)
y1 = np.insert(y1,len(y1),loc[0])
height = np.array([h]*len(loc[0]))
y2 = np.insert(y2,len(y2),height)

tmp = [0, 0]
count = 0
min_ = y2.min()-5
for (i, j) in zip(y1, y2):
    if abs(tmp[0]-i) > min_:
        cv2.rectangle(img_rgb, (10, int(i)), (img_rgb.shape[1]-10, int(i+j)), (0,0,255), 2)
        count += 1
    else : continue
    tmp = [i, j]

print(count)
cv2.imwrite('res.png',img_rgb)