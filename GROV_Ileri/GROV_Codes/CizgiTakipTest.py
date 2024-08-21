import cv2
import numpy as np

cap = cv2.VideoCapture("test2.mp4")
hsvValues = [44,87,72,94,255,129] #[86,54,113,106,255,167] #hsv pickerdan value gircen
sensors = 3
threshold = 0.1
width, height = 720, 540

senstivity = 3 #ne kadar yüksek deger alirsa o kadar düsük hassasiyet

weights = [-25, -15, 0, 15, 25] #sensOut [0,0,0] ise 0 dönüs acisi, sensOut [1,1,0] ise -15 dönüs acisi, sensOut [1,0,0] ise -25 dönüs acisi, digerleride zitti
curve = 0

def thresholding(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower = np.array([hsvValues[0],hsvValues[1],hsvValues[2]])
    upper = np.array([hsvValues[3],hsvValues[4],hsvValues[5]])
    mask = cv2.inRange(hsv, lower, upper) #sadece beyaz gözüken foto mask olcak
    return mask

def getContours(imgThreshold, img):
    cx = 0
    contours, hieracrhy = cv2.findContours(imgThreshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    if len(contours) != 0:
        biggest = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(biggest)
        cx = x + w // 2
        cy = y + h // 2
        cv2.circle(img,(cx,cy),10,(0,255,0),cv2.FILLED)
        cv2.drawContours(img, biggest,-1, (255,0,255),7)
        #cv2.drawContours(img, contours,-1, (255,0,255),7)
    return cx

def getSensorOutput(imgThreshold, sensors):
    imgs = np.hsplit(imgThreshold, sensors)
    totalPixels = (img.shape[1]//sensors) * img.shape[0]
    senOut = []
    for x,im in enumerate(imgs):
        pixelCount = cv2.countNonZero(im)
        if pixelCount > threshold*totalPixels:
            senOut.append(1)
        else:
            senOut.append(0)
        cv2.imshow(str(x), im)
    print(senOut)
    return senOut
"""
def motorKomut(senOut, cx):
    global curve
    lr = (cx - width//2)//senstivity # sagsan sola deger (left and right)
    lr = int(np.clip(lr,-10,10)) #hiz degeri herhal 10 arasinda saniyorum
    if lr < 2 and lr >-2:lr = 0

    if senOut == [1, 0, 0]: curve = weights[0]
    elif senOut == [1, 1, 0]: curve = weights[1]
    elif senOut == [0, 1, 0]: curve = weights[2]
    elif senOut == [0, 1, 1]: curve = weights[3]
    elif senOut == [0, 0, 1]: curve = weights[4]
    
    elif senOut == [0, 0, 0]: curve = weights[2]
    elif senOut == [1, 1, 1]: curve = weights[2]
    elif senOut == [1, 0, 1]: curve = weights[2]

    #burda escc elre deger yazcaz
"""   
while True:
    _, img = cap.read()
    img = cv2.resize(img, (width, height))


    imgThreshold = thresholding(img)
    cx = getContours(imgThreshold,img) #fotoyu dönüstürmek için
    senOut = getSensorOutput(imgThreshold, sensors) #hizalanma sensör outputlari
    #motorKomut(senOut, cx)
    cv2.imshow("Output", img)
    cv2.imshow("Path", imgThreshold)
    cv2.waitKey(0)
