import sys
import platform


def check_os():
    err_msg = 'This system is not Windows 10. Exit.'
    if sys.platform != 'win32':
        print(err_msg)
        exit()
    if platform.release() != '10':
        print(err_msg)
        exit()
