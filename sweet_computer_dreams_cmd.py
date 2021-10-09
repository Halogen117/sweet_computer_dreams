# You now face godlike judegement. May it extend eternally

# Ensure you add arguments as well! args
import argparse
from bs4 import BeautifulSoup
import datetime
from pynput import keyboard
import os
# Add argument to play youtube playlist!
import pafy
import random
import requests


from time import sleep
import time
import threading

# External custom classes
from exact_date_time.exact_date_time import exact_date_time
from play_vlc.play_vlc import play_vlc
from miscellenous_main.miscellenous_main import miscellenous_main

# Working Goals :
# Add Spotify and Apple Music support (Issue was that I want it to be a simple login and go for everyone but doesn't seem to support for both for now)
# Add exact time to shutdown instead of a countdown (I can convert the time to the day, hours, minutes and second format) (Added to GUI)
# Find a better way to run powershell commands
# Count how long I watch the videos and calculate which ones I am bound to play the next round?!?!?!!?!? (Deceptively AI but interesting challenge)
# Consider working on a GUI version?
# Debug Debug Debug

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
    
    parser.add_argument('-S', '--seconds', action='store', dest='second_timer',
                    help='Add in how many seconds do you wish the timer starts!', default=None, type=int)
    parser.add_argument('-M', '--minutes', action='store', dest='minute_timer',
                    help='Add in how many minutes do you wish the timer starts!', default=None, type=int)
    parser.add_argument('-H', '--hours', action='store', dest='hour_timer',
                    help='Add in how many hours do you wish the timer starts!', default=None, type=int)           
    parser.add_argument('-D', '--days', action='store', dest='day_timer',
                    help='Add in how many days do you wish the timer starts!', default=None, type=int)
    
    parser.add_argument('--shutdown', action='store',dest='enable_full_shutdown', 
                    help='Enable this option to fully shutdown the computer along with all applications as well',default=None)

    parser.add_argument('--playlist', action='store',dest='playlist_url', 
                    help='Change this argument for you to play a different youtube playlist',default='https://www.youtube.com/playlist?list=PLy8QXiv7X7KFygflzVEYfLB0_p1IhX9S7')

    parser.add_argument('--p', action='store_true',dest='player_off',
                    help='Set this option to turn on the video player with the vlc option')   

    parser.add_argument('--p-c', action='store_false',dest='player_off',
                    help='Set this option to turn off the video player with the vlc option')

    parser.add_argument('-d','--descending', action='store_true',dest='descending',
                    help='Set this option to play the playlist through descending order. Eg : 1 -> 2-> 3') 

    parser.add_argument('-a', '--ascending', action='store_true',dest='ascending', 
                    help='Set this option to play the playlist through Ascending order. Eg : 3 -> 2-> 1')   

    parser.add_argument('--st', action='store', dest='set_time', help='Input the exact time you want the program to shutdown!', default= None, type=str)
    # Exact Date
    parser.add_argument('--sd', action='store', dest='set_date', help='Input the exact date you want the program to shutdown!', default=None, type=str)

    args = parser.parse_args()
    
    args_seconds = args.second_timer
    args_minutes = args.minute_timer
    args_hours = args.hour_timer
    args_days = args.day_timer
    args_playlist_url = args.playlist_url
    args_player_off = args.player_off
    if 'https://www.youtube.com' not in args_playlist_url:
        print("Invalid Youtube Link! The VLC Player will automatically be disabled")
        args_player_off = False

    if miscellenous_main.connect_to_internet() is False:
        print("No internet connection... The vlc player will automatically be disabled")
        args_player_off = False
    
    args_descending = args.descending
    args_ascending = args.ascending

    args_set_time = args.set_time
    args_set_date = args.set_date

    if args_set_date and args_set_time is not None:
        exact_date_time_class = exact_date_time(args_set_date, args_set_time)
    
        exact_date_time_class.analyze_time_format()
    #exact_date_time_class.different_time_format()
    
    if args_ascending and args_descending is True:
        print("Youtube is unable to play soundtracks both ascending or descending simultaneously (obviously). Playing the tracks randomly... ")
 
    if miscellenous_main.check_shutdown_file() is False:
        print("No shutdown file in existance! Exiting Program!")
        exit()


    if miscellenous_main.test_admin() is False:
        print("It is recommended if you run the program in an administrator mode!")
        exit()


    start_time = datetime.datetime.now()
    if args_hours is None and args_minutes is None and args_seconds is None and args_days is None:
        time_to_pause = miscellenous_main.check_time_no_args()
        while time_to_pause is False:
            print("Not an integer! Please enter the time again!") 
            time_to_pause = check_time_no_args.check_time_no_args()
            
    else:
        time_to_pause = miscellenous_main.calculate_to_seconds(args_days,args_hours,args_minutes,args_seconds)

    end_time = start_time + datetime.timedelta(seconds=time_to_pause)

    if args_player_off is True:
        # Get the dictionary of the playlist
        playlist_dict = miscellenous_main.getPlaylistLinks(args_playlist_url)
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
        custom_vlc_class.play_video(video.getbest().url,"GVK_Test.vtt")
        video_list_number.append(select_random_url_int)

    if miscellenous_main.check_shutdown_file() is True:

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
                            custom_vlc_class.play_video(video.getbest().url,"GVK_Test.vtt")
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
                            custom_vlc_class.play_video(video.getbest().url,"GVK_Test.vtt")
                            video_list_number.append(select_random_url_int)
                            set_print = True
                            next_video = False
                        except:
                            select_random_url_int = select_random_url_int+1 if (args_ascending is True and args_descending is False) else select_random_url_int - 1 if (args_ascending is False and args_descending is True) else random.randrange(len(playlist_dict))
                            video = pafy.new(playlist_dict[select_random_url_int])
                            custom_vlc_class.play_video(video.getbest().url,"GVK_Test.vtt")
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
                            custom_vlc_class.play_video(video.getbest().url,"GVK_Test.vtt")
                            previous_video = False
                        except:
                            select_random_url_int = select_random_url_int+1 if (args_ascending is True and args_descending is False) else select_random_url_int - 1 if (args_ascending is False and args_descending is True) else random.randrange(len(playlist_dict))
                            video = pafy.new(playlist_dict[select_random_url_int])
                            custom_vlc_class.play_video(video.getbest().url,"GVK_Test.vtt")
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
        print("Unable to shutdown, non existing shutdown program!")


main()