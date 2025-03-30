import network
import socket
import camera
import time

# האינטרנט לרשת החיבור הגדרת
SSID = "name"  # הרשת שם
PASSWORD = "password"  # הרשת סיסמת
wlan = network.WLAN(network.STA_IF)  # לקוח למצב האינטרנט של הממשק הגדרת (STA_IF)
wlan.disconnect() # קודם מחיבור מתנתק
wlan.active(True)  # האינטרנט הפעלת
wlan.connect(SSID, PASSWORD)  # וסיסמא שם עם לרשת התחברות

# לאינטרנט יתחבר שהמכשיר חכה
while not wlan.isconnected():
    time.sleep(1)  # יתבצע החיבור עד המתן

print("Connected! IP:", wlan.ifconfig()[0]) 

# המצלמה הגדרת
camera.init(0, format=camera.JPEG, fb_location=camera.PSRAM)  # PSRAM זיכרון בשימוש JPEG לפורמט המצלמה אתחול
camera.framesize(camera.FRAME_QVGA)  # (QVGA) 320x240 תמונה גודל הגדרת
camera.flip(1)  # (הפוכה תמונה בעיית לתקן כדי) 180 מעלות ב-התמונה הפיכת

def start_server():
    # לשרת סוקט פתיחת
    addr = ('', 80)  # HTTP ל-ברירת מחדל הפורט הוא (80) פורט ו-IP כתובת הגדרת
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # TCP סוקט יצירת
    s.bind(addr)  # שהגדרנו והפורט לכתובת הסוקט קישור
    s.listen(5)  # להתבצע שיכולים מקבילים חיבורים מספר של ההגדרה
    
    while True:
        try: # הזה בבלוק הפעולות את לבצע ננסה לכן ,לשגיאה לגרום עשוי זה קוד
            # מהלקוחות בקשות קבלת
            conn, addr = s.accept()  # נכנס חיבור קבלת
            request = conn.recv(1024)  # מהלקוח הבקשה קריאת
            request = str(request)  # למחרוזת הבקשה המרת
            # הראשי לעמוד הבקשה היא אם בדיקה
            if "GET / " in request:
                conn.send("HTTP/1.1 200 OK\n")  # OK 200 סטטוס עם חיובית תשובה שליחת
                conn.send("Content-Type: text/html\n\n")  # HTML כ-התוכן סוג הגדרת
                conn.send("""
                <html>
                <head><title>ESP32-CAM</title></head>
                <body>
                    <img src="/cam.jpg" style="width:100%">
                    <script>
                        setInterval(() => { document.querySelector("img").src = "/cam.jpg?" + new Date().getTime(); }, 100);
                    </script>
                </body>
                </html>
                """)  # (100ms כל תתעדכן המצלמה) חיה תמונה עם HTML שליחת

            # (cam.jpg) לתמונה הבקשה היא אם בדיקה
            elif "GET /cam.jpg" in request:
                img = camera.capture()  # מהמצלמה תמונה צילום
                try:
                    conn.send(img)  # ללקוח התמונה שליחת
                except OSError as e:
                    print(f"תמונה שליחת בעת שגיאה: {e}")

            conn.close()  # הלקוח עם החיבור סגירת

        except OSError: # עליו נדלג מסויים בפריים שגיאה יתקבל אם
            if conn:
                conn.close()  # שגיאה של במקרה החיבור סגירת

# השרת הפעלת
start_server()  # השרת הרצת התחלת
