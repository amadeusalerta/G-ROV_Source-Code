from rov_control import rovAracUart, rovAracSwd
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

grovUart.butunMotorlarDurdur()

grovUart.debugModeSet(1) # grovSwd'yi kullanmak için 1 yap

while True:

    try:
        
        """grovUart.ileriGit(100, 100)
        sleep(1)
        grovUart.altMotorlarDurdur()
        sleep(1)"""

        """for i in range(100):
            grovUart.role0Set(1)
            grovUart.role1Set(1)
            grovUart.role2Set(1)
            grovUart.role3Set(1)
            grovUart.role4Set(1)
            sleep(0.005)
            grovUart.role0Set(0)
            grovUart.role1Set(0)
            grovUart.role2Set(0)
            grovUart.role3Set(0)
            grovUart.role4Set(0)
            sleep(0.005)"""

        print(grovUart.onMesGet())
        sleep(0.5)

    except:
        grovUart.butunMotorlarDurdur()
        break
    
