import spidev
import time
import RPi.GPIO as GPIO

spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz = 1000000

def measure_ch0():
    msg =[0b01100000,0b00000000]
    digit_byte = spi.xfer2(msg)
    digit_in = (digit_byte[0] << 8) +digit_byte[1]
    return digit_in
def measure_ch1():
    msg =[0b01110000,0b00000000]
    digit_byte = spi.xfer2(msg)
    digit_in = (digit_byte[0] << 8) +digit_byte[1]
    return digit_in

def check(x,y):
    if y > 1000:
        result =3
        print("D")
        return result
    if y <= 100:
        result =2
        print("U")
        return result
    if x > 1000:
        result =1
        print("R")
        return result
    if x <= 100:
        result = 0
        print("L")
        return result

a = []
password = [0,1,2,3]

for i in range(4):
    while True:
        passwordId = check(measure_ch0(),measure_ch1())
        if passwordId == None:
            continue
        a.append(passwordId)
        print(a)
        if passwordId != None:
            time.sleep(1)
            break

if a == password:
    GPIO.setmode(GPIO.BOARD)
    PWM =12
    LED_G =13
    GPIO.setup(PWM,GPIO.OUT)
    GPIO.setup(LED_G,GPIO.OUT)

    GPIO.output(LED_G,GPIO.HIGH)
    time.sleep(2)
    GPIO.output(LED_G,GPIO.LOW)

    p =GPIO.PWM(PWM, 50)
    p.start(0)
    p.ChangeDutyCycle(5)
    print("end")

    p.stop()

if a != password:

    GPIO.setmode(GPIO.BOARD)
    LED_R =11
    GPIO.setup(LED_R,GPIO.OUT)

    GPIO.output(LED_R,GPIO.HIGH)
    time.sleep(2)
    GPIO.output(LED_R,GPIO.LOW)



GPIO.cleanup()
