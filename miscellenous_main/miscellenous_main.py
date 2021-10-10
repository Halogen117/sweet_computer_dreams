import ctypes
import datetime
import os
import subprocess
import json
import requests

class miscellenous_main:
    def __init__(self):
        print('Initializing Miscellenous_main class')
    
    def connect_to_internet():
        '''
        # Replace hardcoded ip address
        if urllib2.urlopen('http://216.58.192.142', timeout=1):
            return True
        else:
            return False
        '''
        try:
            request = requests.get('https://8.8.8.8', timeout=5)
            return True
        except (requests.ConnectionError, requests.Timeout) as exception:
            return False
    # Function that scraps website to get Youtube playlist links
    def getPlaylistLinks(url):
        dict_append = {}
        #command =  'youtube-dl --dump-json https://www.youtube.com/playlist?list=PLy8QXiv7X7KGWy6raCmBTlRC8Vz7V2I2p > "'+os.getcwd()+'\\json.json"'
        #print('youtube-dl -j --flat-playlist '+url+' > "'+os.getcwd()+'\\json.json"')

        # Note change on the 21st Feb 2021, you wanted to try to change the play_video function to add a subtitle file
        #subprocess.run('youtube-dl -j --flat-playlist "'+url+'" > "'+os.getcwd()+'\\json.json"',shell=True)

        subprocess.run('youtube-dl -j --write-sub --sub-lang=en --flat-playlist "'+url+'" > "'+os.getcwd()+'\\json.json"',shell=True)

        with open(os.getcwd()+"\\json.json", "r") as f:
            for count,file_line in enumerate(f.readlines(), start=0):
                load_json = json.loads(file_line)
                dict_append[count] = "https://www.youtube.com/watch?v="+load_json["id"]
                count +=  1
        f.close()
        os.remove(os.getcwd()+"\\json.json")
        if len(dict_append) == 0:
            # Fix this error to Return suitable value
            return False
        else:
            return dict_append

    # Function that convert all time to seconds
    def calculate_to_seconds(args_days,args_hours,args_minutes,args_seconds):
        args_days = args_days or 0
        args_hours = args_hours or 0
        args_minutes = args_minutes or 0
        args_seconds = args_seconds or 0
        return (args_days*3600*24) + (args_hours * 60 + args_minutes) * 60 + args_seconds

    # Function to enhance argument function
    def check_time_no_args(self):
        time_output = input("How long do you want to run the program before allowing the compute to sleep? (seconds)")
        try:
            return int(time_output)
        except ValueError:
            print("Value Error")
            return False

    # Function to find Existance of shutdown file
    def check_shutdown_file():
        print("Checking shutdown program!")
        if os.path.isfile('C:\\Windows\\System32\\shutdown.exe'):
            return True
        else:
            return False

    # Function to check if the function is running in an administrator mode
    def test_admin():
        try:
            is_admin = os.getuid() == 0
        except AttributeError:
            is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0

        return is_admin


    def return_time_to_pause(self,args_days, args_hours, args_seconds, args_set_date, args_set_time):
        if args_set_date or args_set_time is not None:
            return False
        
        if (args_hours and args_seconds and args_days and args_set_time and args_set_date) is None:
            time_to_pause = self.check_time_no_args()
            while time_to_pause is False:
                print("Not an integer! Please enter the time again!") 
                time_to_pause = self.check_time_no_args()
        else:
            time_to_pause = calculate_to_seconds(args_days,args_hours,args_minutes,args_seconds)

        return time_to_pause
    # Calculate the number to return? (Work on it)
    def calculate_playlist_number(self):
        number = 0
        return 