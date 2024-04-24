import cv2
import numpy as np

class Find_HSV_Range:
    def __init__(self,HSV_image):
        self.HSV_image=HSV_image

    def HSV_Rangef(self):
        Hlist=[]; Slist=[];Vlist=[]
        HSV=cv2.cvtColor(self.HSV_image, cv2.COLOR_BGR2HSV)
        dimensions = HSV.shape
        for y in range((dimensions[1])):
            for x in range((dimensions[0])):
                Hlist.append(HSV[x, y, 0])
                Slist.append(HSV[x, y, 1]) 
                Vlist.append(HSV[x, y, 2])
            
        H_min=min(Hlist);S_min=min(Slist);V_min=min(Vlist)
        H_max=max(Hlist);S_max=max(Slist);V_max=max(Vlist)
        HSV_lower=np.array([H_min,S_min,V_min])
        HSV_upper=np.array([H_max,S_max,V_max])
        return HSV_lower,HSV_upper

image_HSV = cv2.imread('HSVBenk.png')
pappa=Find_HSV_Range(image_HSV)
lower,upper=pappa.HSV_Rangef()
print(lower,upper)
