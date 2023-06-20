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
mntpath = input("Please enter where you mounted your filesystem(Example: /mnt1/)")

print("Deleting Setup.app \n")
device.exec_command(f"rm -rf {mntpath}/Applications/Setup.app")
device.exec_command(f"rm -rf {mntpath}/var/mobile/Library/Accounts/*")
print("Done!")
device.close()
iproxy.kill()
iproxy.terminate()
