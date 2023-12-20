from machine import Pin, I2C
from ads1x15 import ADS1115
import utime

#erstellung eine I2c objekt  Pins GP2 und GP3
i2c = I2C(scl=Pin(3), sda=Pin(2))
#erstellung eine ADS1115-objekt  
ads = ADS1115(i2c, address=0x48)
#verstärkung faktor
ads.gain = 1

prev_time = utime.ticks_ms()
current_time = prev_time
prev_voltage = 0
zero_crossings = 0

  

while True:

#a0 lesen von adc 

 voltage = ads.read(2)

 

 if prev_voltage < 0 and voltage >= 0:
     #einenullstelle detektiert wurde

    zero_crossings += 1

 if utime.ticks_diff(utime.ticks_ms(), current_time) >= 1000:
    #f=1/2 der nullstellen pro secunde
    frequency = zero_crossings / 2
    zero_crossings = 0          # Nullstellen zurucksetzen
    #berechnung der derehzahl
    rpm = frequency * 60 / 8   #bersätzungverhältniss 8
    print('Drehzahl: ', rpm, 'RPM')

 prev_voltage = voltage
 utime.sleep(0.001)