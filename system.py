import sys

def check_python_version(major_request, minor_request):
    major, minor = sys.version_info[:2]
    if (major, minor) < (major_request, minor_request):
        print("This script requires python >={}.{} to run!\n".format(major_request, minor_request))
        print("You seem to be running: " + sys.version)
        sys.exit(1)
