from serial import Serial
import struct
from time import sleep

URF_VAL_SIRA = 0
ULF_VAL_SIRA = 1
URB_VAL_SIRA = 2
ULB_VAL_SIRA = 3
LRF_VAL_SIRA = 4
LLF_VAL_SIRA = 5
LRB_VAL_SIRA = 6
LLB_VAL_SIRA = 7
ROLE0_VAL_SIRA = 8
ROLE1_VAL_SIRA = 9
ROLE2_VAL_SIRA = 10
FILTER_RESET_SIRA = 11
GYRO_CALIB_SIRA = 12

MES_ON_VAL_SIRA = 128
MES_ASAGI_VAL_SIRA = 129
GYRO_ROLL_VAL_SIRA = 130
GYRO_PITCH_VAL_SIRA = 131
GYRO_YAW_VAL_SIRA = 132
VOLTAJ_VAL_SIRA = 133
AKIM_VAL_SIRA = 134
WATT_VAL_SIRA = 135

ESC_MIN = 1000
ESC_STOP = 1500
ESC_MAX = 2000

karaDegerler = {
    "ust_sag_on_val": ESC_STOP,
    "ust_sol_on_val": ESC_STOP,
    "ust_sag_arka_val": ESC_STOP,
    "ust_sol_arka_val": ESC_STOP,
    "alt_sag_on_val": ESC_STOP,
    "alt_sol_on_val": ESC_STOP,
    "alt_sag_arka_val": ESC_STOP,
    "alt_sol_arka_val": ESC_STOP,
    "role0_val": 0,
    "role1_val": 0,
    "role2_val": 0,
    "filter_reset": 0,
    "gyro_calib": 0
}

suAltiDegerler = {
    "on_mes_val": 0,
    "asagi_mes_val": 0,
    "roll": 0.0,
    "pitch": 0.0,
    "yaw": 0.0,
    "voltaj": 0.0,
    "akim": 0.0,
    "watt": 0.0,
}

def constrain(val, min_, max_):
    if val > max_:
        return max_
    elif val < min_:
        return min_
    else:
        return val
    

class rovArac:

    def __init__(self, port, baud):
        self.ser = Serial(port, baud)

    def kapat(self):
        self.ser.close()

    def sinyalAlindiOku(self):
        #self.ser.read(1)
        pass

    def ustSagOnMotorCntr(self, hiz):
        karaDegerler["ust_sag_on_val"] = constrain(hiz, ESC_MIN, ESC_MAX)
        self.ser.write(URF_VAL_SIRA.to_bytes(1, "little"))
        self.ser.write(karaDegerler["ust_sag_on_val"].to_bytes(2, "little"))
        self.sinyalAlindiOku()

    def ustSolOnMotorCntr(self, hiz):
        karaDegerler["ust_sol_on_val"] = constrain(hiz, ESC_MIN, ESC_MAX)
        self.ser.write(ULF_VAL_SIRA.to_bytes(1, "little"))
        self.ser.write(karaDegerler["ust_sol_on_val"].to_bytes(2, "little"))
        self.sinyalAlindiOku()

    def ustSagArkaMotorCntr(self, hiz):
        karaDegerler["ust_sag_arka_val"] = constrain(hiz, ESC_MIN, ESC_MAX)
        self.ser.write(URB_VAL_SIRA.to_bytes(1, "little"))
        self.ser.write(karaDegerler["ust_sag_arka_val"].to_bytes(2, "little"))
        self.sinyalAlindiOku()

    def ustSolArkaMotorCntr(self, hiz):
        karaDegerler["ust_sol_arka_val"] = constrain(hiz, ESC_MIN, ESC_MAX)
        self.ser.write(ULB_VAL_SIRA.to_bytes(1, "little"))
        self.ser.write(karaDegerler["ust_sol_arka_val"].to_bytes(2, "little"))
        self.sinyalAlindiOku()

    def altSagOnMotorCntr(self, hiz):
        karaDegerler["alt_sag_on_val"] = constrain(hiz, ESC_MIN, ESC_MAX)
        self.ser.write(LRF_VAL_SIRA.to_bytes(1, "little"))
        self.ser.write(karaDegerler["alt_sag_on_val"].to_bytes(2, "little"))
        self.sinyalAlindiOku()

    def altSolOnMotorCntr(self, hiz):
        karaDegerler["alt_sol_on_val"] = constrain(hiz, ESC_MIN, ESC_MAX)
        self.ser.write(LLF_VAL_SIRA.to_bytes(1, "little"))
        self.ser.write(karaDegerler["alt_sol_on_val"].to_bytes(2, "little"))
        self.sinyalAlindiOku()

    def altSagArkaMotorCntr(self, hiz):
        karaDegerler["alt_sag_arka_val"] = constrain(hiz, ESC_MIN, ESC_MAX)
        self.ser.write(LRB_VAL_SIRA.to_bytes(1, "little"))
        self.ser.write((3000 - karaDegerler["alt_sag_arka_val"]).to_bytes(2, "little"))
        self.sinyalAlindiOku()

    def altSolArkaMotorCntr(self, hiz):
        karaDegerler["alt_sol_arka_val"] = constrain(hiz, ESC_MIN, ESC_MAX)
        self.ser.write(LLB_VAL_SIRA.to_bytes(1, "little"))
        self.ser.write((3000 - karaDegerler["alt_sol_arka_val"]).to_bytes(2, "little"))
        self.sinyalAlindiOku()

    def role0Cntrl(self, val):
        karaDegerler["role0_val"] = constrain(val, 0, 1)
        self.ser.write(ROLE0_VAL_SIRA.to_bytes(1, "little"))
        self.ser.write(karaDegerler["role0_val"].to_bytes(1, "little"))
        self.sinyalAlindiOku()

    def role1Cntrl(self, val):
        karaDegerler["role1_val"] = constrain(val, 0, 1)
        self.ser.write(ROLE1_VAL_SIRA.to_bytes(1, "little"))
        self.ser.write(karaDegerler["role1_val"].to_bytes(1, "little"))
        self.sinyalAlindiOku()

    def role2Cntrl(self, val):
        karaDegerler["role2_val"] = constrain(val, 0, 1)
        self.ser.write(ROLE2_VAL_SIRA.to_bytes(1, "little"))
        self.ser.write(karaDegerler["role2_val"].to_bytes(1, "little"))
        self.sinyalAlindiOku()

    def filterResetCntr(self, val):
        karaDegerler["filter_reset"] = constrain(val, 0, 1)
        self.ser.write(FILTER_RESET_SIRA.to_bytes(1, "little"))
        self.ser.write(karaDegerler["filter_reset"].to_bytes(1, "little"))
        self.sinyalAlindiOku()

    def gyroCalibCntr(self, val):
        karaDegerler["gyro_calib"] = constrain(val, 0, 1)
        self.ser.write(GYRO_CALIB_SIRA.to_bytes(1, "little"))
        self.ser.write(karaDegerler["gyro_calib"].to_bytes(1, "little"))
        self.sinyalAlindiOku()

    def altMotorlarDurdur(self):
        self.altSagOnMotorCntr(ESC_STOP)
        self.altSolOnMotorCntr(ESC_STOP)
        self.altSagArkaMotorCntr(ESC_STOP)
        self.altSolArkaMotorCntr(ESC_STOP)

    def ustMotorlarDurdur(self):
        self.ustSagOnMotorCntr(ESC_STOP)
        self.ustSolOnMotorCntr(ESC_STOP)
        self.ustSagArkaMotorCntr(ESC_STOP)
        self.ustSolArkaMotorCntr(ESC_STOP)

    def butunMotorlarDurdur(self):
        self.altMotorlarDurdur()
        self.ustMotorlarDurdur()

    #-----------------------------------------------------------------------

    def ileriGit(self, sol_hiz, sag_hiz):
        self.altSagOnMotorCntr(ESC_STOP + (constrain(sag_hiz, 0, 500)))
        self.altSolOnMotorCntr(ESC_STOP - (constrain(sag_hiz, 0, 500)))
        self.altSagArkaMotorCntr(ESC_STOP + (constrain(sag_hiz, 0, 500)))
        self.altSolArkaMotorCntr(ESC_STOP - (constrain(sag_hiz, 0, 500)))

    def geriGit(self, sol_hiz, sag_hiz):
        self.altSagOnMotorCntr(ESC_STOP - constrain(sag_hiz, 0, 500))
        self.altSolOnMotorCntr(ESC_STOP + constrain(sol_hiz, 0, 500))
        self.altSagArkaMotorCntr(ESC_STOP - constrain(sag_hiz, 0, 500))
        self.altSolArkaMotorCntr(ESC_STOP + constrain(sol_hiz, 0, 500))

    def sagaDon(self, hiz):
        self.altSagOnMotorCntr(ESC_STOP - constrain(hiz, 0, 500))
        self.altSolOnMotorCntr(ESC_STOP - constrain(hiz, 0, 500))
        self.altSagArkaMotorCntr(ESC_STOP - constrain(hiz, 0, 500))
        self.altSolArkaMotorCntr(ESC_STOP - constrain(hiz, 0, 500))

    def solaDon(self, hiz):
        self.altSagOnMotorCntr(ESC_STOP + constrain(hiz, 0, 500))
        self.altSolOnMotorCntr(ESC_STOP + constrain(hiz, 0, 500))
        self.altSagArkaMotorCntr(ESC_STOP + constrain(hiz, 0, 500))
        self.altSolArkaMotorCntr(ESC_STOP + constrain(hiz, 0, 500))

    def sagGit(self, sol_hiz, sag_hiz):
        self.altSagOnMotorCntr(ESC_STOP - constrain(sag_hiz, 0, 500)) #-
        self.altSolOnMotorCntr(ESC_STOP - constrain(sol_hiz, 0, 500))
        self.altSagArkaMotorCntr(ESC_STOP + constrain(sag_hiz, 0, 500))
        self.altSolArkaMotorCntr(ESC_STOP + constrain(sol_hiz, 0, 500))

    def solGit(self, sol_hiz, sag_hiz):
        self.altSagOnMotorCntr(ESC_STOP + constrain(sag_hiz, 0, 500)) #+
        self.altSolOnMotorCntr(ESC_STOP + constrain(sol_hiz, 0, 500))
        self.altSagArkaMotorCntr(ESC_STOP - constrain(sag_hiz, 0, 500))
        self.altSolArkaMotorCntr(ESC_STOP - constrain(sol_hiz, 0, 500))

    def yukariGit(self, hiz):
        self.ustSagOnMotorCntr(ESC_STOP - constrain(hiz, 0, 500))
        self.ustSolOnMotorCntr(ESC_STOP + constrain(hiz, 0, 500))
        self.ustSagArkaMotorCntr(ESC_STOP + constrain(hiz, 0, 500))
        self.ustSolArkaMotorCntr(ESC_STOP + constrain(hiz, 0, 500))
        
    def asagiGit(self, hiz):
        self.ustSagOnMotorCntr(ESC_STOP + constrain(hiz, 0, 500))
        self.ustSolOnMotorCntr(ESC_STOP - constrain(hiz, 0, 500))
        self.ustSagArkaMotorCntr(ESC_STOP - constrain(hiz, 0, 500))
        self.ustSolArkaMotorCntr(ESC_STOP - constrain(hiz, 0, 500))

    def onKaldir(self, hiz):
        self.ustSagOnMotorCntr(ESC_STOP - constrain(hiz, 0, 500))
        self.ustSolOnMotorCntr(ESC_STOP + constrain(hiz, 0, 500))
        self.ustSagArkaMotorCntr(ESC_STOP - constrain(hiz, 0, 500))
        self.ustSolArkaMotorCntr(ESC_STOP - constrain(hiz, 0, 500))

    def arkaKaldir(self, hiz):
        self.ustSagOnMotorCntr(ESC_STOP + constrain(hiz, 0, 500))
        self.ustSolOnMotorCntr(ESC_STOP - constrain(hiz, 0, 500))
        self.ustSagArkaMotorCntr(ESC_STOP + constrain(hiz, 0, 500))
        self.ustSolArkaMotorCntr(ESC_STOP + constrain(hiz, 0, 500))

    def sagKaldir(self, hiz):
        self.ustSagOnMotorCntr(ESC_STOP - constrain(hiz, 0, 500))
        self.ustSolOnMotorCntr(ESC_STOP - constrain(hiz, 0, 500))
        self.ustSagArkaMotorCntr(ESC_STOP + constrain(hiz, 0, 500))
        self.ustSolArkaMotorCntr(ESC_STOP - constrain(hiz, 0, 500))

    def solKaldir(self, hiz):
        self.ustSagOnMotorCntr(ESC_STOP + constrain(hiz, 0, 500))
        self.ustSolOnMotorCntr(ESC_STOP + constrain(hiz, 0, 500))
        self.ustSagArkaMotorCntr(ESC_STOP - constrain(hiz, 0, 500))
        self.ustSolArkaMotorCntr(ESC_STOP + constrain(hiz, 0, 500))

    #---------------------------------------------------

    def onMesGet(self):
        self.ser.write(MES_ON_VAL_SIRA.to_bytes(1, "little"))
        karaDegerler["on_mes_val"] = int.from_bytes(self.ser.read(2), "little", signed = True)
        return karaDegerler["on_mes_val"]

    def asagiMesGet(self):
        self.ser.write(MES_ASAGI_VAL_SIRA.to_bytes(1, "little"))
        karaDegerler["on_asagi_val"] = int.from_bytes(self.ser.read(2), "little", signed = True)
        return karaDegerler["on_asagi_val"]

    def rollGet(self):
        self.ser.write(GYRO_ROLL_VAL_SIRA.to_bytes(1, "little"))
        karaDegerler["roll"] = round(struct.unpack("f", self.ser.read(4))[0], 2)
        return karaDegerler["roll"]

    def pitchGet(self):
        self.ser.write(GYRO_PITCH_VAL_SIRA.to_bytes(1, "little"))
        karaDegerler["pitch"] = round(struct.unpack("f", self.ser.read(4))[0], 2)
        return karaDegerler["pitch"]

    def yawGet(self):
        self.ser.write(GYRO_YAW_VAL_SIRA.to_bytes(1, "little"))
        karaDegerler["yaw"] = round(struct.unpack("f", self.ser.read(4))[0], 2)
        return karaDegerler["yaw"]

    def voltajGet(self):
        self.ser.write(VOLTAJ_VAL_SIRA.to_bytes(1, "little"))
        karaDegerler["voltaj"] = round(struct.unpack("f", self.ser.read(4))[0], 2)
        return karaDegerler["voltaj"]

    def akimGet(self):
        self.ser.write(AKIM_VAL_SIRA.to_bytes(1, "little"))
        karaDegerler["akim"] = round(struct.unpack("f", self.ser.read(4))[0], 2)
        return karaDegerler["akim"]

    def wattGet(self):
        self.ser.write(WATT_VAL_SIRA.to_bytes(1, "little"))
        karaDegerler["watt"] = round(struct.unpack("f", self.ser.read(4))[0], 2)
        return karaDegerler["watt"]
