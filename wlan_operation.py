#https://github.qualcomm.com/junwan/Perfdump2Guide/blob/master/api_guide/example_code.md

import subprocess
import time

class wlan_operation():
    def __init__(self, serial):
        self.serial = serial
        return

    def query_connection_status(self, ssid):
        cmd_wifi_status = 'adb -s ' + self.serial + ' shell cmd wifi status'
        status, output = subprocess.getstatusoutput(cmd_wifi_status)
        if status != 0:
            print('Error: ' + cmd_wifi_status)
            return False
        if 'Wifi is disabled' in output:
            cmd_enable_wifi = 'adb -s ' + self.serial + ' shell cmd wifi set-wifi-enabled enabled'
            status, output = subprocess.getstatusoutput(cmd_enable_wifi)
            if status != 0:
                print('Error: ' + cmd_enable_wifi)
                return False
        elif ssid in output:
            print('already connected.')
            return True

    def scan_result(self, ssid):
        target_wifi_found = False
        retry_count = 0
        while retry_count < 10:
            cmd_list_scans = 'adb -s ' + self.serial + ' shell cmd wifi list-scan-results'
            status, output = subprocess.getstatusoutput(cmd_list_scans)
            if status == 0:
                if ssid in output:
                    target_wifi_found = True
                    break
            time.sleep(1)
            retry_count += 1

        return target_wifi_found

    def connect(self, ssid, password = None):
        if not password:
            cmd_connect_network = 'adb -s ' + self.serial + ' shell cmd wifi connect-network ' \
                                + ssid + ' open'
        else:
            cmd_connect_network = 'adb -s ' + self.serial + ' shell cmd wifi connect-network ' \
                                + ssid + ' wpa2 ' + password
        status, output = subprocess.getstatusoutput(cmd_connect_network)
        if status != 0:
            print('Error: ' + cmd_connect_network)
            return False
        retry_count = 0
        while retry_count < 10:
            cmd_wifi_status = 'adb -s ' + self.serial + ' shell cmd wifi status'
            status, output = subprocess.getstatusoutput(cmd_wifi_status)
            if status != 0:
                return False
            if 'Wifi is connected to' in output:
                print('wifi connected.')
                return True
            time.sleep(1)
        retry_count += 1
        return False

if __name__ == "__main__":
    w = wlan_operation("e25a1c75")
    w.query_connection_status("555")
    w.scan_result("555")
    w.connect("555", None)