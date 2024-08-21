import cv2
import numpy as np
from time import sleep
from datetime import datetime
from threading import Thread
import worker
import os
from time import sleep
from yolov8_test import getModel
#from rov_control import rovAracUart, rovAracSwd

"""
port = "COM8" # aygıt yöneticisinden bağlanılan com port'a göre değiştiriniz
baud = 9600

aruna = rovArac(port, baud)
sleep(3)
print("Sistem baslatildi.")
"""

cam = cv2.VideoCapture("kapitest1.mp4")

cam.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M','J','P','G'))
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

model = getModel("bestkapi.pt", "v10", with_cuda = True)

yatay_bolum = 3
dikey_bolum = 3

son_yon = "R"

yorunge_mod = False
hizalama_mod = False

ilk_egim_alindi = False
egim_kiyaslandi = False
"""
grovUart = rovAracUart(port, baud)
grovUart.adresAl(show = True)
grovSwd = rovAracSwd()

grov = {
    "UART": grovUart,
    "SWD": grovSwd
}

def protocolSet(index):
    global com_prtcl
    print(form.ComPrtcl.itemText(index))
    com_prtcl = form.ComPrtcl.itemText(index)
    if com_prtcl == "UART":
        grovUart.debugModeSet(0)
    elif com_prtcl == "SWD":
        grovUart.debugModeSet(1)
"""
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

while True:

    ret, frame = cam.read()

    if not ret:
        frame = np.zeros((1080, 1408, 3))

    #frame = frame[:, 256:-256, :]

    frame = cv2.resize(frame, (640, 480))

    height, width = frame.shape[:-1]

    sol_bolme = width//yatay_bolum*(yatay_bolum//2)
    sag_bolme = width//yatay_bolum*(yatay_bolum//2+1)

    ust_bolme = height//dikey_bolum*(dikey_bolum//2)
    alt_bolme = height//dikey_bolum*(dikey_bolum//2+1)

    locations = model.getLocations(frame, None, 640)

    """cv2.putText(frame, f"Arkad", (width//2-50, 50), cv2.FONT_HERSHEY_SIMPLEX, 
        1, (0, 255, 0), 2)"""

    sira = 0

    for (x1, y1, x2, y2, t, n) in locations:
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
        cv2.circle(frame, ((x1+x2)//2, (y1+y2)//2), (2), (0, 0, 255), 2)
        """cv2.putText(frame, f"{n} {t}", (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 
            1, (255, 0, 255), 2)"""
        alan = (x2-x1)*(y2-y1)
        egim = round((y2-y1)/(x2-x1), 2)
        oranti = round(alan * egim, 2)
        ekran_yuzde = round(alan / (frame.size//3) * 100, 2)
        if n == "sari_kapi" or n == "kor_nokta":
            """print("Alan:", alan)
            print("Egim:", egim)
            print("Oranti:", oranti)"""
            print("Yukseklik Yuzde:", round((y2-y1) / height * 100, 2), sep="\t")
            print("Ekran Yuzde:\t\t", ekran_yuzde)
            print()
        cv2.putText(frame, f"{oranti}", (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 
            1, (255, 0, 255), 2)
        sira += 1

    #print()

    if not yorunge_mod:

        if len(locations) == 0:

            if son_yon == "L":
                #print("Sol Don")
                cv2.putText(frame, f"Sola Don", (width//2-50, 50), cv2.FONT_HERSHEY_SIMPLEX, 
                    1, (0, 255, 0), 2)
                #pass
                #aruna.solaDon(75)

            elif son_yon == "R":
                #print("Sağ Don")
                cv2.putText(frame, f"Saga Don", (width//2-50, 50), cv2.FONT_HERSHEY_SIMPLEX, 
                    1, (0, 255, 0), 2)
                #pass
                #aruna.sagaDon(75)

        else:

            kapi = locations[0]

            kapi_bulundu = False

            for i in locations:
                    if i[5] == "sari_kapi":
                        kapi = i
                        kapi_bulundu = True
                        break

            for i in locations:
                if i[5] == "kor_nokta":
                    kapi = i
                    kapi_bulundu = True
                    break

            if kapi_bulundu:

                merkez_x = (kapi[0] + kapi[2]) // 2

                #print(merkez)

                if merkez_x < sol_bolme:
                    #aruna.solaDon(50)
                    son_yon = "L"
                    #print("Sol Don")
                    cv2.putText(frame, f"Sola Don", (width//2-50, 50), cv2.FONT_HERSHEY_SIMPLEX, 
                        1, (0, 255, 0), 2)

                elif merkez_x > sag_bolme:
                    #aruna.sagaDon(50)
                    son_yon = "R"
                    #print("Sağ Don")
                    cv2.putText(frame, f"Saga Don", (width//2-50, 50), cv2.FONT_HERSHEY_SIMPLEX, 
                        1, (0, 255, 0), 2)

                else:
                    #aruna.ileriGit(100, 100)
                    #print("İleri")
                    cv2.putText(frame, f"Ileri Git", (width//2-50, 50), cv2.FONT_HERSHEY_SIMPLEX, 
                        1, (0, 255, 0), 2)
                    #pass

                yukseklik_yuzde = round((kapi[3]-kapi[1]) / height * 100, 2)
                ekran_yuzde = round(alan / (frame.size//3) * 100, 2)

                if yukseklik_yuzde >= 60 or ekran_yuzde >= 25:
                    yorunge_mod = True

    else:

        if not hizalama_mod:

            kapi = locations[0]

            kapi_bulundu = False

            for i in locations:
                if i[5] == "sari_kapi":
                    kapi = i
                    kapi_bulundu = True
                    break

            for i in locations:
                if i[5] == "kor_nokta":
                    kapi = i
                    kapi_bulundu = True
                    break

            if kapi_bulundu:

                if not egim_kiyaslandi:

                    if not ilk_egim_alindi:
                    
                        egim_onceki = round((kapi[3]-kapi[2])/(kapi[1]-kapi[0]), 2)

                        #aruna.geriGit(100, 100)
                        sleep(2)
                        #aruna.sagGit(100, 100)
                        sleep(2)
                        #aruna.solaDon(75)
                        sleep(2)

                        #aruna.altMotorlarDurdur()
                        sleep(1.5)

                        ilk_egim_alindi = True

                    else:

                        egim = round((kapi[3]-kapi[2])/(kapi[1]-kapi[0]), 2)

                        if egim > egim_onceki:
                            yorunge_yon = "L"

                        else:
                            yorunge_yon = "R"

                        egim_kiyaslandi = True

                else:

                    egim = round((kapi[3]-kapi[2])/(kapi[1]-kapi[0]), 2)

                    if egim < 1.3:
                        hizalama_mod = True

                    else:

                        #aruna.geriGit(100, 100)
                        sleep(2)

                        if yorunge_yon == "R":
                            #aruna.sagGit(100, 100)
                            sleep(2)
                            #aruna.solaDon(75)
                            sleep(2)

                        elif yorunge_yon == "L":
                            #aruna.solGit(100, 100)
                            sleep(2)
                            #aruna.sagaDon(75)
                            sleep(2)

                        #aruna.altMotorlarDurdur()
                        sleep(1.5)

    #print()
    #print(son_yon)
    #print(kapi)

    cv2.line(frame, (sol_bolme, 0), (sol_bolme, height), (255, 255, 0), 2)
    cv2.line(frame, (sag_bolme, 0), (sag_bolme, height), (255, 255, 0), 2)

    cv2.line(frame, (0, ust_bolme), (width, ust_bolme), (255, 255, 0), 2)
    cv2.line(frame, (0, alt_bolme), (width, alt_bolme), (255, 255, 0), 2)

    #print(height, width)

    cv2.imshow("CAM", frame)

    if cv2.waitKey(1) == ord("q"):
        #aruna.butunMotorlarDurdur()
        break

    #sleep(0.15)

cam.release()
cv2.destroyAllWindows()
