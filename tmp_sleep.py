from time import sleep
import subprocess
import ctypes, os
def test_admin():
    
    try:
        is_admin = os.getuid() == 0
    except AttributeError:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0

    return is_admin


if test_admin() is not True:
    print("It is recommended if you run the program in an administrator mode!")
    exit()

get_time = input("How long do you want to run the program before allowing the compute to sleep? (seconds)")

sleep(int(get_time))
subprocess.run('C:\Windows\System32\shutdown.exe -h')
