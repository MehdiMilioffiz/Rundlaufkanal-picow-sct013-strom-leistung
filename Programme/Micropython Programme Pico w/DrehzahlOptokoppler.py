from machine import Pin, Timer
import time

sensor_pin = Pin(16, Pin.IN, Pin.PULL_UP)

#variablem für die Zeitmessung
previous_time = time.ticks_ms()
current_time = time.ticks_ms()

#funktion ,die bei eine unterbrechung des lichtstrahls aufgerufen wird
def handle_interrupt (pin):
 global previous_time
 global current_time
 previous_time = current_time
 current_time = time.ticks_ms()


sensor_pin.irq(trigger=Pin.IRQ_FALLING, handler=handle_interrupt)

 #endloseschleife zur berechnung und ausgabe der drehzahl

while True:
 elapsed_time = time.ticks_diff(current_time, previous_time) / 1000.0
 if elapsed_time > 0:
  speed = 60.0 / elapsed_time #berechnung der drehzahl umdrehung pro minute
  print("Speed: ", speed, "RPM")
 time.sleep(0.1)
