#! python3
import subprocess
from datetime import datetime
from sys import exit
"""

lib-shell contains helper functions to ease interaction with shell commands.
There are two primary operations:

	sh() - exectue a given shell command
	esh() - evaluate a given shell command

There are two additional functions to help understand the results of the above
functions:

	is_success() - returns true if the given result indicates success
	is_err() - returns the boolean opposite of is_success()

The remaining functions are slight variations on sh() and esh(), with 'quiet' or
'bail' applied. 'Quiet' pipes stderr and stdout to DEVNULL, while 'bail' simply
exits the program on failure. The full table of shell functions are as follows:

	sh() - SHell
	bsh() - Bail, SHell
	qsh() - Quiet, SHell
	esh() - Evaluate, SHell
	ebsh() - Evaluate, Bail, SHell
	eqsh() - Evaluate, Quiet, SHell

"""
from subprocess import DEVNULL, PIPE, run
from os import path as os_path
import threading
import logging

def is_success(result):
	""" Returns true if the given result is not a non-zero status code """
	return isinstance(result, str) or result == 0

def is_err(result):
	""" Returns true if the given result is a non-zero status code """
	return not is_success(result)

def sh(cmd):
	""" Execute the given shell command (prints stdout/stderr) """
	result = run(cmd, universal_newlines=True, stdout=subprocess.PIPE, shell=True)
	return result

def bsh(cmd):
    """ Execute the given shell command or bail on error (prints stderr) """
    #logging.info("%s"%cmd)
    return sh(cmd)
    """
    # Fix me, need use exception here, return -1 is not a good solution
    if (is_err(result.returncode)):
        return ""
    return result.stdout
    """

def bsh_thread_handler(cmd):
    bsh(cmd)

def bsh_async(cmd):
    """ Execute the given shell command or bail on error (prints stderr) """
    thread = threading.Thread(target=bsh_thread_handler, args=(cmd,))
    return thread

def qsh(cmd):
	""" Quietly execute the given shell command (squelches stdout/stderr) """
	result = run(cmd, stdout=DEVNULL, stderr=DEVNULL, universal_newlines=True)
	return result

def esh(cmd):
	""" Evaluate the given shell command (prints stderr) """
	result = run(cmd, stdout=PIPE, universal_newlines=True)
	return result.returncode or result.stdout.rstrip()

def ebsh(cmd):
	""" Evaluate the given shell command or bail on error (prints stderr) """
	result = esh(cmd)
	if (is_err(result)):
		exit(result)

	return result

def eqsh(cmd):
	""" Quietly evaluate the given shell command (squelches stderr) """
	result = run(cmd, stdout=PIPE, stderr=DEVNULL, universal_newlines=True)
	return result.returncode or result.stdout.rstrip()

def shpath(*paths):
	""" Normalizes and joins one or more path arguments for use in a POSIX shell """
	path = os_path.join(*paths)
	path = os_path.normpath(path)
	return path.replace('\\', '/')
