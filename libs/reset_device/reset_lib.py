import os
import fileinput
import subprocess
import email_sender

def config_file_hash():
	config_file = open('/etc/raspiwifi/raspiwifi.conf')
	config_hash = {}

	for line in config_file:
		line_key = line.split("=")[0]
		line_value = line.split("=")[1].rstrip()
		config_hash[line_key] = line_value

	return config_hash

def wpa_check_activate(wpa_enabled, wpa_key):
	wpa_active = False
	reboot_required = False

	with open('/etc/hostapd/hostapd.conf') as hostapd_conf:
		for line in hostapd_conf:
			if 'wpa_passphrase' in line:
				wpa_active = True

	if wpa_enabled == '1' and wpa_active == False:
		reboot_required = True
		subprocess.run(["cp", "/usr/lib/raspiwifi/reset_device/static_files/hostapd.conf.wpa", "/etc/hostapd/hostapd.conf"])

	if wpa_enabled == '1':
		with fileinput.FileInput('/etc/hostapd/hostapd.conf', inplace=True) as hostapd_conf:
			for line in hostapd_conf:
				if 'wpa_passphrase' in line:
					if 'wpa_passphrase=' + wpa_key not in line:
						print('wpa_passphrase=' + wpa_key)
						subprocess.run("reboot")
					else:
						print(line, end = '')
				else:
					print(line, end = '')

	if wpa_enabled == '0' and wpa_active == True:
		reboot_required = True
		subprocess.run(["cp", "/usr/lib/raspiwifi/reset_device/static_files/hostapd.conf.nowpa", "/etc/hostapd/hostapd.conf"])

	return reboot_required

def update_ssid(ssid_prefix, serial_last_four):
	reboot_required = False
	ssid_correct = False

	with open('/etc/hostapd/hostapd.conf') as hostapd_conf:
		for line in hostapd_conf:
			if ssid_prefix in line:
				ssid_correct = True

	if ssid_correct == False:
		with fileinput.FileInput("/etc/hostapd/hostapd.conf", inplace=True) as file:
			for line in file:
				if 'ssid=' in line:
					line_array = line.split('=')
					line_array[1] = ssid_prefix + ' ' + serial_last_four
					print(line_array[0] + '=' + line_array[1])
				else:
					print(line, end = '')

		reboot_required = True
			
	return reboot_required

def is_wifi_active():
	iwconfig_out = subprocess.check_output(['iwconfig']).decode('utf-8')
	wifi_active = True

	if "Access Point: Not-Associated" in iwconfig_out:
		wifi_active = False

	return wifi_active

def reset_to_host_mode():
	if not os.path.isfile('/etc/raspiwifi/host_mode'):
		email_sender.send_reset_message()
		subprocess.run(["aplay", "/usr/lib/raspiwifi/reset_device/button_chime.wav"])
		subprocess.run(["rm", "-f", "/etc/wpa_supplicant/wpa_supplicant.conf"])
		subprocess.run('rm -f" /home/pi/Projects/RaspiWifi/tmp/*', shell=True)
		subprocess.run(["rm", "/etc/cron.raspiwifi/apclient_bootstrapper"])
		subprocess.run(["cp", "/usr/lib/raspiwifi/reset_device/static_files/aphost_bootstrapper", "/etc/cron.raspiwifi/"])
		subprocess.run(["chmod", "+x", "/etc/cron.raspiwifi/aphost_bootstrapper"])
		subprocess.run(["mv", "/etc/dhcpcd.conf", "/etc/dhcpcd.conf.original"])
		subprocess.run(["cp", "/usr/lib/raspiwifi/reset_device/static_files/dhcpcd.conf", "/etc/"])
		subprocess.run(["mv", "/etc/dnsmasq.conf", "/etc/dnsmasq.conf.original"])
		subprocess.run(["cp", "/usr/lib/raspiwifi/reset_device/static_files/dnsmasq.conf", "/etc/"])
		subprocess.run(["cp", "/usr/lib/raspiwifi/reset_device/static_files/dhcpcd.conf", "/etc/"])
		subprocess.run(["pihole", "disable"])
		subprocess.run(["rm", "-f", "/etc/systemd/system/dnsmasq.service"])
		subprocess.run(["touch", "/etc/raspiwifi/host_mode"])
		subprocess.run("reboot")
