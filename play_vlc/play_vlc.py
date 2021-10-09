import vlc
class play_vlc:
    def __init__(self,youtube_playlist):
        self.youtube_playlist = youtube_playlist 
        self.vlc_instance = vlc.Instance()
        self.media_player = self.vlc_instance.media_player_new()
    
    def play_video(self,url_link,subtitle_file):
        Media = self.vlc_instance.media_new(url_link)
        Media.get_mrl() 
        self.media_player.set_media(Media)


        #subtitles = self.media_player.add_slave(self.media_player,subtitle_file, True)


        self.media_player.play()

    def get_state_player(self):
        return self.media_player.get_state()

    def pause_player(self):
        self.media_player.pause()
    
    def start_player(self):
        self.media_player.play()
    
    def stop_player(self):
        self.media_player.stop()