from serial import Serial
from time import sleep
import os
from swd import Swd
import struct

ESC_MIN = 1000
ESC_STOP = 1500
ESC_MAX = 2000

ADRES_GOSTER_SIRA = 0
DEBUG_ON_SIRA = 1
LRF_VAL_SIRA = 2
LLF_VAL_SIRA = 3
LRB_VAL_SIRA = 4
LLB_VAL_SIRA = 5
U_VAL_SIRA = 6
ROLE0_VAL_SIRA = 7
ROLE1_VAL_SIRA = 8
ROLE2_VAL_SIRA = 9
ROLE3_VAL_SIRA = 10
ROLE4_VAL_SIRA = 11
ROLICAM_ANGLE_SIRA = 12
ROLICAM_SPEED_SIRA = 13
ROLICAM_DIM_SIRA = 14
ROLICAM_RESET_SIRA = 15
FILTER_RESET_SIRA = 16

MES_ON_VAL_SIRA = 128
MES_ARKA_VAL_SIRA = 129
MES_SAG_VAL_SIRA = 130
MES_SOL_VAL_SIRA = 131
MES_ASAGI_VAL_SIRA = 132
GYRO_ROLL_VAL_SIRA = 133
GYRO_PITCH_VAL_SIRA = 134
GYRO_YAW_VAL_SIRA = 135
VOLTAJ_VAL_SIRA = 136
AKIM_VAL_SIRA = 137
WATT_VAL_SIRA = 138

rovDegerlerGelen = {
    "alt_sag_on_val": ESC_STOP,
    "alt_sol_on_val": ESC_STOP,
    "alt_sag_arka_val": ESC_STOP,
    "alt_sol_arka_val": ESC_STOP,
    "ust_val": ESC_STOP,
    "role0_val": 0,
    "role1_val": 0,
    "role2_val": 0,
    "role3_val": 0,
    "role4_val": 0,
    "rolicam_angle": 0,
    "rolicam_speed": 0,
    "rolicam_dim": 0,
    "rolicam_reset": 0,
    "filter_reset": 0
}

rov_degerler_giden = {
  "mes_on": 0,
  "mes_arka": 0,
  "mes_sag": 0,
  "mes_sol": 0,
  "mes_asagi": 0,
  "roll": 0.0,
  "pitch": 0.0,
  "yaw": 0.0,
  "voltaj": 0.0,
  "akim": 0.0,
  "watt": 0.0
}

rovAdresler = {
    "debug_on": 0x00000000,
    "alt_sag_on_val": 0x00000000,
    "alt_sol_on_val": 0x00000000,
    "alt_sag_arka_val": 0x00000000,
    "alt_sol_arka_val": 0x00000000,
    "ust_val": 0x00000000,
    "role0_val": 0x00000000,
    "role1_val": 0x00000000,
    "role2_val": 0x00000000,
    "role3_val": 0x00000000,
    "role4_val": 0x00000000,
    "rolicam_angle": 0x00000000,
    "rolicam_speed": 0x00000000,
    "rolicam_dim": 0x00000000,
    "rolicam_reset": 0x00000000,
    "filter_reset": 0x00000000,
    "mes_on": 0x00000000,
    "mes_arka": 0x00000000,
    "mes_sag": 0x00000000,
    "mes_sol": 0x00000000,
    "mes_asagi": 0x00000000,
    "roll": 0x00000000,
    "pitch": 0x00000000,
    "yaw": 0x00000000,
    "voltaj": 0x00000000,
    "akim": 0x00000000,
    "watt": 0x00000000
}

def constrain(val, min_, max_):
    if val < min_:
        return min_
    elif val > max_:
        return max_
    else:
        return val

class rovAracUart(Serial):

    def __init__(self, port, baud):
        super().__init__(port, baud)

    def adresAl(self, show = False):
        self.write(ADRES_GOSTER_SIRA.to_bytes(1, "little"))
        sleep(0.1)
        for (k, v) in rovAdresler.items():
            deger = self.readline().decode().strip()
            rovAdresler[deger.split()[0]] = int(deger.split()[1])
        if show:
            for (k, v) in rovAdresler.items():
                print(f"{k}:\t{hex(v)}")

    def debugModeSet(self, val):
        rovDegerlerGelen["debug_on"] = constrain(val, 0, 1)
        self.write(DEBUG_ON_SIRA.to_bytes(1, "little"))
        self.write(rovDegerlerGelen["debug_on"].to_bytes(1, "little"))
        self.read(1)

    def altSagOnMotorSet(self, val):
        rovDegerlerGelen["alt_sag_on_val"] = constrain(val, ESC_MIN, ESC_MAX)
        self.write(LRF_VAL_SIRA.to_bytes(1, "little"))
        self.write(rovDegerlerGelen["alt_sag_on_val"].to_bytes(2, "little"))
        self.read(1)

    def altSolOnMotorSet(self, val):
        rovDegerlerGelen["alt_sol_on_val"] = constrain(val, ESC_MIN, ESC_MAX)
        self.write(LLF_VAL_SIRA.to_bytes(1, "little"))
        self.write(rovDegerlerGelen["alt_sol_on_val"].to_bytes(2, "little"))
        self.read(1)

    def altSagArkaMotorSet(self, val):
        rovDegerlerGelen["alt_sag_arka_val"] = constrain(val, ESC_MIN, ESC_MAX)
        self.write(LRB_VAL_SIRA.to_bytes(1, "little"))
        self.write(rovDegerlerGelen["alt_sag_arka_val"].to_bytes(2, "little"))
        self.read(1)

    def altSolArkaMotorSet(self, val):
        rovDegerlerGelen["alt_sol_arka_val"] = constrain(val, ESC_MIN, ESC_MAX)
        self.write(LLB_VAL_SIRA.to_bytes(1, "little"))
        self.write(rovDegerlerGelen["alt_sol_arka_val"].to_bytes(2, "little"))
        self.read(1)

    def ustMotorSet(self, val):
        rovDegerlerGelen["ust_val"] = constrain(val, ESC_MIN, ESC_MAX)
        self.write(U_VAL_SIRA.to_bytes(1, "little"))
        self.write(rovDegerlerGelen["ust_val"].to_bytes(2, "little"))
        self.read(1)

    def role0Set(self, val):
        rovDegerlerGelen["role0_val"] = constrain(val, 0, 1)
        self.write(ROLE0_VAL_SIRA.to_bytes(1, "little"))
        self.write(rovDegerlerGelen["role0_val"].to_bytes(1, "little"))
        self.read(1)

    def role1Set(self, val):
        rovDegerlerGelen["role1_val"] = constrain(val, 0, 1)
        self.write(ROLE1_VAL_SIRA.to_bytes(1, "little"))
        self.write(rovDegerlerGelen["role1_val"].to_bytes(1, "little"))
        self.read(1)

    def role2Set(self, val):
        rovDegerlerGelen["role2_val"] = constrain(val, 0, 1)
        self.write(ROLE2_VAL_SIRA.to_bytes(1, "little"))
        self.write(rovDegerlerGelen["role2_val"].to_bytes(1, "little"))
        self.read(1)

    def role3Set(self, val):
        rovDegerlerGelen["role3_val"] = constrain(val, 0, 1)
        self.write(ROLE3_VAL_SIRA.to_bytes(1, "little"))
        self.write(rovDegerlerGelen["role3_val"].to_bytes(1, "little"))
        self.read(1)

    def role4Set(self, val):
        rovDegerlerGelen["role4_val"] = constrain(val, 0, 1)
        self.write(ROLE4_VAL_SIRA.to_bytes(1, "little"))
        self.write(rovDegerlerGelen["role4_val"].to_bytes(1, "little"))
        self.read(1)

    def rolicamAngleSet(self, val):
        rovDegerlerGelen["rolicam_angle"] = constrain(val, 0, 180)
        self.write(ROLICAM_ANGLE_SIRA.to_bytes(1, "little"))
        self.write(rovDegerlerGelen["rolicam_angle"].to_bytes(1, "little"))
        self.read(1)

    def rolicamSpeedSet(self, val):
        rovDegerlerGelen["rolicam_speed"] = constrain(val, 0, 100)
        self.write(ROLICAM_SPEED_SIRA.to_bytes(1, "little"))
        self.write(rovDegerlerGelen["rolicam_speed"].to_bytes(1, "little"))
        self.read(1)

    def rolicamDimSet(self, val):
        rovDegerlerGelen["rolicam_dim"] = constrain(val, 0, 100)
        self.write(ROLICAM_DIM_SIRA.to_bytes(1, "little"))
        self.write(rovDegerlerGelen["rolicam_dim"].to_bytes(1, "little"))
        self.read(1)

    def rolicamResetSet(self, val):
        rovDegerlerGelen["rolicam_reset"] = constrain(val, 0, 1)
        self.write(ROLICAM_RESET_SIRA.to_bytes(1, "little"))
        self.write(rovDegerlerGelen["rolicam_reset"].to_bytes(1, "little"))
        self.read(1)

    def filterResetSet(self, val):
        rovDegerlerGelen["filter_reset"] = constrain(val, 0, 1)
        self.write(FILTER_RESET_SIRA.to_bytes(1, "little"))
        self.write(rovDegerlerGelen["filter_reset"].to_bytes(1, "little"))
        self.read(1)

    def altMotorlarDurdur(self):
        self.altSagOnMotorSet(ESC_STOP)
        self.altSolOnMotorSet(ESC_STOP)
        self.altSagArkaMotorSet(ESC_STOP)
        self.altSolArkaMotorSet(ESC_STOP)

    def ustMotorlarDurdur(self):
        self.ustMotorSet(ESC_STOP)

    def butunMotorlarDurdur(self):
        self.altMotorlarDurdur()
        self.ustMotorlarDurdur()

    def ileriGit(self, sol_hiz, sag_hiz):
        self.altSagOnMotorSet(ESC_STOP + constrain(sag_hiz, -500, 500))
        self.altSolOnMotorSet(ESC_STOP + constrain(sol_hiz, -500, 500))
        self.altSagArkaMotorSet(ESC_STOP + constrain(sag_hiz, -500, 500))
        self.altSolArkaMotorSet(ESC_STOP + constrain(sol_hiz, -500, 500))

    def geriGit(self, sol_hiz, sag_hiz):
        self.altSagOnMotorSet(ESC_STOP - constrain(sag_hiz, -500, 500))
        self.altSolOnMotorSet(ESC_STOP - constrain(sol_hiz, -500, 500))
        self.altSagArkaMotorSet(ESC_STOP - constrain(sag_hiz, -500, 500))
        self.altSolArkaMotorSet(ESC_STOP - constrain(sol_hiz, -500, 500))

    def sagaDon(self, hiz):
        self.altSagOnMotorSet(ESC_STOP - constrain(hiz, -500, 500))
        self.altSolOnMotorSet(ESC_STOP + constrain(hiz, -500, 500))
        self.altSagArkaMotorSet(ESC_STOP - constrain(hiz, -500, 500))
        self.altSolArkaMotorSet(ESC_STOP + constrain(hiz, -500, 500))

    def solaDon(self, hiz):
        self.altSagOnMotorSet(ESC_STOP + constrain(hiz, -500, 500))
        self.altSolOnMotorSet(ESC_STOP - constrain(hiz, -500, 500))
        self.altSagArkaMotorSet(ESC_STOP + constrain(hiz, -500, 500))
        self.altSolArkaMotorSet(ESC_STOP - constrain(hiz, -500, 500))

    def sagGit(self, on_hiz, arka_hiz):
        self.altSagOnMotorSet(ESC_STOP - constrain(on_hiz, -500, 500))
        self.altSolOnMotorSet(ESC_STOP + constrain(on_hiz, -500, 500))
        self.altSagArkaMotorSet(ESC_STOP + constrain(arka_hiz, -500, 500))
        self.altSolArkaMotorSet(ESC_STOP - constrain(arka_hiz, -500, 500))

    def solGit(self, on_hiz, arka_hiz):
        self.altSagOnMotorSet(ESC_STOP + constrain(on_hiz, -500, 500))
        self.altSolOnMotorSet(ESC_STOP - constrain(on_hiz, -500, 500))
        self.altSagArkaMotorSet(ESC_STOP - constrain(arka_hiz, -500, 500))
        self.altSolArkaMotorSet(ESC_STOP + constrain(arka_hiz, -500, 500))

    def yukariGit(self, hiz):
        self.ustMotorSet(ESC_STOP + constrain(hiz, -500, 500))

    def asagiGit(self, hiz):
        self.ustMotorSet(ESC_STOP - constrain(hiz, -500, 500))

    def onMesGet(self):
        self.write(MES_ON_VAL_SIRA.to_bytes(1, "little"))
        rov_degerler_giden["mes_on"] = int.from_bytes(self.read(2), "little", signed = True)
        return rov_degerler_giden["mes_on"]

    def arkaMesGet(self):
        self.write(MES_ARKA_VAL_SIRA.to_bytes(1, "little"))
        rov_degerler_giden["mes_arka"] = int.from_bytes(self.read(2), "little", signed = True)
        return rov_degerler_giden["mes_arka"]

    def sagMesGet(self):
        self.write(MES_SAG_VAL_SIRA.to_bytes(1, "little"))
        rov_degerler_giden["mes_sag"] = int.from_bytes(self.read(2), "little", signed = True)
        return rov_degerler_giden["mes_sag"]

    def solMesGet(self):
        self.write(MES_SOL_VAL_SIRA.to_bytes(1, "little"))
        rov_degerler_giden["mes_sol"] = int.from_bytes(self.read(2), "little", signed = True)
        return rov_degerler_giden["mes_sol"]

    def asagiMesGet(self):
        self.write(MES_ASAGI_VAL_SIRA.to_bytes(1, "little"))
        rov_degerler_giden["mes_asagi"] = int.from_bytes(self.read(2), "little", signed = True)
        return rov_degerler_giden["mes_asagi"]

    def rollGet(self):
        self.write(GYRO_ROLL_VAL_SIRA.to_bytes(1, "little"))
        rov_degerler_giden["roll"] = round(struct.unpack("f", self.read(4))[0], 2)
        return rov_degerler_giden["roll"]

    def pitchGet(self):
        self.write(GYRO_PITCH_VAL_SIRA.to_bytes(1, "little"))
        rov_degerler_giden["pitch"] = round(struct.unpack("f", self.read(4))[0], 2)
        return rov_degerler_giden["pitch"]

    def yawGet(self):
        self.write(GYRO_YAW_VAL_SIRA.to_bytes(1, "little"))
        rov_degerler_giden["yaw"] = round(struct.unpack("f", self.read(4))[0], 2)
        return rov_degerler_giden["yaw"]

    def voltajGet(self):
        self.write(VOLTAJ_VAL_SIRA.to_bytes(1, "little"))
        rov_degerler_giden["voltaj"] = round(struct.unpack("f", self.read(4))[0], 2)
        return rov_degerler_giden["voltaj"]

    def akimGet(self):
        self.write(AKIM_VAL_SIRA.to_bytes(1, "little"))
        rov_degerler_giden["akim"] = round(struct.unpack("f", self.read(4))[0], 2)
        return rov_degerler_giden["akim"]

    def wattGet(self):
        self.write(WATT_VAL_SIRA.to_bytes(1, "little"))
        rov_degerler_giden["watt"] = round(struct.unpack("f", self.read(4))[0], 2)
        return rov_degerler_giden["watt"]

class rovAracSwd(Swd):

    def __init__(self):
        #self = Swd()
        super().__init__()
        os.system("st-flash reset")
        #print(dir(self))

    def debugOn(self):
        self.write_mem(rovAdresler["debug_on"], b"\x01")

    def debugOff(self):
        self.write_mem(rovAdresler["debug_on"], b"\x00")

    def altSagOnMotorSet(self, val):
        rovDegerlerGelen["alt_sag_on_val"] = constrain(val, ESC_MIN, ESC_MAX)
        self.write_mem(rovAdresler["alt_sag_on_val"], rovDegerlerGelen["alt_sag_on_val"].to_bytes(2, "little"))

    def altSolOnMotorSet(self, val):
        rovDegerlerGelen["alt_sol_on_val"] = constrain(val, ESC_MIN, ESC_MAX)
        self.write_mem(rovAdresler["alt_sol_on_val"], rovDegerlerGelen["alt_sol_on_val"].to_bytes(2, "little"))

    def altSagArkaMotorSet(self, val):
        rovDegerlerGelen["alt_sag_arka_val"] = constrain(val, ESC_MIN, ESC_MAX)
        self.write_mem(rovAdresler["alt_sag_arka_val"], rovDegerlerGelen["alt_sag_arka_val"].to_bytes(2, "little"))

    def altSolArkaMotorSet(self, val):
        rovDegerlerGelen["alt_sol_arka_val"] = constrain(val, ESC_MIN, ESC_MAX)
        self.write_mem(rovAdresler["alt_sol_arka_val"], rovDegerlerGelen["alt_sol_arka_val"].to_bytes(2, "little"))

    def ustMotorSet(self, val):
        rovDegerlerGelen["ust_val"] = constrain(val, ESC_MIN, ESC_MAX)
        self.write_mem(rovAdresler["ust_val"], rovDegerlerGelen["ust_val"].to_bytes(2, "little"))

    def role0Set(self, val):
        rovDegerlerGelen["role0_val"] = constrain(val, 0, 1)
        self.write_mem(rovAdresler["role0_val"], rovDegerlerGelen["role0_val"].to_bytes(1, "little"))

    def role1Set(self, val):
        rovDegerlerGelen["role1_val"] = constrain(val, 0, 1)
        self.write_mem(rovAdresler["role1_val"], rovDegerlerGelen["role1_val"].to_bytes(1, "little"))

    def role2Set(self, val):
        rovDegerlerGelen["role2_val"] = constrain(val, 0, 1)
        self.write_mem(rovAdresler["role2_val"], rovDegerlerGelen["role2_val"].to_bytes(1, "little"))

    def role3Set(self, val):
        rovDegerlerGelen["role3_val"] = constrain(val, 0, 1)
        self.write_mem(rovAdresler["role3_val"], rovDegerlerGelen["role3_val"].to_bytes(1, "little"))

    def role4Set(self, val):
        rovDegerlerGelen["role4_val"] = constrain(val, 0, 1)
        self.write_mem(rovAdresler["role4_val"], rovDegerlerGelen["role4_val"].to_bytes(1, "little"))

    def rolicamAngleSet(self, val):
        rovDegerlerGelen["rolicam_angle"] = constrain(val, 0, 180)
        self.write_mem(rovAdresler["rolicam_angle"], rovDegerlerGelen["rolicam_angle"].to_bytes(1, "little"))

    def rolicamSpeedSet(self, val):
        rovDegerlerGelen["rolicam_speed"] = constrain(val, 0, 180)
        self.write_mem(rovAdresler["rolicam_speed"], rovDegerlerGelen["rolicam_speed"].to_bytes(1, "little"))

    def rolicamDimSet(self, val):
        rovDegerlerGelen["rolicam_dim"] = constrain(val, 0, 100)
        self.write_mem(rovAdresler["rolicam_dim"], rovDegerlerGelen["rolicam_dim"].to_bytes(1, "little"))

    def rolicamResetSet(self, val):
        rovDegerlerGelen["rolicam_reset"] = constrain(val, 0, 1)
        self.write_mem(rovAdresler["rolicam_reset"], rovDegerlerGelen["rolicam_reset"].to_bytes(1, "little"))

    def filterResetSet(self, val):
        rovDegerlerGelen["filter_reset"] = constrain(val, 0, 1)
        self.write_mem(rovAdresler["filter_reset"], rovDegerlerGelen["filter_reset"].to_bytes(1, "little"))

    def altMotorlarDurdur(self):
        self.altSagOnMotorSet(ESC_STOP)
        self.altSolOnMotorSet(ESC_STOP)
        self.altSagArkaMotorSet(ESC_STOP)
        self.altSolArkaMotorSet(ESC_STOP)

    def ustMotorlarDurdur(self):
        self.ustMotorSet(ESC_STOP)

    def butunMotorlarDurdur(self):
        self.altMotorlarDurdur()
        self.ustMotorlarDurdur()

    def ileriGit(self, sol_hiz, sag_hiz):
        self.altSagOnMotorSet(ESC_STOP + constrain(sag_hiz, -500, 500))
        self.altSolOnMotorSet(ESC_STOP + constrain(sol_hiz, -500, 500))
        self.altSagArkaMotorSet(ESC_STOP + constrain(sag_hiz, -500, 500))
        self.altSolArkaMotorSet(ESC_STOP + constrain(sol_hiz, -500, 500))

    def geriGit(self, sol_hiz, sag_hiz):
        self.altSagOnMotorSet(ESC_STOP - constrain(sag_hiz, -500, 500))
        self.altSolOnMotorSet(ESC_STOP - constrain(sol_hiz, -500, 500))
        self.altSagArkaMotorSet(ESC_STOP - constrain(sag_hiz, -500, 500))
        self.altSolArkaMotorSet(ESC_STOP - constrain(sol_hiz, -500, 500))

    def sagaDon(self, hiz):
        self.altSagOnMotorSet(ESC_STOP - constrain(hiz, -500, 500))
        self.altSolOnMotorSet(ESC_STOP + constrain(hiz, -500, 500))
        self.altSagArkaMotorSet(ESC_STOP - constrain(hiz, -500, 500))
        self.altSolArkaMotorSet(ESC_STOP + constrain(hiz, -500, 500))

    def solaDon(self, hiz):
        self.altSagOnMotorSet(ESC_STOP + constrain(hiz, -500, 500))
        self.altSolOnMotorSet(ESC_STOP - constrain(hiz, -500, 500))
        self.altSagArkaMotorSet(ESC_STOP + constrain(hiz, -500, 500))
        self.altSolArkaMotorSet(ESC_STOP - constrain(hiz, -500, 500))

    def sagGit(self, on_hiz, arka_hiz):
        self.altSagOnMotorSet(ESC_STOP - constrain(on_hiz, -500, 500))
        self.altSolOnMotorSet(ESC_STOP + constrain(on_hiz, -500, 500))
        self.altSagArkaMotorSet(ESC_STOP + constrain(arka_hiz, -500, 500))
        self.altSolArkaMotorSet(ESC_STOP - constrain(arka_hiz, -500, 500))

    def solGit(self, on_hiz, arka_hiz):
        self.altSagOnMotorSet(ESC_STOP + constrain(on_hiz, -500, 500))
        self.altSolOnMotorSet(ESC_STOP - constrain(on_hiz, -500, 500))
        self.altSagArkaMotorSet(ESC_STOP - constrain(arka_hiz, -500, 500))
        self.altSolArkaMotorSet(ESC_STOP + constrain(arka_hiz, -500, 500))

    def yukariGit(self, hiz):
        self.ustMotorSet(ESC_STOP + constrain(hiz, -500, 500))

    def asagiGit(self, hiz):
        self.ustMotorSet(ESC_STOP - constrain(hiz, -500, 500))

    def onMesGet(self):
        rov_degerler_giden["mes_on"] = int.from_bytes(bytes(self.read_mem(rovAdresler["mes_on"], 2)), "little", signed = True)
        return rov_degerler_giden["mes_on"]

    def arkaMesGet(self):
        rov_degerler_giden["mes_arka"] = int.from_bytes(bytes(self.read_mem(rovAdresler["mes_arka"], 2)), "little", signed = True)
        return rov_degerler_giden["mes_arka"]

    def sagMesGet(self):
        rov_degerler_giden["mes_sag"] = int.from_bytes(bytes(self.read_mem(rovAdresler["mes_sag"], 2)), "little", signed = True)
        return rov_degerler_giden["mes_sag"]

    def solMesGet(self):
        rov_degerler_giden["mes_sol"] = int.from_bytes(bytes(self.read_mem(rovAdresler["mes_sol"], 2)), "little", signed = True)
        return rov_degerler_giden["mes_sol"]

    def asagiMesGet(self):
        rov_degerler_giden["mes_asagi"] = int.from_bytes(bytes(self.read_mem(rovAdresler["mes_asagi"], 2)), "little", signed = True)
        return rov_degerler_giden["mes_asagi"]

    def rollGet(self):
        rov_degerler_giden["roll"] = round(struct.unpack("f", bytes(self.read_mem(rovAdresler["roll"], 4)))[0], 2)
        return rov_degerler_giden["roll"]

    def pitchGet(self):
        rov_degerler_giden["pitch"] = round(struct.unpack("f", bytes(self.read_mem(rovAdresler["pitch"], 4)))[0], 2)
        return rov_degerler_giden["pitch"]

    def yawGet(self):
        rov_degerler_giden["yaw"] = round(struct.unpack("f", bytes(self.read_mem(rovAdresler["yaw"], 4)))[0], 2)
        return rov_degerler_giden["yaw"]

    def voltajGet(self):
        rov_degerler_giden["voltaj"] = round(struct.unpack("f", bytes(self.read_mem(rovAdresler["voltaj"], 4)))[0], 2)
        return rov_degerler_giden["voltaj"]

    def akimGet(self):
        rov_degerler_giden["akim"] = round(struct.unpack("f", bytes(self.read_mem(rovAdresler["akim"], 4)))[0], 2)
        return rov_degerler_giden["akim"]

    def wattGet(self):
        rov_degerler_giden["watt"] = round(struct.unpack("f", bytes(self.read_mem(rovAdresler["watt"], 4)))[0], 2)
        return rov_degerler_giden["watt"]

if __name__ == "__main__":

    port = "/dev/ttyUSB0"
    baud = 115200

    grovUart = rovAracUart(port, baud)
    #sleep(3)
    grovUart.adresAl()

    grovSwd = rovAracSwd()
    grovSwd.debugOn()

    grovUart.butunMotorlarDurdur()

    print("Sistem baslatildi.")
