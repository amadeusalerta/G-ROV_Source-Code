import cv2
import numpy as np
from rov_control import rovAracUart, rovAracSwd
#from yolov8_test import getModel
from time import sleep
#from color_correction import simplest_cb

def mapFloat(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

port = "/dev/ttyUSB0"
baud = 115200

grovUart = rovAracUart(port, baud)
"""grovUart.adresAl(show = True)
grovSwd = rovAracSwd()"""

grov = {
    "UART": grovUart
}

#cam = cv2.VideoCapture("mp4/test.mp4")
cam = cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M','J','P','G'))

cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

#model = getModel("./yolov8_test/v10s_50e_halkalar.pt", "v10", with_cuda = True)
#model = getModel("./yolov8_test/yolov10s_999e_cember.pt", "v10", with_cuda = True)

yatay_bolum = 3
dikey_bolum = 3

son_yon = "R"

yorunge_mod = False
hizalama_mod = False

ilk_egim_alindi = False
egim_kiyaslandi = False

grov["UART"].butunMotorlarDurdur()

sira = 0

son_asagi_hiz = 0

on_mesafe = 0
arka_mesafe = 0
sag_mesafe = 0
sol_mesafe = 0
alt_mesafe = 0

suya_girdi = False

print("Suya girmeyi bekliyor...")

mesafeler = {
    "on_mesafe": 0,
    "arka_mesafe": 0,
    "sag_mesafe": 0,
    "sol_mesafe": 0,
    "alt_mesafe": 0
}

"""while not suya_girdi:

    mesafeler["on_mesafe"] = grov["UART"].onMesGet()
    mesafeler["arka_mesafe"] = grov["UART"].arkaMesGet()
    mesafeler["sag_mesafe"] = grov["UART"].sagMesGet()
    mesafeler["sol_mesafe"] = grov["UART"].solMesGet()
    mesafeler["alt_mesafe"] = grov["UART"].asagiMesGet()

    print(mesafeler["on_mesafe"])
    print(mesafeler["arka_mesafe"])
    print(mesafeler["sag_mesafe"])
    print(mesafeler["sol_mesafe"])
    print(mesafeler["alt_mesafe"])

    for i in mesafeler:
        if mesafeler[i] != 0 or mesafeler[i] != -1 or mesafeler[i] != -2 or mesafeler[i] != -3 or mesafeler[i] > 100:
            suya_girdi = True
            break"""

sleep(10)

print("Suya girdi.")

sleep(3)

while True:

    grov["UART"].solaDon(50)
    sleep(3.5)

    grov["UART"].butunMotorlarDurdur()
    sleep(1)

    grov["UART"].ileriGit(100, 100)
    sleep(15)

    grov["UART"].butunMotorlarDurdur()
    sleep(1)

    grov["UART"].asagiGit(250)
    sleep(5)

    grov["UART"].butunMotorlarDurdur()

    for i in range(100):

        grov["UART"].role2Set(1)
        print("Torpido 2 fırlatıldı!!!")
        sleep(0.005)
        grov["UART"].role2Set(0)
        print("Torpido 2 bırakıldı")
        sleep(0.005)

    sleep(1)

    grov["UART"].butunMotorlarDurdur()

    break

"""print("Sistem baslatildi")

for i in range(30):

    grov["UART"].role2Set(1)
    print("Torpido 2 fırlatıldı!!!")
    sleep(0.005)
    grov["UART"].role2Set(0)
    print("Torpido 2 bırakıldı")
    sleep(0.005)

    print(i)"""
    
grov["UART"].butunMotorlarDurdur()

cam.release()
cv2.destroyAllWindows()
