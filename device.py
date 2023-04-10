#! python3
from .shell import *
from subprocess import call
from datetime import datetime
import os
import re

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

def adb_cmd(device_id, cmd):
    result = bsh("adb -s {} shell \"{}\"".format(device_id, cmd))
    if is_err(result.returncode):
        print(result.stdout)
    return result.returncode

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

def adb_get_verity(device_id):
    result = bsh("adb -s {} shell getprop".format(device_id))
    if is_err(result.returncode):
        print("getprop failed")
    for line in re.split(r'[\n\r]+', result.stdout):
        #line = re.sub(r'\s+$', r'', line)
        if "[ro.boot.veritymode]" in line and "disabled" in line:
            #print(line.split()[1].split())
            print("verify disabled")
            return False
    return True

def adb_get_property(device_id, property):
    result = bsh("adb -s {} shell getprop".format(device_id))
    if is_err(result.returncode):
        print("getprop failed")
    for line in re.split(r'[\n\r]+', result.stdout):
        if property in line:
            return line
    return ""

def adb_reboot(device_id):
    bsh("adb -s {} reboot".format(device_id))

def adb_keep_debugfs_mounted(device_id):
    bsh("adb -s {} shell setprop persist.dbg.keep_debugfs_mounted true".format(device_id))

def adb_mount_debugfs(device_id):
    # Add fix to check if debugfs has already been mounted
    result = bsh("adb -s {} shell mount -t debugfs none /sys/kernel/debug/".format(device_id))
    if is_err(result.returncode) and "Device or resource busy" not in result.stdout:
        print(result.stdout)

def adb_push(device_id, file, path):
    result = bsh("adb -s {} push {} {}".format(device_id, file, path))
    if "error" in result.stdout:
        return (-1, result.stdout)
    else:
        return (0, result.stdout)

def adb_rmmod(device_id, driver):
    bsh("adb -s {} shell rmmod {}".format(device_id, driver))

def adb_insmod(device_id, binary, mode):
    if mode == "sniffer":
        bsh("adb -s {} shell insmod {} con_mode=4".format(device_id, binary))
    else:
        bsh("adb -s {} shell insmod {}".format(device_id, binary))

def adb_interface_up(device_id, interface):
    bsh("adb -s {} shell ifconfig {} up".format(device_id, interface))

def adb_remove_folder(device_id, folder):
    bsh("adb -s {} shell rm -rf {}".format(device_id, folder))

def adb_mount(device_id, path):
    bsh("adb -s {} shell mount -o rw,remount {}".format(device_id, path))

def adb_pull_cnss_log(device_id, log_path = "."):
    bsh("adb -s {} shell cat /d/ipc_logging/cnss/log > {}".format(device_id,
                                                                  os.path.join(log_path, "ipc_cnss.txt")))
    bsh("adb -s {} shell cat /d/ipc_logging/cnss-long/log > {}".format(device_id,
                                                                  os.path.join(log_path, "ipc_cnss-long.txt")))
def adb_pull_qmi_log(device_id, log_path = "."):
    bsh("adb -s {} shell cat /d/ipc_logging/qrtr_7/log > {}".format(device_id,
                                                                  os.path.join(log_path, "ipc_qrtr_7.txt")))
    bsh("adb -s {} shell cat /d/ipc_logging/qrtr_ns/log > {}".format(device_id,
                                                                  os.path.join(log_path, "ipc_qrtr_ns.txt")))

def adb_pull_mhi_log(device_id, log_path = "."):
    bsh("adb -s {} shell cat /d/ipc_logging/mhi_*00/log > {}".format(device_id,
                                                                     os.path.join(log_path, "ipc_mhi.txt")))
    bsh("adb -s {} shell cat /d/ipc_logging/mhi_*DIAG/log > {}".format(device_id,
                                                                       os.path.join(log_path, "ipc_mhi_diag.txt")))
    bsh("adb -s {} shell cat /d/ipc_logging/mhi_*LOOPBACK/log > {}".format(device_id,
                                                                           os.path.join(log_path, "ipc_mhi_LOOPBACK.txt")))

def adb_pull_pcie_log(device_id, log_path = "."):
    file_list = ["dump", "long", "short"]
    for idx in range(0, 3):
        for file in file_list:
            file_name = "ipc_pcie" + str(idx) + "-" + file
            bsh("adb -s {} shell cat /d/ipc_logging/pcie{}-{}/log > {}".format(device_id, str(idx), file,
                                                                  os.path.join(log_path, file_name)))

def adb_pull_wlan_log(device_id, log_path = "."):
    bsh("adb -s {} pull /data/vendor/wifi/wlan_logs {}".format(device_id, log_path))

def adb_pull_logcat_log(device_id, log_path = "."):
    bsh("adb -s {} logcat -d > {}".format(device_id, os.path.join(log_path, "logcat.txt")))

def adb_pull_dmesg_log(device_id, log_path = "."):
    bsh("adb -s {} shell dmesg > {}".format(device_id, os.path.join(log_path, "dmesg.txt")))

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
    result = bsh("adb devices")
    if is_err(result.returncode) :
        print(result.stdout)
        return []
    else:
        output = result.stdout

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

def adb_get_chip(device_id):
    result = bsh("adb -s {} shell lspci | grep 17cb:11 | cut -f4 -d : | cut -f1 -d ' '".format(device_id))
    for line in re.split(r'[\n\r]+', result.stdout):
        if line.startswith("11"):
            return line

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
