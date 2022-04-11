#! python3

from .shell import *
from subprocess import call
from datetime import datetime
import os

def __device_probe_ini():
	options = [
		('/vendor/etc/wifi', 'WCNSS_qcom_cfg.ini'),
		('/system/etc/wifi', 'WCNSS_qcom_cfg.ini'),
	]

	for (path, name) in options:
		code = qsh(f"adb shell stat {path}/{name}")
		if (is_success(code)):
			return {
				'ini_path': path,
				'ini_name': name,
			}

	return {
		'ini_path': None,
		'ini_name': None,
	}

def __device_probe_ko():
	options = [
		('/vendor/lib/modules', 'qca_cld3_wlan.ko'),
		('/vendor/lib/modules/qca_cld3', 'qca_cld3_wlan.ko'),
		('/system/lib/modules', 'wlan.ko'),
	]

	for (path, name) in options:
		code = qsh(f"adb shell stat {path}/{name}")
		if (is_success(code)):
			return {
				'ko_path': path,
				'ko_name': name,
			}

	return {
		'ko_path': None,
		'ko_name': None,
	}

def __device_probe_hostapd_conf():
	options = [
		('/data/misc/wifi', 'hostapd.conf'),
		('/data/vendor/wifi/hostapd', 'hostapd.conf'),
	]

	for (path, name) in options:
		code = qsh(f"adb shell stat {path}/{name}")
		if (is_success(code)):
			return {
				'hostapd_conf_path': path,
				'hostapd_conf_name': name,
			}

	return {
		'hostapd_conf_path': None,
		'hostapd_conf_name': None,
	}

def adb_root(device_id):
    #print("adb root #1 %s"%datetime.now().time())
    #bsh("adb -s {} wait-for-device".format(device_id))
    #print("adb root #2 %s"%datetime.now().time())
    bsh("adb -s {} root".format(device_id))
    #print("adb root #3 %s"%datetime.now().time())
    #bsh("adb -s {} wait-for-device".format(device_id))
    #print("adb root #4 %s"%datetime.now().time())

def adb_wait_for_device(device_id):
	print("Waiting for adb...")
	bsh("adb -s {} wait-for-device".format(device_id))

def adb_sync(device_id):
    bsh("adb -s {} shell sync".format(device_id))

def adb_remount(device_id):
    bsh("adb -s {} remount".format(device_id))

def adb_disable_verity(device_id):
    bsh("adb -s {} disable-verity".format(device_id))

def adb_reboot(device_id):
    bsh("adb -s {} reboot".format(device_id))

def adb_push(device_id, file, path):
    bsh("adb -s {} push {} {}".format(device_id, file, path))
    return 0

def adb_mount(device_id, path):
    bsh("adb -s {} shell mount -o rw,remount {}".format(device_id, path))

def adb_chmod_exec(device_id, file, path):
    # make sure full_path is
    full_path = os.path.join(path, file)
    full_path = full_path.replace('\\', '/')
    print("full path:", full_path)
    bsh("adb -s {} shell chmod 777 {}".format(device_id, full_path))

def device_info(device_id):
    info = {
        #'id': esh("adb -s {} shell get-serialno".format(device_id)),
        #'build': esh("adb -s {} shell getprop persist.build.path".format(device_id)),
        #'apps': esh("adb -s {} shell getprop persist.build.apps".format(device_id)),
        #'ko_tag': esh("adb -s {} shell getprop persist.build.ko_tag".format(device_id)),
        'product': esh("adb -s {} shell getprop ro.product.name".format(device_id)),
        #'meta': esh("adb -s {} shell "cat /vendor/firmware_mnt/verinfo/ver_info.txt |grep Meta_Build_ID | cut -f2 -d ":" | sed 's/[", ]//g'"".format(device_id)),
    }

    # Fix me filter out "
    cmd = "adb -s {} shell cat /vendor/firmware_mnt/verinfo/ver_info.txt |grep Meta_Build_ID | cut -f2 -d : | sed 's/[, ]//g'".format(device_id)
    info['meta'] = esh(cmd)

    #info.update(__device_probe_ini())
    #info.update(__device_probe_ko())
    #info.update(__device_probe_hostapd_conf())

    return info

def wait_for_adb():
	print("Waiting for adb...")
	bsh("adb wait-for-device")

def adb_devices():
    print("adb devices")
    output = bsh("adb devices")
    # assume output is using below format
    # List of devices attached
    # 174e29ac        device
    # 19024635        device

    filter = ["List", "of", "devices", "attached", "device"]
    device_list = []
    for item in (output.split()):
        if item not in filter:
            device_list.append(item)
    print(device_list)
    return device_list

def wait_for_boot():
	print(f"Waiting for boot complete...")
	bsh("adb wait-for-device root")

	while (True):
		result = esh("adb shell getprop dev.bootcomplete")
		if (result == "1"):
			break

		bsh("sleep 0.5s")

def wait_for_file(fullpath, wait_for_exist = True):
	print(f"Waiting for '{fullpath}' file...")
	bsh("adb wait-for-device root")

	while (True):
		result = qsh(f"adb shell stat {fullpath}")
		exists = is_success(result)
		if (exists == wait_for_exist):
			break

		bsh("sleep 0.5s")

def wait_for_process(name, wait_for_start = True):
	print(f"Waiting for '{name}' process...")
	bsh("adb wait-for-device root")

	while (True):
		pid = eqsh(f"adb shell pidof {name}")
		is_running = is_success(pid)
		if (is_running == wait_for_start):
			break

		bsh("sleep 0.5s")

def wait_for_service(name, wait_for_start = True):
	print(f"Waiting for '{name}' service...")
	bsh("adb wait-for-device root")

	while (True):
		result = eqsh(f"adb shell service check {name}")
		is_running = is_success(result) and result.endswith(": found")
		if (is_running == wait_for_start):
			break

		bsh("sleep 0.5s")
