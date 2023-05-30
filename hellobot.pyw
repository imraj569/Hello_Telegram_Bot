import os , sys , time
time.sleep(10)
#replace your file path before past it on startup folder
file_path = "D:\\Hello_Telegram_Bot\\main.pyw"
try:
    os.startfile(file_path)
    sys.exit()
except:
    sys.exit()