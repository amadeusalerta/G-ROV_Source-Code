import cv2
import numpy as np
from rov_control import rovAracUart, rovAracSwd
from yolov8_test import getModel
from time import sleep
from color_correction import simplest_cb
from threading import Thread

def mapFloat(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

port = "/dev/ttyUSB0"
baud = 115200

grovUart = rovAracUart(port, baud)
grovUart.adresAl(show = True)
grovSwd = rovAracSwd()

grov = {
    "UART": grovUart,
    "SWD": grovSwd
}

grov["UART"].butunMotorlarDurdur()
grov["UART"].debugModeSet(1)

#cam = cv2.VideoCapture("mp4/test.mp4")
cam = cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M','J','P','G'))

cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

#model = getModel("./yolov8_test/v10s_50e_halkalar.pt", "v10", with_cuda = True)
model = getModel("./yolov8_test/yolov10s_999e_cember.pt", "v10", with_cuda = True)

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

def yukseklikAyar():

    while True:

        try:
            alt_mesafe = grov["SWD"].asagiMesGet()

            print(alt_mesafe)

            if alt_mesafe >= 1000:

                asagi_hiz = int(mapFloat(alt_mesafe, 1000, 1650, 0, 250))

                grov["SWD"].asagiGit(asagi_hiz)
                
                #grov["UART"].asagiIn(100, 100)
                """cv2.putText(frame, f"asagi in", (width//2-100, 50), cv2.FONT_HERSHEY_SIMPLEX, 
                            1, (0, 255, 0), 2)"""
                
                son_asagi_hiz = asagi_hiz
                
                pass

            elif alt_mesafe == 0:
                grov["SWD"].asagiGit(son_asagi_hiz//2)
                #grov["UART"].ustMotorlarDurdur()
                pass

            else:
                grov["SWD"].ustMotorlarDurdur()
                pass

        except:
            grov["SWD"].butunMotorlarDurdur()
            break

yukseklik_ayar = Thread(target = yukseklikAyar)
yukseklik_ayar.start()

while True:

    ret, frame = cam.read()

    if not ret:
        frame = np.zeros((1080, 1408, 3))

    frame = frame[:, 256:-256, :]

    frame = cv2.resize(frame, (640, 480))

    #frame = simplest_cb(frame, 1)[0]

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
        alan = (x2-x1)*(y2-y1)
        egim = round((y2-y1)/(x2-x1), 2)
        oranti = round(alan * egim, 2)
        ekran_yuzde = round(alan / (frame.size//3) * 100, 2)
        if n == "kirmizi_cember" or n == "kor_nokta":
            """print("Alan:", alan)
            print("Egim:", egim)
            print("Oranti:", oranti)"""
            #print("Yukseklik Yuzde:", round((y2-y1) / height * 100, 2), sep="\t")
            #print("Ekran Yuzde:\t\t", ekran_yuzde)
            #print()
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

    if True:

        if not yorunge_mod:

            if len(locations) == 0:

                #grov["UART"].ustMotorlarDurdur()

                if son_yon == "L":
                    #print("Sol Don")
                    cv2.putText(frame, f"Sola Don", (width//2-50, 50), cv2.FONT_HERSHEY_SIMPLEX, 
                        1, (0, 255, 0), 2)
                    #pass
                    grov["UART"].solaDon(50)

                elif son_yon == "R":
                    #print("Sağ Don")
                    cv2.putText(frame, f"Saga Don", (width//2-50, 50), cv2.FONT_HERSHEY_SIMPLEX, 
                        1, (0, 255, 0), 2)
                    #pass
                    grov["UART"].sagaDon(50)

            else:

                #grov["UART"].ustMotorlarDurdur()

                if on_mesafe != 0 and on_mesafe < 500:
                    grov["UART"].geriGit(150)
                    #print("Geri")
                    cv2.putText(frame, f"Geri Git", (width//2-50, 50), cv2.FONT_HERSHEY_SIMPLEX, 
                        1, (0, 255, 0), 2)
                    sleep(3)

                else:

                    cember = locations[0]

                    kirmizi_bulundu = False

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

                    kirmizi_bulundu = True

                    if kirmizi_bulundu:

                        merkez_x = (cember[0] + cember[2]) // 2
                        merkez_y = (cember[1] + cember[3]) // 2

                        #print(merkez)

                        if merkez_x < sol_bolme:
                            if merkez_y <= alt_bolme:
                                grov["UART"].solaDon(50)
                            else:
                                grov["UART"].solaDon(75)
                            son_yon = "L"
                            #print("Sol Don")
                            cv2.putText(frame, f"Sola Don", (width//2-50, 50), cv2.FONT_HERSHEY_SIMPLEX, 
                                1, (0, 255, 0), 2)

                        elif merkez_x > sag_bolme:
                            if merkez_y <= alt_bolme:
                                grov["UART"].sagaDon(50)
                            else:
                                grov["UART"].sagaDon(75)
                            son_yon = "R"
                            #print("Sağ Don")
                            cv2.putText(frame, f"Saga Don", (width//2-50, 50), cv2.FONT_HERSHEY_SIMPLEX, 
                                1, (0, 255, 0), 2)

                        else:
                            grov["UART"].ileriGit(100, 100)
                            #print("qq")
                            cv2.putText(frame, f"Ileri Git", (width//2-50, 50), cv2.FONT_HERSHEY_SIMPLEX, 
                                1, (0, 255, 0), 2)
                            #pass

                        """if merkez_y > alt_bolme:
                            grov["UART"].asagiGit(250)"""

                        alan = (cember[2]-cember[0])*(cember[3]-cember[1])

                        yukseklik_yuzde = round((cember[3]-cember[1]) / height * 100, 2)
                        ekran_yuzde = round(alan / (frame.size//3) * 100, 2)

                        print("Yukseklik Yuzde:", round((y2-y1) / height * 100, 2), sep="\t")
                        print("Ekran Yuzde:\t\t", ekran_yuzde)
                        print()

                        if ekran_yuzde >= 19:
                            print("Yorunge moda girildi!!!")
                            yorunge_mod = True

            """if on_mesafe != 0 and on_mesafe < 200:
               #grov["UART"].geriGit(100, 100)
               sleep(3)

            if arka_mesafe != 0 and arka_mesafe < 200:
               #grov["UART"].ileriGit(100, 100)
               sleep(3)

            if sag_mesafe != 0 and sag_mesafe < 200:
               #grov["UART"].solGit(100, 100)
               sleep(3)

            if sol_mesafe != 0 and sol_mesafe < 200:
               #grov["UART"].sagGit(100, 100)
               sleep(3)"""

        else:

            #grov["UART"].ustMotorlarDurdur()

            if not hizalama_mod:

                if len(locations) == 0:
                    pass

                else:

                    cember = locations[0]

                    kirmizi_bulundu = False

                    for i in locations:
                        if i[5] == "kirmizi_cember":
                            cember = i
                            kirmizi_bulundu = True
                            break

                    for i in locations:
                        if i[5] == "kor_nokta":
                            cember = i
                            kirmizi_bulundu = True
                            break

                    if kirmizi_bulundu:

                        if not egim_kiyaslandi:

                            if not ilk_egim_alindi:
                            
                                egim_onceki = round((cember[3]-cember[2])/(cember[1]-cember[0]), 2)

                                grov["UART"].geriGit(100, 100)
                                sleep(1)
                                grov["UART"].sagGit(100, 100)
                                sleep(1)
                                grov["UART"].solaDon(50)
                                sleep(1)

                                grov["UART"].altMotorlarDurdur()
                                sleep(1.5)

                                ilk_egim_alindi = True

                            else:

                                egim = round((cember[3]-cember[1])/(cember[2]-cember[0]), 2)

                                print(egim)

                                if egim > egim_onceki:
                                    yorunge_yon = "L"

                                else:
                                    yorunge_yon = "R"

                                egim_kiyaslandi = True

                        else:

                            egim = round((cember[3]-cember[2])/(cember[1]-cember[0]), 2)

                            print(egim)

                            """if egim < 1.3:
                                hizalama_mod = True"""

                            if True:

                                grov["UART"].geriGit(100, 100)
                                sleep(1)

                                if yorunge_yon == "R":
                                    grov["UART"].sagGit(100, 100)
                                    sleep(1)
                                    grov["UART"].solaDon(50)
                                    sleep(1)

                                elif yorunge_yon == "L":
                                    grov["UART"].solGit(100, 100)
                                    sleep(1)
                                    grov["UART"].sagaDon(50)
                                    sleep(1)

                                grov["UART"].altMotorlarDurdur()
                                sleep(1.5)

            else:

                #grov["UART"].tor0Cntr(1)
                print("Torpido 0 fırlatıldı!!!")
                sleep(0.1)
                #grov["UART"].tor0Cntr(0)
                print("Torpido 0 bırakıldı")
                sleep(0.1)

                #grov["UART"].tor1Cntr(1)
                print("Torpido 1 fırlatıldı!!!")
                sleep(0.1)
                #grov["UART"].tor1Cntr(0)
                print("Torpido 1 bırakıldı")
                sleep(0.1)

                #grov["UART"].tor2Cntr(1)
                print("Torpido 2 fırlatıldı!!!")
                sleep(0.1)
                #grov["UART"].tor2Cntr(0)
                print("Torpido 2 bırakıldı")
                sleep(0.1)

                #grov["UART"].tor3Cntr(1)
                print("Torpido 3 fırlatıldı!!!")
                sleep(0.1)
                #grov["UART"].tor3Cntr(0)
                print("Torpido 3 bırakıldı")
                sleep(0.1)

                #grov["UART"].tor4Cntr(1)
                print("Torpido 4 fırlatıldı!!!")
                sleep(0.1)
                #grov["UART"].tor4Cntr(0)
                print("Torpido 4 bırakıldı")
                sleep(0.1)

                sleep(1)

                grov["UART"].ustMotorlarDurdur()

                grov["UART"].sagaDon(100)
                sleep(0.3)

                """while grov["UART"].onMesGet() < 200:
                    grov["UART"].ileriGit(100, 100)"""

                break

    """if alt_mesafe == 0 or alt_mesafe >= 1200:
        grov["UART"].asagiGit(150)
        pass

    else:
        grov["UART"].ustMotorlarDurdur()
        pass"""

    #sira += 1
    #print(sira)

    #print()
    #print(son_yon)

    #print(cember)

    cv2.line(frame, (sol_bolme, 0), (sol_bolme, height), (255, 255, 0), 2)
    cv2.line(frame, (sag_bolme, 0), (sag_bolme, height), (255, 255, 0), 2)

    cv2.line(frame, (0, ust_bolme), (width, ust_bolme), (255, 255, 0), 2)
    cv2.line(frame, (0, alt_bolme), (width, alt_bolme), (255, 255, 0), 2)

    #print(height, width)

    cv2.imshow("CAM", frame)

    if cv2.waitKey(1) == ord("q"):
        #grov["UART"].butunMotorlarDurdur()
        break

    #sleep(0.15)

grov["UART"].butunMotorlarDurdur()

cam.release()
cv2.destroyAllWindows()
