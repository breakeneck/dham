from machine import Pin


class esp8266:
    rx = 3
    tx = 1
    d0 = 16  # wake
    d1 = 5
    d2 = 4
    d3 = 0  # flash
    d4 = 2
    d5 = 14
    d6 = 12
    d7 = 13
    d8 = 15
    a0 = 0


# SCK	PA_01，PA_11，PB_16，PB_27
# MOSI	PA_04，PA_09，PA_10，PB_02，PB_18
# MISO	PA_03，PA_05，PA_10，PB_01，PB_17
# CS	PA_02，PA_12，PB_00，PB_07，PB_15
# ---------
# PWM CH	W60x PWM supported IO
# CH 0	PA_00，PA_05，PB_05，PB_18，PB_19，PB_30
# CH 1	PA_01，PA_07，PB_04，PB_13，PB_17，PB_20
# CH 2	PA_02，PA_08，PB_04，PB_03，PB_16，PB_21
# CH 3	PA_03，PA_09，PB_02，PB_06，PB_15，PB_22
# CH 4	PA_04，PA_10，PB_01，PB_08，PB_14，PB_23
class w600:
    a0 = Pin.PA_00
    a1 = Pin.PA_01
    b6 = Pin.PB_06
    b7 = Pin.PB_07
    b8 = Pin.PB_08
    b9 = Pin.PB_09
    b10 = Pin.PB_10
    b11 = Pin.PB_11
    b12 = Pin.PB_12
    b13 = Pin.PB_13
    b14 = Pin.PB_14
    b15 = Pin.PB_15
    b16 = Pin.PB_16
    b17 = Pin.PB_17
    b18 = Pin.PB_18