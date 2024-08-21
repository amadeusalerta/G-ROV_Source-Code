import cv2
import numpy as np
from yolov8_test import getModel
from time import sleep
from rov_control import rovArac
import pygetwindow as gw
import pyautogui as p
import threading

def ekran_goruntusu(ekran_adi):
    w = gw.getWindowsWithTitle(ekran_adi)[0]
    frame = p.screenshot(region=(w.left, w.top, w.width, w.height))
    frame = np.array(frame)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    return frame

def color_correction(frame, intensity=4):
    b, g, r = cv2.split(frame)
    r = cv2.multiply(r, intensity)
    r = np.clip(r, 0, 255).astype(np.uint8)
    corrected_frame = cv2.merge((b, g, r))
    return corrected_frame

def check_distance_and_adjust(aruna):
    while True:
        alt_mesafe = aruna.asagiMesGet()
        if alt_mesafe != 0 and alt_mesafe < 100:
            aruna.yukariGit(200)
            #aruna.sagGit(60, 60)
            print("check ??????????????????????????????")
            #sleep(3)
        """else:
            aruna.asagiGit(100)"""
        sleep(0.1)

port = "COM8" # aygıt yöneticisinden bağlanılan com port'a göre değiştiriniz
baud = 9600

aruna = rovArac(port, baud)
sleep(3)
print("Sistem baslatildi.")

model = getModel("pt/best.pt", with_cuda=True)

yatay_bolum = 3
dikey_bolum = 3

son_yon = "R"

yorunge_mod = False
hizalama_mod = False

ilk_egim_alindi = False
egim_kiyaslandi = False

ekran_adi = "ONVIF_ICAMERA IMA50L35"

alt_mesafe = aruna.asagiMesGet()

aruna.butunMotorlarDurdur()

"""distance_thread = threading.Thread(target=check_distance_and_adjust, args=(aruna,))
distance_thread.daemon = True
distance_thread.start()"""

while True:
    frame = ekran_goruntusu(ekran_adi)

    height, width = frame.shape[:-1]

    sol_bolme = width // yatay_bolum * (yatay_bolum // 2)
    sag_bolme = width // yatay_bolum * (yatay_bolum // 2 + 1)

    ust_bolme = height // dikey_bolum * (dikey_bolum // 2)
    alt_bolme = height // dikey_bolum * (dikey_bolum // 2 + 1)

    locations = model.getLocations(frame, None, 640)

    if locations:
        print(f"Detections: {len(locations)}")

        sira = 0
        for (x1, y1, x2, y2, t, n) in locations:
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
            cv2.circle(frame, ((x1 + x2) // 2, (y1 + y2) // 2), (2), (0, 0, 255), 2)
            alan = (x2 - x1) * (y2 - y1)
            egim = round((y2 - y1) / (x2 - x1), 2)
            oranti = round(alan * egim, 2)
            ekran_yuzde = round(alan / (frame.size // 3) * 100, 2)
            if n == "kirmizi_kapi" or n == "kor_nokta":
                print("Yukseklik Yuzde:", round((y2 - y1) / height * 100, 2), sep="\t")
                print("Ekran Yuzde:\t\t", ekran_yuzde)
                print()
            """cv2.putText(frame, f"{oranti}", (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX,
                        1, (255, 0, 255), 2)"""
            sira += 1

        kapi = locations[0]
        kapi_bulundu = False

        for i in locations:
            if i[5] == "kirmizi_bayrak":
                kapi = i
                kapi_bulundu = True
                print("Kirmizi kapi BULUNDU")
                break
            if i[5] == "kirmizi_kapi":
                kapi = i
                kapi_bulundu = True
                print("Kirmizi kapi BULUNDU")
                break

        if not kapi_bulundu:
            for i in locations:
                if i[5] == "kor_nokta":
                    kapi = i
                    kapi_bulundu = True
                    print("Kor nokta BULUNDU")
                    break

        if ekran_yuzde != 0 and ekran_yuzde < 15:
                print("ASAGI INILIYOR ###########")
                aruna.ileriGit(100, 100)
                #aruna.sagGit(15, 15)
                #aruna.onKaldir(20)
                aruna.asagiGit(150)

        if kapi_bulundu:
            #frame = color_correction(frame)
            merkez_x = (kapi[0] + kapi[2]) // 2

            

            if merkez_x < sol_bolme:
                #aruna.yukariGit(5)
                #aruna.solaDon(50)
                aruna.solGit(75, 75)
                aruna.asagiGit(80)
                aruna.ileriGit(100, 100)
                print("Sola Don")
                son_yon = "L"
                cv2.putText(frame, f"Sola Don", (width // 2 - 50, 50), cv2.FONT_HERSHEY_SIMPLEX,
                            1, (0, 255, 0), 2)

            elif merkez_x > sag_bolme:
                #aruna.yukariGit(5)
                #aruna.sagaDon(50)
                aruna.sagGit(50, 50)
                aruna.asagiGit(25)
                aruna.ileriGit(100, 100)
                print("Saga Don")
                son_yon = "R"
                cv2.putText(frame, f"Saga Don", (width // 2 - 50, 50), cv2.FONT_HERSHEY_SIMPLEX,
                            1, (0, 255, 0), 2)

            elif merkez_x > ust_bolme:
                #aruna.yukariGit(5)
                #aruna.sagaDon(50)
                #aruna.sagGit(50, 50)
                aruna.asagiGit(20)
                aruna.ileriGit(100, 100)
                print("Asagi In")
                #son_yon = "R"
                cv2.putText(frame, f"Asagi In", (width // 2 - 50, 50), cv2.FONT_HERSHEY_SIMPLEX,
                            1, (0, 255, 0), 2)

            elif merkez_x < alt_bolme:
                #aruna.yukariGit(5)
                #aruna.sagaDon(50)
                #aruna.sagGit(50, 50)
                aruna.yukariGit(25)
                aruna.ileriGit(100, 100)
                print("Yukari Cik")
                #son_yon = "R"
                cv2.putText(frame, f"Yukari Cik", (width // 2 - 50, 50), cv2.FONT_HERSHEY_SIMPLEX,
                            1, (0, 255, 0), 2)

            else:
                #aruna.asagiGit(95)
                aruna.ileriGit(100, 100)
                print("Ileri Git")
                cv2.putText(frame, f"Ileri Git", (width // 2 - 50, 50), cv2.FONT_HERSHEY_SIMPLEX,
                            1, (0, 255, 0), 2)
        else:
            print("kapi bulunamadi")
            aruna.ileriGit(240, 240)
            #aruna.yukariGit(25)
            if son_yon == "L":
                #print("Sol Don")
                cv2.putText(frame, f"Sola Don", (width//2-50, 50), cv2.FONT_HERSHEY_SIMPLEX, 
                    1, (0, 255, 0), 2)
                #pass
                aruna.solaDon(10)
                aruna.ileriGit(100, 100)
                #aruna.asagiGit(50)
                #aruna.yukariGit(100)
            elif son_yon == "R":
                #print("Sağ Don")
                cv2.putText(frame, f"Saga Don", (width//2-50, 50), cv2.FONT_HERSHEY_SIMPLEX, 
                1, (0, 255, 0), 2)
                #pass
                aruna.sagaDon(15)
                aruna.ileriGit(100, 100)
                #aruna.asagiGit(50)
                #aruna.yukariGit(100)
            """elif ekran_yuzde >= 7 and ekran_yuzde <= 20:
                print("ASAGI INILIYOR ###########")
                aruna.asagiGit(300)"""
    else:
        print("obje bulunamadi")
        aruna.ileriGit(120, 120)
        #aruna.yukariGit(70)
        if son_yon == "L":
            #print("Sol Don")
            cv2.putText(frame, f"Sola Don", (width//2-50, 50), cv2.FONT_HERSHEY_SIMPLEX, 
                1, (0, 255, 0), 2)
            #pass
            aruna.solaDon(10)
            #aruna.asagiGit(100)
            aruna.ileriGit(100, 100)
            #aruna.yukariGit(100)
        elif son_yon == "R":
            #print("Sağ Don")
            cv2.putText(frame, f"Saga Don", (width//2-50, 50), cv2.FONT_HERSHEY_SIMPLEX, 
            1, (0, 255, 0), 2)
            #pass
            aruna.sagaDon(15)
            #aruna.asagiGit(100)
            aruna.ileriGit(200, 200)
            #aruna.yukariGit(100)
        else:
            aruna.ileriGit(100,100)
        
        """if alt_mesafe != 0  and alt_mesafe < 50:
                aruna.yukariGit(60)
                aruna.sagGit(60, 60)
                print("check")
                cv2.putText(frame, f"Yukari Git", (width//2-100, 50), cv2.FONT_HERSHEY_SIMPLEX, 
                    1, (0, 255, 0), 2)
                sleep(3)
        else:
            aruna.asagiGit(100)"""
        
        
        

        
        

    cv2.line(frame, (sol_bolme, 0), (sol_bolme, height), (255, 255, 0), 2)
    cv2.line(frame, (sag_bolme, 0), (sag_bolme, height), (255, 255, 0), 2)

    cv2.line(frame, (0, ust_bolme), (width, ust_bolme), (255, 255, 0), 2)
    cv2.line(frame, (0, alt_bolme), (width, alt_bolme), (255, 255, 0), 2)

    cv2.imshow("CAM", frame)

    if cv2.waitKey(1) == ord("q"):
        aruna.butunMotorlarDurdur()
        break

cv2.destroyAllWindows()
