import subprocess
import sys
import os

subprocess.run("clear")
print()
print()
print("#################################")
print("##### RaspiWiFi Uninstaller #####")
print("#################################")
print()
print()
uninstall_answer = input("Would you like to uninstall RaspiWiFi? [y/N]: ")
print()

if (uninstall_answer.lower() == "y"):
    print('Uninstalling RaspiWiFi from your system...')

    subprocess.run(["cp", os.path.dirname(os.path.realpath(__file__)) + "/reset_device/static_files/wpa_supplicant.conf.default", "/etc/wpa_supplicant/wpa_supplicant.conf"])
    subprocess.run(["chmod", "600", "/etc/wpa_supplicant/wpa_supplicant.conf"])
    subprocess.run("mv /etc/wpa_supplicant/wpa_supplicant.conf.original /etc/wpa_supplicant/wpa_supplicant.conf 2>/dev/null", shell=True)
    subprocess.run(["rm", "-rf", "/etc/raspiwifi"])
    subprocess.run(["rm", "-rf", "/usr/lib/raspiwifi"])
    subprocess.run(["rm", "-rf", "/etc/cron.raspiwifi"])
    subprocess.run(["rm", "/etc/dnsmasq.conf"])
    subprocess.run("mv /etc/dnsmasq.conf.original /etc/dnsmasq.conf 2>/dev/null", shell=True)
    subprocess.run("mv /etc/ssmtp/ssmtp.conf.original /etc/ssmtp/ssmtp.conf 2>/dev/null", shell=True)
    subprocess.run(["rm", "/etc/hostapd/hostapd.conf"])
    subprocess.run(["rm", "/etc/dhcpcd.conf"])
    subprocess.run("mv /etc/dhcpcd.conf.original /etc/dhcpcd.conf 2>/dev/null", shell=True)
    subprocess.run('sed -i \'s/# RaspiWiFi Startup//\' /etc/crontab', shell=True)
    subprocess.run('sed -i \'s/@reboot root run-parts \/etc\/cron.raspiwifi\///\' /etc/crontab', shell=True)
    
    print()
    print()
    reboot_answer = input('Uninstallation is complete. Would you like to reboot the system now?: ')

    if(reboot_answer.lower() == "y"):
        subprocess.run("reboot")
else:
    print()
    print('No changes made. Exiting unistaller...')