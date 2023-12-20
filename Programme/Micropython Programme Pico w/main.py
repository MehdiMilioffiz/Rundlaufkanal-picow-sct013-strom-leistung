import machine
import utime
from machine import Pin, ADC
import math
from math import pow, sqrt
ADC_BITS = 16
ADC_COUNTS = 1 << ADC_BITS
SUPPLY_VOLTAGE = 3300
#

while True:
     offsetCurrent = ADC_COUNTS >> 1
     #print("--",offsetCurrent)
     sumCurrent = 0
     currentCalibration = 10
     adc_current = machine.ADC(28)
     
     for sample in range(0, 1000):
            
             sample_current = adc_current.read_u16()
             #print("------111111111----------------------------------------",sample_current)
             offsetCurrent += (sample_current - offsetCurrent)/1024
             #print(offsetCurrent)
             #print("1111-----",sample_current)
             filteredCurrent = sample_current - offsetCurrent
             #print("---aa----",filteredCurrent)
             sqrtCurrent = pow(filteredCurrent, 2)
             #print("----2---",sqrtCurrent)
             sumCurrent += sqrtCurrent          
             #print("---3----",sumCurrent)
             
    
     current_ratio = currentCalibration * ((3.3) / ADC_COUNTS)
     strom = current_ratio * sqrt(sumCurrent / 1000)
     print(strom,"A")