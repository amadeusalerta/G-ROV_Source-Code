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
    "SWD": grovSwd
}

sleep(2)

grov["UART"].butunMotorlarDurdur()
grov["UART"].debugModeSet(0)

print("Sistem baslatildi.")

calis = True

def ustMotorKontrol():

    global calis

    while calis:

        try:
            grov["UART"].asagiGit(150)
            sleep(1)
            grov["UART"].ustMotorlarDurdur()
            sleep(1)

        except:
            grov["UART"].butunMotorlarDurdur()
            break

    grov["UART"].butunMotorlarDurdur()

ust_motor_cntr = Thread(target = ustMotorKontrol)
#ust_motor_cntr.start()

#print(dir(ust_motor_cntr))

grov["UART"].filterResetSet(1)
grov["UART"].filterResetSet(0)

while True:

    print(grov["UART"].yawGet())
    sleep(0.1)

    try:
        grov["UART"].ileriGit(150, 150)
        sleep(2)
        grov["UART"].altMotorlarDurdur()
        sleep(2)

    except:
        grov["UART"].butunMotorlarDurdur()
        calis = False
        break
