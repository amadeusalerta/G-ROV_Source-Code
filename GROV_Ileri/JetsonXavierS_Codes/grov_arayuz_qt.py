from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QGraphicsScene
from PyQt5.QtCore import QTimer, QThread, Qt
from PyQt5.QtGui import QFont, QImage, QPixmap
from time import sleep
from rov_control import rovAracUart, rovAracSwd
import cv2
from threading import Thread
import worker
import os
from datetime import datetime
import numpy as np
from yolov8_test import getModel
from color_correction import simplest_cb

port = "/dev/ttyUSB0"
baud = 115200

#os.system(f"sudo chmod 777 {port}")

grovUart = rovAracUart(port, baud)
grovUart.adresAl(show = True)
#grovSwd = rovAracSwd()

grov = {
    "UART": grovUart,
    "SWD": "grovSwd"
}

Form, Window = uic.loadUiType("tasarim.ui")

app = QApplication([])
window = Window()
form = Form()
form.setupUi(window)
window.show()

"""scene = QGraphicsScene()
form.Camera.setScene(scene)"""

font = QFont('MS Shell Dlg 2', 14)

form.MesOn.setAlignment(Qt.AlignCenter)
form.MesArka.setAlignment(Qt.AlignCenter)
form.MesSag.setAlignment(Qt.AlignCenter)
form.MesSol.setAlignment(Qt.AlignCenter)
form.MesAsagi.setAlignment(Qt.AlignCenter)

form.MesOn.setFont(font)
form.MesArka.setFont(font)
form.MesSag.setFont(font)
form.MesSol.setFont(font)
form.MesAsagi.setFont(font)

form.Roll.setFont(font)
form.Pitch.setFont(font)
form.Yaw.setFont(font)

form.Voltaj.setFont(font)
form.Akim.setFont(font)
form.Watt.setFont(font)

com_prtcl = "UART"

motor_hiz = 250
rolicam_aci = 90
rolicam_dim = 0

frame = None

def constrain(val, min_, max_):
    if val < min_:
        return min_
    elif val > max_:
        return max_
    else:
        return val

camOn = True

def fotoCek():
    if camOn:
        print("Foto Cekildi")
        if frame is not None:
            if not os.path.exists("./photos"):
                os.mkdir("photos")
            now = datetime.now()
            now_str = now.strftime("%d_%m_%Y %H_%M_%S")
            foto_isim = f"{os.getcwd()}/photos/Foto {now_str}.jpg"
            cv2.imwrite(foto_isim, frame)

def protocolSet(index):
    global com_prtcl
    print(form.ComPrtcl.itemText(index))
    com_prtcl = form.ComPrtcl.itemText(index)
    if com_prtcl == "UART":
        grovUart.debugModeSet(0)
    elif com_prtcl == "SWD":
        grovUart.debugModeSet(1)

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

def tor0On():
    grov[com_prtcl].role0Set(1)

def tor0Off():
    grov[com_prtcl].role0Set(0)

def tor1On():
    grov[com_prtcl].role1Set(1)

def tor1Off():
    grov[com_prtcl].role1Set(0)

def tor2On():
    grov[com_prtcl].role2Set(1)

def tor2Off():
    grov[com_prtcl].role2Set(0)

def tor3On():
    grov[com_prtcl].role3Set(1)

def tor3Off():
    grov[com_prtcl].role3Set(0)

def tor4On():
    grov[com_prtcl].role4Set(1)

def tor4Off():
    grov[com_prtcl].role4Set(0)

def rolicamAciSet(val):
    global rolicam_aci
    form.RolicamAngleTxt.setText(str(val))
    grov[com_prtcl].rolicamAngleSet(val)
    rolicam_aci = val

fenerOn = True

def rolicamParlaklikSet(val):
    if fenerOn:
        global rolicam_dim
        grov[com_prtcl].rolicamDimSet(val)
    else:
        grov[com_prtcl].rolicamDimSet(0)
    form.RolicamDimTxt.setText(str(val))
    rolicam_dim = val

def setFener(checked):
    global fenerOn
    fenerOn = bool(checked)
    if not fenerOn:
        grov[com_prtcl].rolicamDimSet(0)
    else:
        grov[com_prtcl].rolicamDimSet(rolicam_dim)
    form.RolicamDim.setEnabled(fenerOn)

def rolicamHizSet(val):
    form.RolicamSpeedTxt.setText(str(val))
    grov[com_prtcl].rolicamSpeedSet(val)

def rolicamResetOn():
    grov[com_prtcl].rolicamResetSet(1)

def rolicamResetOff():
    grov[com_prtcl].rolicamResetSet(0)

def filterResetOn():
    grov[com_prtcl].filterResetSet(1)

def filterResetOff():
    grov[com_prtcl].filterResetSet(0)

keyPressed = False

key_ = 0

basili = False
birakildi = False

cam = cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M','J','P','G'))

cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

def getValues():

    form.MesOn.setText(str(grov[com_prtcl].onMesGet()))
    form.MesArka.setText(str(grov[com_prtcl].arkaMesGet()))
    form.MesSag.setText(str(grov[com_prtcl].sagMesGet()))
    form.MesSol.setText(str(grov[com_prtcl].solMesGet()))
    form.MesAsagi.setText(str(grov[com_prtcl].asagiMesGet()))

    """form.Roll.setText(str(grov[com_prtcl].rollGet()))
    form.Pitch.setText(str(grov[com_prtcl].pitchGet()))
    form.Yaw.setText(str(grov[com_prtcl].yawGet()))

    form.Voltaj.setText(str(grov[com_prtcl].voltajGet()))
    form.Akim.setText(str(grov[com_prtcl].akimGet()))
    form.Watt.setText(str(grov[com_prtcl].wattGet()))"""

def processKeyPress():

    global keyPressed, basili, birakildi, key_, rolicam_aci

    if keyPressed:
        
        if not basili:

            #print("Basildi")

            if key_ < 0x110000:
                key = chr(key_)

            else:
                key = key_

            #print(key)

            if key == "W":
                grov[com_prtcl].ileriGit(motor_hiz, motor_hiz)

            elif key == "S":
                grov[com_prtcl].geriGit(motor_hiz, motor_hiz)

            elif key == "D":
                grov[com_prtcl].sagaDon(motor_hiz)

            elif key == "A":
                grov[com_prtcl].solaDon(motor_hiz)

            elif key == "E":
                grov[com_prtcl].sagGit(motor_hiz, motor_hiz)

            elif key == "Q":
                grov[com_prtcl].solGit(motor_hiz, motor_hiz)

            if key == "O":
                grov[com_prtcl].yukariGit(motor_hiz)

            elif key == "L":
                grov[com_prtcl].asagiGit(motor_hiz)

            if key == "1":
                grov[com_prtcl].role0Set(1)

            if key == "2":
                grov[com_prtcl].role1Set(1)

            if key == "3":
                grov[com_prtcl].role2Set(1)

            if key == "4":
                grov[com_prtcl].role3Set(1)

            if key == "5":
                grov[com_prtcl].role4Set(1)

            if key == "+":
                rolicam_aci += 10
                rolicam_aci = constrain(rolicam_aci, 0, 180)
                form.RolicamAngle.setValue(rolicam_aci)

            if key == "-":
                rolicam_aci -= 10
                rolicam_aci = constrain(rolicam_aci, 0, 180)
                form.RolicamAngle.setValue(rolicam_aci)

            if key == Qt.Key_Enter - 1:
                fotoCek()
            
            birakildi = False
            basili = True

    else:
        
        if not birakildi:

            #print("Birakildi")

            if key_ < 0x110000:
                key = chr(key_)

            else:
                key = key_

            if key == "W" or key == "S" or key == "D" or key == "A" or key == "E" or key == "Q":
                grov[com_prtcl].altMotorlarDurdur()

            if key == "O" or key == "L":
                grov[com_prtcl].ustMotorlarDurdur()

            if key == "1":
                grov[com_prtcl].role0Set(0)

            if key == "2":
                grov[com_prtcl].role1Set(0)

            if key == "3":
                grov[com_prtcl].role2Set(0)

            if key == "4":
                grov[com_prtcl].role3Set(0)

            if key == "5":
                grov[com_prtcl].role4Set(0)

            basili = False
            birakildi = True

    keyPressed = False

def setCam(checked):
    global camOn
    camOn = bool(checked)
    form.FotoCek.setEnabled(camOn)

def getCamera():

    global frame, cam

    cam_acildi = True
    cam_kapandi = False

    #model = getModel("yolov8_test/yolov10s.pt", "v10", with_cuda = True)
    model = getModel("yolov8_test/yolov10s_999e_cember.pt", "v10", with_cuda = True)

    while True:

        if camOn:

            if not cam_acildi:
                #del cam
                print("Kamera aciliyor")
                cam = cv2.VideoCapture(0)
                cam.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M','J','P','G'))
                cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
                cam_kapandi = False
                cam_acildi = True

            ret, frame = cam.read()

            #print(frame)

            if ret:

                #print(frame.shape)

                frame = frame[:, 256:-256, :]

                frame = cv2.resize(frame, (640, 480))

                height, width = frame.shape[:-1]

                #frame = simplest_cb(frame, 1)[0]

                """locations = model.getLocations(frame, None, 640)

                for (x1, y1, x2, y2, t, n) in locations:
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                    cv2.circle(frame, ((x1+x2)//2, (y1+y2)//2), (2), (0, 0, 255), 2)
                    cv2.putText(frame, f"{n} {t}", (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 
                               1, (255, 0, 255), 2)

                if len(locations) > 0:

                    cember = locations[0]

                    for i in locations:
                            if i[5] == "kirmizi_cember":
                                cember = i
                                #kirmizi_bulundu = True
                                break

                    for i in locations:
                        if i[5] == "kor_nokta":
                            cember = i
                            #kirmizi_bulundu = True
                            break

                    alan = (cember[2]-cember[0])*(cember[3]-cember[1])

                    yukseklik_yuzde = round((cember[3]-cember[1]) / height * 100, 2)
                    ekran_yuzde = round(alan / (frame.size//3) * 100, 2)

                    print("Alan:", alan)
                    print("Yukseklik Yuzde:", round((y2-y1) / height * 100, 2), sep="\t")
                    print("Ekran Yuzde:\t\t", ekran_yuzde)
                    print()"""

                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                h, w, ch = frame_rgb.shape
                bytes_per_line = ch * w
                convert_to_Qt_format = QImage(frame_rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)
                p = convert_to_Qt_format.scaled(640, 480, Qt.KeepAspectRatio)

                form.Camera.setPixmap(QPixmap.fromImage(p))

        else:

            if not cam_kapandi:
                print("Kamera kapaniyor")
                cam.release()
                cam_acildi = False
                cam_kapandi = True

            frame_rgb = np.zeros((480, 640, 3), dtype = np.uint8)

            frame_rgb[:,:,:] = 255

            h, w, ch = frame_rgb.shape
            bytes_per_line = ch * w
            convert_to_Qt_format = QImage(frame_rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)
            p = convert_to_Qt_format.scaled(640, 480, Qt.KeepAspectRatio)

            form.Camera.setPixmap(QPixmap.fromImage(p))

thread = QThread()
thread.run = getCamera
thread.start()
"""obj.intReady.connect(getCamera)
obj.moveToThread(thread)"""

timerKeyboard = QTimer()
timerKeyboard.timeout.connect(processKeyPress)
timerKeyboard.start(100)

timerGetData = QTimer()
timerGetData.timeout.connect(getValues)
timerGetData.start(100)

"""timerCamera = QTimer()
timerCamera.timeout.connect(getCamera)
timerCamera.start(1)"""

def keyPressEvent(event):
    global keyPressed, key_
    keyPressed = True
    key_ = event.key()

def keyReleaseEvent(event):
    keyPressed = False

form.CamOn.stateChanged.connect(setCam)

form.FotoCek.clicked.connect(fotoCek)

form.ComPrtcl.currentIndexChanged.connect(protocolSet)

form.IleriGit.pressed.connect(ileriGit)
form.IleriGit.released.connect(altMotorlarDurdur)

form.GeriGit.pressed.connect(geriGit)
form.GeriGit.released.connect(altMotorlarDurdur)

form.SagaDon.pressed.connect(sagaDon)
form.SagaDon.released.connect(altMotorlarDurdur)

form.SolaDon.pressed.connect(solaDon)
form.SolaDon.released.connect(altMotorlarDurdur)

form.SagaGit.pressed.connect(sagaGit)
form.SagaGit.released.connect(altMotorlarDurdur)

form.SolaGit.pressed.connect(solaGit)
form.SolaGit.released.connect(altMotorlarDurdur)

form.YukariCik.pressed.connect(yukariCik)
form.YukariCik.released.connect(ustMotorlarDurdur)

form.AsagiIn.pressed.connect(asagiIn)
form.AsagiIn.released.connect(ustMotorlarDurdur)

form.Tor0.pressed.connect(tor0On)
form.Tor0.released.connect(tor0Off)

form.Tor1.pressed.connect(tor1On)
form.Tor1.released.connect(tor1Off)

form.Tor2.pressed.connect(tor2On)
form.Tor2.released.connect(tor2Off)

form.Tor3.pressed.connect(tor3On)
form.Tor3.released.connect(tor3Off)

form.Tor4.pressed.connect(tor4On)
form.Tor4.released.connect(tor4Off)

form.MotorHiz.valueChanged.connect(motorHizSet)

form.RolicamAngle.valueChanged.connect(rolicamAciSet)

form.FenerOn.stateChanged.connect(setFener)

form.RolicamDim.valueChanged.connect(rolicamParlaklikSet)

form.RolicamSpeed.valueChanged.connect(rolicamHizSet)

form.RolicamReset.pressed.connect(rolicamResetOn)
form.RolicamReset.released.connect(rolicamResetOff)

form.FilterReset.pressed.connect(filterResetOn)
form.FilterReset.released.connect(filterResetOff)

window.keyPressEvent = keyPressEvent
#window.keyReleaseEvent = keyReleaseEvent

app.exec()
