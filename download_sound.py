def down_sound(self):
            URLS =f'{self.entry_link.get()}'
            info_dict = yt_dlp.YoutubeDL().extract_info(url=self.entry_link.get(), download=False)
            self.get_sound_information=info_dict.get("title")
            self.status.configure(text=f" </> Downloading  Sound Please Wait </> {self.get_sound_information}")
            sound_format=self.resolutions_song_fields.get().replace("kbps","")
            ydl_opts1 = {
             'format': 'bestaudio/best',
             'quiet': True,
             'no_warnings': True,
             'progress':True,
             'progress_hooks': [self.progress_hook],
             "external_downloader_args": ['-loglevel', 'panic'],
             'postprocessors': [{
             'key': 'FFmpegExtractAudio',
             'preferredcodec': 'mp3',
             'preferredquality': f'{sound_format}',
               }],
              'outtmpl':os.path.join(f"{self.entry_path.get()}","%(title)s.%(ext)s"),
               } 
            with yt_dlp.YoutubeDL(ydl_opts1) as ydl:
               download_sound = ydl.download(self.entry_link.get())
               messagebox.showinfo("Congratulations",f" </> Sound Downloaded Successfully </> {self.get_sound_information}")
               self.status.configure(text=f" </> Successful Download Sound </> {self.get_sound_information}")
               self.download_Sound_button.configure(state="normal")
               self.style.configure('text.Horizontal.TProgressbar', text=f'No Download')
               self.progress_bar['value']=0
               self.download_Playlist_button.configure(state="normal")
               self.entry_link.delete(0,1000)
               self.entry_path.delete(0,10000)
               self.pause_and_play.configure(state="disabled") 