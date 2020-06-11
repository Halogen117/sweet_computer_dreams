from time import sleep
import datetime
import subprocess
import ctypes, os
import time
import keyboard
import threading
# Ensure you add arguments as well! args
import argparse
# For future GUI implementation
import tkinter
# Add argument to play youtube playlist!
import pafy
import vlc
from bs4 import BeautifulSoup
import requests
import random
def getPlaylistLinks(url):
    dict_append = {}
    count = 0
    source_code = requests.get(url).text

    soup = BeautifulSoup(source_code, 'lxml')
    domain = 'https://www.youtube.com'

    for i, tr in enumerate(soup.select('tr.pl-video')):
        #print('{}. {}'.format(i + 1, tr['data-title']))
        #print(domain + tr.a['href'])
        #print('-' * 80)
        dict_append[count] = [domain + tr.a['href'], tr['data-title']]
        count += 1
        
    return dict_append

 




def calculate_to_seconds(args_days,args_hours,args_minutes,args_seconds):
    args_days = args_days or 0
    args_hours = args_hours or 0
    args_minutes = args_minutes or 0
    args_seconds = args_seconds or 0
    return (args_days*3600*24) + (args_hours * 60 + args_minutes) * 60 + args_seconds


def check_time_no_args():
    time_output = input("How long do you want to run the program before allowing the compute to sleep? (seconds)")
    try:
        return int(time_output)
    except ValueError:
        return False

def check_shutdown_file():
    print("Checking shutdown program!")
    if os.path.isfile('C:\\Windows\\System32\\shutdown.exe'):
        return True
    else:
        return False


def test_admin():
    try:
        is_admin = os.getuid() == 0
    except AttributeError:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0

    return is_admin



def main():
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
    args = parser.parse_args()
    args_seconds = args.second_timer
    args_minutes = args.minute_timer
    args_hours = args.hour_timer
    args_days = args.day_timer
    args_playlist_url = args.playlist_url
    if check_shutdown_file is False:
        print("No shutdown file in existance! Exiting Program!")
        exit()
    if test_admin() is False:
        print("It is recommended if you run the program in an administrator mode!")
        exit()

    start_time = datetime.datetime.now()
    if args_hours is None and args_minutes is None and args_seconds is None and args_days is None:
        time_to_pause = check_time_no_args() 
    else:
        time_to_pause = calculate_to_seconds(args_days,args_hours,args_minutes,args_seconds)
    
    end_time = start_time + datetime.timedelta(seconds=time_to_pause)
    

    # Get the dictionary of the playlist
    playlist_dict = getPlaylistLinks(args_playlist_url)

    #Initalize VLC and media player
    Instance = vlc.Instance()
    player = Instance.media_player_new()

    set_print = True

    select_random_url_int = random.randrange(len(playlist_dict))

    video = pafy.new(playlist_dict[select_random_url_int][0])
    best = video.getbest()
    playurl = best.url

    Media = Instance.media_new(playurl)
    Media.get_mrl()
    player.set_media(Media)
    player.play()



    if check_shutdown_file() is True:

        print("The program will end at approximately "+str(end_time))
        while time_to_pause > 0:

            # State.Ended
            if set_print == True:
                print("Now playing "+playlist_dict[select_random_url_int][1])
                print("Composed By :"+video.author)
                set_print = False


            if str(player.get_state()) == "State.Ended":
                print("Switching to the next video!")
                player.stop()
                select_random_url_int = random.randrange(len(playlist_dict))

                video = pafy.new(playlist_dict[select_random_url_int][0])
                best = video.getbest()
                playurl = best.url
                Media = Instance.media_new(playurl)
                Media.get_mrl()
                player.set_media(Media)
                player.play()
                set_print = True

            print("The time remaining is "+ str(time_to_pause)+ " seconds")
            time_to_pause -= 1
            sleep(1)

        print("Turned off!")
        exit()
        subprocess.run('C:\\Windows\\System32\\shutdown.exe -h')

    else:
        print("Unable to shutdown, non existing program!")


main()