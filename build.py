#! python3

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
