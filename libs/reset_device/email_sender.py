import socket
import subprocess
import os

def config_file_hash():
	config_file = open('/etc/raspiwifi/raspiwifi.conf')
	config_hash = {}

	for line in config_file:
		line_key = line.split("=")[0]
		line_value = line.split("=")[1].rstrip()
		config_hash[line_key] = line_value

	return config_hash

config_hash = config_file_hash()
recipient = config_hash["email_address"]

def send_ip_message():
    if os.path.isfile('/etc/raspiwifi/client_first_boot'):
        ip_addr = (([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")] or [[(s.connect(("8.8.8.8", 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) + ["no IP found"])[0]
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
