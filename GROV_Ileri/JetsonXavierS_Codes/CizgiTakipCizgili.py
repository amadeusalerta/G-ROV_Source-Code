import cv2
import numpy as np
from time import sleep
from datetime import datetime
from threading import Thread
import worker
import os
from time import sleep
from rov_control import rovAracUart, rovAracSwd

#cap = cv2.VideoCapture("take4_lamb.mp4")

cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M','J','P','G'))
"""
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
"""

hsvValues = [78,0,36,114,164,153] #hsv pickerdan value gircen



"""
[57,71,36,112,180,134]
[57,71,36,112,180,134]
[57,71,36,112,180,134]
[57,71,36,112,180,134]
[57,71,36,112,180,134]
[57,71,36,112,180,134]


[86,170,103,179,205,184]
[86,170,103,179,205,184]
[86,170,103,179,205,184]


[78,0,36,114,164,153]
[78,0,36,114,164,153]
[78,0,36,114,164,153]
[78,0,36,114,164,153]
[78,0,36,114,164,153]
[78,0,36,114,164,153]


"""

sensors = 3
threshold = 0.7
width, height = 720, 540

port = "/dev/ttyUSB0"
baud = 115200

grovUart = rovAracUart(port, baud)
grovUart.adresAl(show = True)
grovSwd = rovAracSwd()

grov = {
    "UART": grovUart,
    "SWD": grovSwd
}

senstivity = 3 #ne kadar yüksek deger alirsa o kadar düsük hassasiyet

weights = [-25, -15, 0, 15, 25] #sensOut [0,0,0] ise 0 dönüs acisi, sensOut [1,1,0] ise -15 dönüs acisi, sensOut [1,0,0] ise -25 dönüs acisi, digerleride zitti
curve = 0

com_prtcl = "UART"

motor_hiz = 150
rolicam_aci = 90
rolicam_dim = 0



def protocolSet(index):
    global com_prtcl
    print(form.ComPrtcl.itemText(index))
    com_prtcl = form.ComPrtcl.itemText(index)
    if com_prtcl == "UART":
        grovUart.debugModeSet(0)
    elif com_prtcl == "SWD":
        grovUart.debugModeSet(1)

"""
def ileriGit():
    grov[com_prtcl].ileriGit(motor_hiz, motor_hiz)

def geriGit():
    grov[com_prtcl].geriGit(motor_hiz, motor_hiz)

def sagaDon():
    grov[com_prtcl].sagaDon(motor_hiz)

def solaDon():
    grov[com_prtcl].solaDon(motor_hiz)

def sagaGit():
    grov[com_prtcl].sagGit(motor_hiz, motor_hiz)

def solaGit():
    grov[com_prtcl].solGit(motor_hiz, motor_hiz)

def altMotorlarDurdur():
    grov[com_prtcl].altMotorlarDurdur()

def yukariCik():
    grov[com_prtcl].yukariGit(motor_hiz)

def asagiIn():
   grov[com_prtcl].asagiGit(motor_hiz)

def ustMotorlarDurdur():
    grov[com_prtcl].ustMotorlarDurdur()

def motorHizSet(val):
    global motor_hiz
    form.MotorHizTxt.setText(str(val))
    motor_hiz = val
"""


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
        hh, ww,_ = img.shape
        cx = x + w // 2
        cy = y + h // 2
        tw = ww
        th = hh 
        cv2.circle(img,(cx,cy),10,(0,255,0),cv2.FILLED)
        cv2.line(img, (cx,cy), (tw // 2, th // 2), (0,255,0), 5)
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

def motorKomut(senOut, cx):
    global curve
    lr = (cx - width//2)//senstivity # sagsan sola deger (left and right)
    lr = int(np.clip(lr,-10,10)) #hiz degeri herhal 10 arasinda saniyorum
    if lr < 2 and lr >-2:lr = 0

    if senOut == [1, 0, 0]:
        #curve = weights[0]
        grov[com_prtcl].solaDon(motor_hiz)
        
    elif senOut == [1, 1, 0]:
        #curve = weights[1]
        grov[com_prtcl].solaDon(motor_hiz-10)
        
    elif senOut == [0, 1, 0]:
        #curve = weights[2]
        grov[com_prtcl].ileriGit(motor_hiz, motor_hiz)
        
    elif senOut == [0, 1, 1]:
        #curve = weights[3]
        grov[com_prtcl].sagaDon(motor_hiz-10)
        
    elif senOut == [0, 0, 1]:
        #curve = weights[4]
        grov[com_prtcl].sagaDon(motor_hiz)
    
    elif senOut == [0, 0, 0]:
        #curve = weights[2]
        grov[com_prtcl].butunMotorlarDurdur()
        #grov[com_prtcl].asagiGitSagSol(175, 200)
        
    elif senOut == [1, 1, 1]:
        #curve = weights[2]
        grov[com_prtcl].butunMotorlarDurdur()
        
    elif senOut == [1, 0, 1]:
        #curve = weights[2]
        grov[com_prtcl].butunMotorlarDurdur()
        
        

    #burda escc elre deger yazcaz



while True:
    _, img = cap.read()
    img = cv2.resize(img, (width, height))


    imgThreshold = thresholding(img)
    cx = getContours(imgThreshold,img) #fotoyu dönüstürmek için
    senOut = getSensorOutput(imgThreshold, sensors) #hizalanma sensör outputlari
    motorKomut(senOut, cx)
    cv2.imshow("Output", img)
    cv2.imshow("Path", imgThreshold)
    if cv2.waitKey(1) and 0xFF == ord('q'):
        grov[com_prtcl].butunMotorlarDurdur()
        break

