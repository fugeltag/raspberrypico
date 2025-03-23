from machine import Pin, I2C
import time

# כתובת I2C של BH1745 (כתובת ברירת מחדל)
BH1745_ADDRESS = 0x38

# רגיסטרים עיקריים
REG_MODE_CONTROL1 = 0x41
REG_MODE_CONTROL2 = 0x42
REG_MODE_CONTROL3 = 0x44
REG_RED_DATA_LSB  = 0x50
REG_GREEN_DATA_LSB = 0x52
REG_BLUE_DATA_LSB  = 0x54
REG_light_DATA_LSB = 0x56

# אתחול I2C (GPIO 4 = SDA, GPIO 5 = SCL)
i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=400000)
# פונקציה לכתיבה לרגיסטר
def write_register(register, value):
    i2c.writeto_mem(BH1745_ADDRESS, register, bytes([value]))

# פונקציה לקריאה מרגיסטר (שני בתים)
def read_register_16bit(register):
    data = i2c.readfrom_mem(BH1745_ADDRESS, register, 2)
    return data[1] << 8 | data[0]

# אתחול BH1745
def init_bh1745():
    # הגדרות הרכיב לפי הדוקומנטציה
    write_register(REG_MODE_CONTROL1, 0x00)  # זמן אינטגרציה = 160ms
    write_register(REG_MODE_CONTROL2, 0x90)  # Gain x1, פעיל
    write_register(REG_MODE_CONTROL3, 0x02)  # IR compensation on

# קריאת ערכי RGB ו-light
def read_rgbc():
    red = read_register_16bit(REG_RED_DATA_LSB)
    green = read_register_16bit(REG_GREEN_DATA_LSB)
    blue = read_register_16bit(REG_BLUE_DATA_LSB)
    light = read_register_16bit(REG_light_DATA_LSB)
    return red, green, blue, light

# אתחול החיישן
init_bh1745()

# קריאה כל שנייה
while True:
    red, green, blue, light = read_rgbc()
    print("Red: {}, Green: {}, Blue: {}, light: {}".format(red, green, blue, light))
    time.sleep(1)
