# Ensure you add arguments as well! args
import argparse
from bs4 import BeautifulSoup
import datetime
import ctypes
import json
from pynput import keyboard
import os
# Add argument to play youtube playlist!
import pafy
import random
import requests
import subprocess
from time import sleep
import time
import threading
# For future GUI implementation
import tkinter
import vlc

class play_vlc:
    def __init__(self,youtube_playlist):
        self.youtube_playlist = youtube_playlist 
        self.vlc_instance = vlc.Instance()
        self.media_player = self.vlc_instance.media_player_new()
    
    def play_video(self,url_link):
        Media = self.vlc_instance.media_new(url_link)
        Media.get_mrl()
        self.media_player.set_media(Media)
        self.media_player.play()

    def get_state_player(self):
        return self.media_player.get_state()
    
    def pause_player(self):
        self.media_player.pause()
    
    def start_player(self):
        self.media_player.play()
    
    def stop_player(self):
        self.media_player.stop()

def on_press(key):
    global next_video
    global previous_video
    global repeat_pause
    print (key)
    if key == keyboard.Key.right:
        print ('Right Key Pressed!')
        next_video = True
    elif key == keyboard.Key.left:
        print("Left Key Pressed")
        previous_video = True
        return False
    elif key == keyboard.Key.enter:
        if repeat_pause == 0:
            print("Initialized!")
            repeat_pause = 1
        elif repeat_pause == 1:
            repeat_pause = 2
        else:
            repeat_pause = 1
        print('Paused pressed!')

# Function that scraps website to get Youtube playlist links
def getPlaylistLinks(url):
    dict_append = {}
    #command =  'youtube-dl --dump-json https://www.youtube.com/playlist?list=PLy8QXiv7X7KGWy6raCmBTlRC8Vz7V2I2p > "'+os.getcwd()+'\\json.json"'
    #print('youtube-dl -j --flat-playlist '+url+' > "'+os.getcwd()+'\\json.json"')
    subprocess.run('youtube-dl -j --flat-playlist "'+url+'" > "'+os.getcwd()+'\\json.json"',shell=True)

    with open(os.getcwd()+"\\json.json", "r") as f:
        for count,file_line in enumerate(f.readlines(), start=0):
            load_json = json.loads(file_line)
            dict_append[count] = "https://www.youtube.com/watch?v="+load_json["id"]
            count +=  1
    f.close()
    os.remove(os.getcwd()+"\\json.json")
    if len(dict_append) == 0:
        return {1:'https://www.youtube.com/watch?v=xf9ZtTC2aHw'}
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
def check_time_no_args():
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


def main():
    global next_video
    global previous_video
    global repeat_pause
    
    previous_video = False
    stop_pausing = True
    repeat_pause = 0
    next_video = False
    video_list_number = []

    parser = argparse.ArgumentParser(description='Welcome to the sweet_computer_dreams program! Have fun getting your computer to sleep in style!')
    
    parser.add_argument('-S', action='store', dest='second_timer',
                    help='Add in how many seconds do you wish the timer starts!', default=None, type=int)
    parser.add_argument('-M', action='store', dest='minute_timer',
                    help='Add in how many minutes do you wish the timer starts!', default=None, type=int)
    parser.add_argument('-H', action='store', dest='hour_timer',
                    help='Add in how many hours do you wish the timer starts!', default=None, type=int)           
    parser.add_argument('-D', action='store', dest='day_timer',
                    help='Add in how many days do you wish the timer starts!', default=None, type=int)
    
    parser.add_argument('-e', action='store',dest='enable_full_shutdown', 
                    help='Enable this option to fully shutdown the computer along with all applications as well',default=None)

    parser.add_argument('-v', action='store',dest='playlist_url', 
                    help='Change this argument for you to play a differetn youtube playlist',default='https://www.youtube.com/playlist?list=PLy8QXiv7X7KFygflzVEYfLB0_p1IhX9S7')

    parser.add_argument('--p', action='store_true',dest='player_off',
                    help='Set this option to turn on the video player with the vlc option')   

    parser.add_argument('--p-c', action='store_false',dest='player_off',
                    help='Set this option to turn off the video player with the vlc option')

    # New Orders that came from starfleet
    parser.add_argument('--d', action='store_true',dest='descending',
                    help='Set this option to play the playlist through descending order. Eg : 1 -> 2-> 3') 

    parser.add_argument('--a', action='store_true',dest='ascending',
                    help='Set this option to play the playlist through Ascending order. Eg : 3 -> 2-> 1')   


    args = parser.parse_args()
    args_seconds = args.second_timer
    args_minutes = args.minute_timer
    args_hours = args.hour_timer
    args_days = args.day_timer
    args_playlist_url = args.playlist_url
    args_player_off = args.player_off
    
    args_descending = args.descending
    args_ascending = args.ascending

    if check_shutdown_file is False:
        print("No shutdown file in existance! Exiting Program!")
        exit()
    """
    if test_admin() is False:
        print("It is recommended if you run the program in an administrator mode!")
        exit()
    """

    start_time = datetime.datetime.now()
    if args_hours is None and args_minutes is None and args_seconds is None and args_days is None:
        time_to_pause = check_time_no_args()
        while time_to_pause is False:
            print("Not an integer! Please enter the time again!") 
            time_to_pause = check_time_no_args()
            
    else:
        time_to_pause = calculate_to_seconds(args_days,args_hours,args_minutes,args_seconds)

    end_time = start_time + datetime.timedelta(seconds=time_to_pause)

    if args_player_off is True:
        # Get the dictionary of the playlist
        playlist_dict = getPlaylistLinks(args_playlist_url)
        #Initalize VLC and media player
        custom_vlc_class =  play_vlc(playlist_dict)
        set_print = True

        select_random_url_int = 0 if (args_ascending is True and args_descending is False) else len(playlist_dict)-1 if (args_ascending is False and args_descending is True) else random.randrange(len(playlist_dict))

        try:
            video = pafy.new(playlist_dict[select_random_url_int])
        except (KeyError, OSError) as e:
            print(e)
            print("This could be due to the playlist being set to private or a deleted video!")
            exit()
        custom_vlc_class.play_video(video.getbest().url)
        video_list_number.append(select_random_url_int)

    if check_shutdown_file() is True:

        print("The program will end at approximately "+str(end_time))

        if args_player_off is True:
            while time_to_pause > 0:
                with keyboard.Listener(on_press=on_press) as listener:
                    # State.Ended
                    if set_print == True:
                        print("Now playing "+playlist_dict[select_random_url_int])
                        print("Composed By :"+video.author)
                        set_print = False

                    if str(custom_vlc_class.get_state_player()) == "State.Ended":
                        print("Switching to the next video!")
                        custom_vlc_class.stop_player()

                        # Error Exception to play next video
                        try:
                            # Ensure code goes back to number after reaches first and last number of code
                            select_random_url_int = select_random_url_int+1 if (args_ascending is True and args_descending is False) else select_random_url_int - 1 if (args_ascending is False and args_descending is True) else random.randrange(len(playlist_dict))
                            video = pafy.new(playlist_dict[select_random_url_int])
                            custom_vlc_class.play_video(video.getbest().url)
                            video_list_number.append(select_random_url_int)
                            set_print = True
                        except:
                            pass

                    if next_video is True:
                        print("Advancing to next video!")
                        custom_vlc_class.stop_player()
                        try:
                            select_random_url_int = select_random_url_int+1 if (args_ascending is True and args_descending is False) else select_random_url_int - 1 if (args_ascending is False and args_descending is True) else random.randrange(len(playlist_dict))
                            video = pafy.new(playlist_dict[select_random_url_int])
                            custom_vlc_class.play_video(video.getbest().url)
                            video_list_number.append(select_random_url_int)
                            set_print = True
                            next_video = False
                        except:
                            select_random_url_int = select_random_url_int+1 if (args_ascending is True and args_descending is False) else select_random_url_int - 1 if (args_ascending is False and args_descending is True) else random.randrange(len(playlist_dict))
                            video = pafy.new(playlist_dict[select_random_url_int])
                            custom_vlc_class.play_video(video.getbest().url)
                            video_list_number.append(select_random_url_int)

                    print(custom_vlc_class.get_state_player())
                    if previous_video is True:
                        print("Replaying previous video!")
                        custom_vlc_class.stop_player()
                        try:
                            if len(video_list_number) > 1:
                                video = pafy.new(playlist_dict[video_list_number[-2]])
                                video_list_number.remove(video_list_number[-1])
                            else:
                                video = pafy.new(playlist_dict[select_random_url_int])
                                video_list_number.append(select_random_url_int)
                            custom_vlc_class.play_video(video.getbest().url)
                            previous_video = False
                        except:
                            select_random_url_int = select_random_url_int+1 if (args_ascending is True and args_descending is False) else select_random_url_int - 1 if (args_ascending is False and args_descending is True) else random.randrange(len(playlist_dict))
                            video = pafy.new(playlist_dict[select_random_url_int])
                            custom_vlc_class.play_video(video.getbest().url)
                            video_list_number.append(select_random_url_int)

                    # The one is always running
                    if repeat_pause == 1 and stop_pausing == True:
                        print("Pausing Video!")
                        custom_vlc_class.pause_player()
                        stop_pausing  = False
                    elif repeat_pause == 2:
                        custom_vlc_class.start_player()
                        stop_pausing = True
                        
                    print(video_list_number)
                    print("The time remaining is "+ str(time_to_pause)+ " seconds")
                    time_to_pause -= 1
                    sleep(1)
                    
                listener.join()

        else:
            while time_to_pause > 0:
                print("The time remaining is "+ str(time_to_pause)+ " seconds without the player!")
                time_to_pause -= 1
                sleep(1)

        print("Turned off!")
        subprocess.run('C:\\Windows\\System32\\shutdown.exe -h')
    else:
        print("Unable to shutdown, non existing program!")


main()