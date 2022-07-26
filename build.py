#! python3

from .shell import *
from subprocess import call
from datetime import datetime
import os

import xml.etree.ElementTree as etree

def __transform_file(fileXml):
	name = fileXml.find('file_name').text

	return (
		name,
		{
			'name': name,
			'path': fileXml.find('file_path').text,
		}
	)

def __transform_build(buildXml):
	name = buildXml.find('name').text

	return (
		name,
		{
			'name': name,
			'chipset': buildXml.find('chipset').text,
			'id': buildXml.find('build_id').text,
			'samba_path': buildXml.find('windows_root_path').text,
			'linux_path': buildXml.find('linux_root_path').text,
			'files': dict(map(__transform_file, buildXml.findall('./download_file'))),
		}
	)

def build_info(path):
	tree = etree.parse(f"{path}/contents.xml")
	root = tree.getroot()
	return dict(map(__transform_build, root.findall('./builds_flat/build')))

def source(target):
    bsh("source build/envsetup.sh && lunch {}-userdebug".format(target))

def rebuild_kernel(target):
    cmd = "RECOMPILE_KERNEL=1 LTO=thin ./kernel_platform/build/android/prepare_vendor.sh"\
          "{} consolidate < /dev/null".format(target)
    bsh(cmd)

def build_vnedor():
    cmd = "(time bash build.sh -j16 dist --target_only) |& tee Vendor_makelog_$(date +%Y%m%d_%H%M%S).txt"
    bsh(cmd)
