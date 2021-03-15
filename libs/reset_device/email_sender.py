import socket
import subprocess
import os
from reset_lib import config_file_hash

ip_addr = (([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")] or [[(s.connect(("8.8.8.8", 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) + ["no IP found"])[0]
config_hash = config_file_hash()
recipient = config_hash["email_address"]

def send_ip_message():
    if os.path.isfile('/etc/raspiwifi/client_first_boot'):
        body = 'Raspberry Pi IP: ' + ip_addr
        subject = 'Pi-hole ready!'
        cmd = 'echo "' + body + '" | mail -s "' + subject + '" ' + recipient
        subprocess.run(cmd,shell=True)
        subprocess.run(["rm", "-f", "/etc/raspiwifi/client_first_boot"])

def send_reset_message():
    body = 'Raspberry Pi has reset to host mode. Reconfigure by joining SSID RaspiWiFi Setup'
    subject = 'Raspberry Pi has reset'
    cmd = 'echo "' + body + '" | mail -s "' + subject + '" ' + recipient
    subprocess.run(cmd,shell=True)
