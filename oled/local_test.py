from microbit import *
import oled12864_i2c

oled = oled12864_i2c.OLED12864_I2C()
oled.clear()

n = 0

while True:
    oled.text(0,0,'Hello!')
    n+=1  # n= n+1
    oled.text(0,1,str(n))
    sleep(1000)
# Write your code here :-)