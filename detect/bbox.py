import cv2
import numpy as np

def y_positions(image, threshold):
    img_rgb = np.asarray(image)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    y1 = np.array([])
    y2 = np.array([])

    template = cv2.imread('detect/a.png',0)
    w, h = template.shape[::-1]
    res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
    loc = np.where( res >= threshold)
    y1 = np.insert(y1,len(y1),loc[0])
    height = np.array([h]*len(loc[0]))
    y2 = np.insert(y2,len(y2),height)

    template = cv2.imread('detect/b.png',0)
    w, h = template.shape[::-1]
    res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
    loc = np.where( res >= threshold)
    loc = np.where( res >= threshold)
    y1 = np.insert(y1,len(y1),loc[0])
    height = np.array([h]*len(loc[0]))
    y2 = np.insert(y2,len(y2),height)

    template = cv2.imread('detect/c.png',0)
    w, h = template.shape[::-1]
    res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
    loc = np.where( res >= threshold)
    loc = np.where( res >= threshold)
    y1 = np.insert(y1,len(y1),loc[0])
    height = np.array([h]*len(loc[0]))
    y2 = np.insert(y2,len(y2),height)

    if len(y2) != 0:
        tmp = [0, 0]
        min_ = y2.min()-5
        for (i, j) in zip(y1, y2):
            if abs(tmp[0]-i) > min_:
                yield int(i), int(i+j)
            else : continue
            tmp = [i, j]
    else :
        return None