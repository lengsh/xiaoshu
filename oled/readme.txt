
https://learn.adafruit.com/adafruit-pioled-128x32-mini-oled-for-raspberry-pi/usage
https://www.raspberrypi-spy.co.uk/2018/04/i2c-oled-display-module-with-raspberry-pi/
https://shumeipai.nxez.com/2019/04/29/use-the-ssd1306-oled-display-on-the-raspberry-pi.html


![image](https://github.com/lengsh/xiaoshu/blob/master/oled/i2c_oled_128x64_raspberry_pi_wiring.png)

0. link pin(OLED1603 and RaspberryPi4)

OLED Pin	Pi GPIO Pin	Notes
---------------------------------------------
 Vcc		1 *		3.3V
 Gnd		14 **		Ground
 SCL		5		I2C SCL
 SDA		3		I2C SCA

* You can connect the Vcc pin to either Pin 1 or 17 as they both provide 3.3V.
** You can connect the Gnd pin to either Pin 6, 9, 14 , 20, 25, 30, 34 or 39 as they all provide Ground.

	sudo raspi-config
        ##  enable I2C 

1. setup develop envirement

	sudo apt install -y python3-dev   // ?
	sudo apt install -y python-smbus i2c-tools
	sudo apt install -y python3-pil    
	sudo apt install -y python3-pip    
	sudo apt install -y python3-setuptools  
	sudo apt install -y python3-rpi.gpio    // ?


2. Finding the OLED Display Module’s Address

	i2cdetect -y 1
 ## such as :  0x3c

3.1 use oled12864_i2c.py as library to test
  	python3 local_test.py

3.2 install Adafruit-SSD1306 library to test 
 ## https://github.com/adafruit/Adafruit_Python_SSD1306/

	sudo python -m pip install --upgrade pip setuptools wheel
	sudo pip install Adafruit-SSD1306

        python3 Adaf_test.py



