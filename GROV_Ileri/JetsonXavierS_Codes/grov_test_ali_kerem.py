from rov_control import rovAracUart, rovAracSwd
from time import sleep
from threading import Thread

port = "/dev/ttyUSB0"
baud = 115200

grovUart = rovAracUart(port, baud)
grovUart.adresAl(show = True)
grovSwd = rovAracSwd()

grov = {
    "UART": grovUart,
    "SWD": grovSwd,
}

sleep(2)

grov["UART"].butunMotorlarDurdur()
grov["UART"].debugModeSet(0)

print("Sistem baslatildi.")

def yukseklikAyar():

    while True:

        try:
            grov["SWD"].yukariGit(150)
            sleep(1)
            grov["SWD"].ustMotorlarDurdur()
            sleep(1)

        except:
            grov["SWD"].butunMotorlarDurdur()
            break

yukseklik_ayar = Thread(target = yukseklikAyar)
#yukseklik_ayar.start()

grov["UART"].filterResetSet(1)
grov["UART"].filterResetSet(0)

while True:

    print(grov["UART"].asagiMesGet())
    sleep(0.1)

    """try:
        grov["UART"].ileriGit(150, 150)
        sleep(2)
        grov["UART"].altMotorlarDurdur()
        sleep(2)

    except:
        grov["UART"].butunMotorlarDurdur()
        break"""

    
