from machine import Pin, SPI
import max7219
import time

spi = SPI(0, baudrate=10000000, polarity=1, phase=0, sck=Pin(2), mosi=Pin(3))
ss = Pin(5, Pin.OUT)
number_of_metrix = 4 #change here if you are using more or less then 4 metrixs.
display = max7219.Matrix8x8(spi, ss, number_of_metrix)

display.brightness(1) #value can be 1 to 15
scrolling_message = "RASPBERRY PI PICO"
length = len(scrolling_message)

column = (length * 8)

display.text("1234",0,0) #text, x  axis, y axiz
display.show() #show the display

time.sleep(1)
while True: #a loop for scrolling message
    for x in range((number_of_metrix * 8), -column, -1):     
        display.fill(0)
        display.text(scrolling_message ,x,1) #text, x  axis, y axiz
        display.show()
        time.sleep(0.05) #set the scrolling speed. Here it is 50mS.