import os
import subprocess

def install_prereqs():
	subprocess.run("clear")
	subprocess.run(["apt", "update"])
	subprocess.run("clear")
	subprocess.run(["apt", "install", "-y", "python3-rpi.gpio", "python3-pip", "dnsmasq", "hostapd", "ssmtp", "mailutils"])
	subprocess.run("clear")
	print("Installing Flask web server...")
	print()
	subprocess.run(["pip3", "install", "flask", "pyopenssl"])
	subprocess.run("clear")

def copy_configs(wpa_enabled_choice):
	subprocess.run(["mkdir", "/usr/lib/raspiwifi"])
	subprocess.run(["mkdir", "/etc/raspiwifi"])
	subprocess.run(["cp", "-a", "libs/*", "/usr/lib/raspiwifi/"])
	subprocess.run(["mv", "/etc/wpa_supplicant/wpa_supplicant.conf", "/etc/wpa_supplicant/wpa_supplicant.conf.original"])
	subprocess.run(["rm", "-f", "./tmp/*"])
	subprocess.run(["mv", "/etc/dnsmasq.conf", "/etc/dnsmasq.conf.original"])
	subprocess.run(["cp", "/usr/lib/raspiwifi/reset_device/static_files/dnsmasq.conf", "/etc/"])

	if wpa_enabled_choice.lower() == "y":
		subprocess.run(["cp", "/usr/lib/raspiwifi/reset_device/static_files/hostapd.conf.wpa", "/etc/hostapd/hostapd.conf"])
	else:
		subprocess.run(["cp", "/usr/lib/raspiwifi/reset_device/static_files/hostapd.conf.nowpa", "/etc/hostapd/hostapd.conf"])
	
	subprocess.run(["mv", "/etc/dhcpcd.conf", "/etc/dhcpcd.conf.original"])
	subprocess.run(["cp", "/usr/lib/raspiwifi/reset_device/static_files/dhcpcd.conf", "/etc/"])
	subprocess.run(["mkdir", "/etc/cron.raspiwifi"])
	subprocess.run(["cp", "/usr/lib/raspiwifi/reset_device/static_files/aphost_bootstrapper", "/etc/cron.raspiwifi"])
	subprocess.run(["chmod", "+x", "/etc/cron.raspiwifi/aphost_bootstrapper"])
	subprocess.run('echo "# RaspiWiFi Startup" >> /etc/crontab', shell=True)
	subprocess.run('echo "@reboot root run-parts /etc/cron.raspiwifi/" >> /etc/crontab', shell=True)
	subprocess.run(["mv", "/usr/lib/raspiwifi/reset_device/static_files/raspiwifi.conf", "/etc/raspiwifi"])
	subprocess.run(["mv", "/etc/ssmtp/ssmtp.conf", "/etc/ssmtp/ssmtp.conf.original"])
	subprocess.run(["cp", "/usr/lib/raspiwifi/reset_device/static_files/ssmtp.conf", "/etc/ssmtp/ssmtp.conf"])
	subprocess.run(["touch", "/etc/raspiwifi/host_mode"])

def update_main_config_file(entered_ssid, auto_config_choice, auto_config_delay, ssl_enabled_choice, server_port_choice, wpa_enabled_choice, wpa_entered_key):
	if entered_ssid != "":
		cmd = 'sed -i \'s/RaspiWiFi Setup/' + entered_ssid + '/\' /etc/raspiwifi/raspiwifi.conf'
		subprocess.run(cmd, shell=True)
	if wpa_enabled_choice.lower() == "y":
		cmd = 'sed -i \'s/wpa_enabled=0/wpa_enabled=1/\' /etc/raspiwifi/raspiwifi.conf'
		subprocess.run(cmd, shell=True)
		cmd = 'sed -i \'s/wpa_key=0/wpa_key=' + wpa_entered_key + '/\' /etc/raspiwifi/raspiwifi.conf'
		subprocess.run(cmd, shell=True)
	if auto_config_choice.lower() == "y":
		cmd = 'sed -i \'s/auto_config=0/auto_config=1/\' /etc/raspiwifi/raspiwifi.conf'
		subprocess.run(cmd, shell=True)
	if auto_config_delay != "":
		cmd = 'sed -i \'s/auto_config_delay=300/auto_config_delay=' + auto_config_delay + '/\' /etc/raspiwifi/raspiwifi.conf'
		subprocess.run(cmd, shell=True)
	if ssl_enabled_choice.lower() == "y":
		cmd = 'sed -i \'s/ssl_enabled=0/ssl_enabled=1/\' /etc/raspiwifi/raspiwifi.conf'
		subprocess.run(cmd, shell=True)
	if server_port_choice != "":
		cmd = 'sed -i \'s/server_port=80/server_port=' + server_port_choice + '/\' /etc/raspiwifi/raspiwifi.conf'
		subprocess.run(cmd, shell=True)
