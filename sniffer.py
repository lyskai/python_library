#! python3
from .shell import *
from .device import *
from subprocess import call
from datetime import datetime
import os
import re

def get_wlan_driver_binary(device):
    id = adb_get_chip(device)
    if id == "1103":
        return "/vendor_dlkm/lib/modules/qca_cld3_qca6490.ko"
    elif id == "1108":
        return "/vendor_dlkm/lib/modules/qca_cld3_kiwi_v2.ko"

def get_wlan_driver_name(device):
    id = adb_get_chip(device)
    if id == "1103":
        return "qca6490"
    elif id == "1107":
        return "kiwi_v2"

def adb_set_channel_bandwidth(device, channel, bandwitdh):
    bsh("adb -s {} shell iwpriv wlan0 setMonChan {} {}".format(device, channel, bandwitdh))

def check_iwpriv(device):
    result = bsh("adb -s {} shell which iwpriv".format(device))
    if is_err(result.returncode):
        return False
    return True

def adb_init_sniffer_setting(device, channel, bandwitdh):
    driver = get_wlan_driver_name(device)
    adb_rmmod(device, driver)

    binary = get_wlan_driver_binary(device)
    adb_insmod(device, binary, "sniffer")
    bsh("sleep 1s")
    adb_interface_up(device, "wlan0")
    bsh("sleep 1s")
    # this folder contain many logs from other module, 
    # remove them before sniffer test
    adb_remove_folder(device, "/data/misc/qdma/tmp")
    adb_set_channel_bandwidth(device, channel, bandwitdh)
    adb_stop_capture(device)

def adb_start_capture(device, file):
    thread = bsh_async("adb -s {} shell tcpdump -i wlan0 -w {}".format(device, file))
    thread.start()

def adb_stop_capture(device):    
    bsh("adb -s {} shell killall tcpdump".format(device))

def adb_pull_sniffer_log(device, file, log_folder):    
    bsh("adb -s {} pull {} {}".format(device, file, log_folder))
