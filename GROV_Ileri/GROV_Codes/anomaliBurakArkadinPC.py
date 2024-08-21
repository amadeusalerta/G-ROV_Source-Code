import cv2
import numpy as np
#from rov_control import rovAracUart, rovAracSwd
from yolov8_test import getModel
from time import sleep
from find_circle import circles
from color_correction import simplest_cb

port = "/dev/ttyUSB0"
baud = 115200

#grovUart = rovAracUart(port, baud)
#grovUart.adresAl(show = True)
#grovSwd = rovAracSwd()

"""grov = {
    "UART": #grovUart,
    "SWD": #grovSwd
}"""

cam = cv2.VideoCapture("mp4/test.mp4")
#cam = cv2.VideoCapture(0)
#cam.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M','J','P','G'))

cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

model = getModel("pt/best.pt", with_cuda = True)

yatay_bolum = 3
dikey_bolum = 3

son_yon = "R"

yorunge_mod = False
hizalama_mod = False

ilk_egim_alindi = False
egim_kiyaslandi = False

grov["UART"].butunMotorlarDurdur()

HSVLOW = np.array([95, 200, 100])
HSVHIGH = np.array([105, 235, 160])#[99,0,0,106,255,159

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
        cv2.putText(frame, f"{n} {t}", (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 
            1, (255, 0, 255), 2)
        """cv2.putText(frame, f"{oranti}", (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 
            1, (255, 0, 255), 2)"""
        sira += 1

    #print()

    """on_mesafe = grov["UART"].onMesGet()
    arka_mesafe = grov["UART"].arkaMesGet()
    sag_mesafe = grov["UART"].sagMesGet()
    sol_mesafe = grov["UART"].solMesGet()
    alt_mesafe = grov["UART"].asagiMesGet()"""

    on_mesafe = 0
    arka_mesafe = 0
    sag_mesafe = 0
    sol_mesafe = 0
    alt_mesafe = 0

    mask = cv2.inRange(hsv,HSVLOW, HSVHIGH)

    res = cv2.bitwise_and(frame, frame, mask = mask)

    cizgiler = circles(res, [HSVLOW, HSVHIGH], min_radius = 5)

    for (x, y, r) in cizgiler:
        cv2.circle(frame, (x, y), r, (0, 0, 255), 2)
        cv2.circle(frame, (x, y), 2, (0, 255, 0), 2)

    if len(cizgiler) > 0:

        cizgi = cizgiler[0]

        for i in cizgiler:
            if i[0] >= sol_sinir and i[0] <= sag_sinir:
                cizgi = i
                break

        if cizgi[0] < sol_sinir:
            son_yon = "L"
            cv2.putText(frame, f"Sola Don", (250, 50), cv2.FONT_HERSHEY_SIMPLEX, 
                       1, (0, 255, 0), 2)
            #grov["UART"].solaDon(50)

        elif cizgi[0] > sag_sinir:
            son_yon = "R"
            cv2.putText(frame, f"Saga Don", (250, 50), cv2.FONT_HERSHEY_SIMPLEX, 
                       1, (0, 255, 0), 2)
            #grov["UART"].sagaDon(50)

        else:
            cv2.putText(frame, f"Ileri Git", (250, 50), cv2.FONT_HERSHEY_SIMPLEX, 
                       1, (0, 255, 0), 2)
            #grov["UART"].ileriGit(100)

    else:

        if son_yon == "L":
            cv2.putText(frame, f"Sola Don", (250, 50), cv2.FONT_HERSHEY_SIMPLEX, 
                       1, (0, 255, 0), 2)
            #grov["UART"].solaDon(50)

        elif son_yon == "R":
            cv2.putText(frame, f"Saga Don", (250, 50), cv2.FONT_HERSHEY_SIMPLEX, 
                       1, (0, 255, 0), 2)
            #grov["UART"].solaDon(50)

    if len(locations) > 0:
        cv2.imwrite("sekil{sira}.jpg", frame)

    cv2.line(frame, (sol_bolme, 0), (sol_bolme, height), (255, 255, 0), 2)
    cv2.line(frame, (sag_bolme, 0), (sag_bolme, height), (255, 255, 0), 2)

    cv2.line(frame, (0, ust_bolme), (width, ust_bolme), (255, 255, 0), 2)
    cv2.line(frame, (0, alt_bolme), (width, alt_bolme), (255, 255, 0), 2)

    #print(height, width)

    cv2.imshow("CAM", frame)

    if cv2.waitKey(0) == ord("q"):
        #grov["UART"].butunMotorlarDurdur()
        break

    #sleep(0.15)

cam.release()
cv2.destroyAllWindows()
