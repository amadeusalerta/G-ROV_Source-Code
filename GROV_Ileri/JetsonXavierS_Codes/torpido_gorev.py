import cv2
import numpy as np
from rov_control import rovAracUart, rovAracSwd
from yolov8_test import getModel
from time import sleep

port = "/dev/ttyUSB0"
baud = 115200

grovUart = rovAracUart(port, baud)
grovUart.adresAl(show = True)
grovSwd = rovAracSwd()

grov = {
    "UART": grovUart,
    "SWD": grovSwd
}

cam = cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M','J','P','G'))

cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

#model = getModel("yolov8_test/v10s_50e_halkalar.pt", "v10", with_cuda = True)
model = getModel("yolov8_test/yolov10s.pt", "v10", with_cuda = True)

yatay_bolum = 3
dikey_bolum = 3

son_yon = "R"

merkez = 0

grov["UART"].butunMotorlarDurdur()

while True:

    ret, frame = cam.read()

    if not ret:
        frame = np.zeros((1080, 1408, 3))

    frame = frame[:, 200:-200, :]

    frame = cv2.resize(frame, (640, 480))

    height, width = frame.shape[:-1]

    sol_bolme = width//yatay_bolum
    sag_bolme = width//yatay_bolum*(yatay_bolum//2+1)

    ust_bolme = height//dikey_bolum
    alt_bolme = height//dikey_bolum*(dikey_bolum//2+1)

    locations = model.getLocations(frame, ["cell phone"], 640)

    print(locations)

    for (x1, y1, x2, y2, t, n) in locations:
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
        cv2.circle(frame, ((x1+x2)//2, (y1+y2)//2), (2), (0, 0, 255), 2)
        cv2.putText(frame, f"{n} {t}", (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 
        1, (255, 0, 255), 2)

    if len(locations) == 0:

        if son_yon == "L":
            pass
            #grov["UART"].solaDon(75)

        elif son_yon == "R":
            pass
            #grov["UART"].sagaDon(75)

    else:

        mesafe = grov["UART"].onMesGet()

        #if False
        if mesafe != 0 or mesafe < 200:
            grov["UART"].geriGit(100, 100)
            sleep(2)

        else:

            cember = locations[-1]

            merkez = (cember[0] + cember[2]) // 2

            #print(merkez)

            if merkez < sol_bolme:
                #grov["UART"].solaDon(50)
                son_yon = "L"

            elif merkez > sag_bolme:
                #grov["UART"].sagaDon(50)
                son_yon = "R"

            else:
                #grov["UART"].ileriGit(100, 100)
                pass

    print()
    print(merkez)
    print(son_yon)

    #print(cember)

    cv2.line(frame, (sol_bolme, 0), (sol_bolme, height), (255, 255, 0), 2)
    cv2.line(frame, (sag_bolme, 0), (sag_bolme, height), (255, 255, 0), 2)

    cv2.line(frame, (0, ust_bolme), (width, ust_bolme), (255, 255, 0), 2)
    cv2.line(frame, (0, alt_bolme), (width, alt_bolme), (255, 255, 0), 2)

    #print(height, width)

    cv2.imshow("CAM", frame)

    if cv2.waitKey(1) == ord("q"):
        grov["UART"].butunMotorlarDurdur()
        break

cam.release()
cv2.destroyAllWindows()
