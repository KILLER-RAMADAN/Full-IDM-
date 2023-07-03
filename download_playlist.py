def down_playlist(self):
      try:
        # global home_directory
        Basic_link="https://"
        Not_Basic_Link="https://youtu.be/"
        
        if self.entry_playlist_link.get()=="":
            messagebox.showerror("Empty Field", "Enter Link....")  
            self.pause_and_play.configure(state="disabled")
            self.entry_playlist_link.configure(state="normal") 
                  
        elif Not_Basic_Link  in self.entry_playlist_link.get():
            messagebox.showerror("Error", "This Link Is Youtube Link Make Sure To Put In his Field....")
            self.pause_and_play.configure(state="disabled")
            self.entry_playlist_link.configure(state="normal") 
            
        elif Basic_link  not in self.entry_playlist_link.get():
            messagebox.showerror("Error", "Invalid Link...")
            self.pause_and_play.configure(state="disabled")
            self.entry_playlist_link.configure(state="normal") 
    
        else:
             
             if self.resolutions_playlist_fields.get()=="mp4":
              playlist_info = yt_dlp.YoutubeDL().extract_info(f'{self.entry_playlist_link.get()}', download=False)
              playlist_count = playlist_info.get("playlist_count", None)
              playlist_title = playlist_info.get("title", None)
              self.status.config(text=f"</> Downloading </> Your Playlist Have ({playlist_count}) Video Please Wait.")
              playlist_opts = {
             'format': f'{"bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best"}',
             'outtmpl': f'{self.home_directory}//Desktop//{playlist_title}//{"%(playlist_index)s.%(title)s.%(ext)s"}',
             'playlist': True,
             'quiet': True,
             'no_warnings': True,
             'progress':True,
             'progress_hooks': [self.progress_hook],
             "external_downloader_args": ['-loglevel', 'panic'],
             'video-multistreams ':True,
              }
             
             elif self.resolutions_playlist_fields.get()=="mp3":
              playlist_info = yt_dlp.YoutubeDL().extract_info(f'{self.entry_playlist_link.get()}', download=False)
              playlist_title = playlist_info.get('title', None)
              playlist_count = playlist_info.get("playlist_count", None)
              self.status.config(text=f"</> Downloading </> Your Playlist Have ({playlist_count}) Song Please Wait.")
              playlist_opts = {
             'format': f'{"bestaudio/best[ext=mp3]"}',
             'outtmpl': f'{self.home_directory}//Desktop//{playlist_title}//{"%(playlist_index)s.%(title)s.%(ext)s"}',
             'playlist': True,
             'quiet': True,
             'no_warnings': True,
             'progress':True,
             'progress_hooks': [self.progress_hook],
             "external_downloader_args": ['-loglevel', 'panic'],
             'audio-multistreams ':True,
              }
            
             with yt_dlp.YoutubeDL(playlist_opts) as ydl:
              playlist_info = yt_dlp.YoutubeDL().extract_info(f'{self.entry_playlist_link.get()}', download=False)
              playlist_title = playlist_info.get('title', None)        
              ydl.download([f'{self.entry_playlist_link.get()}']) 
              messagebox.showinfo("Congratulations",f"{playlist_title}\nDownloaded Successfully...")
              self.status.config(text=f"Playlist Successfully Downloading in your Desktop......")
              self.style.configure('text.Horizontal.TProgressbar', text=f'No Download')
              self.progress_bar['value']=0
              self.download_Playlist_button.configure(state="normal")
              self.pause_and_play.configure(state="disabled")
              self.entry_playlist_link.delete(0,1000)
      except:
        messagebox.showerror("Error","maybe some Error founded:\n\n1)check internet connection\n2)Enter Correct File Location\n3)Enter Basic Link that has 'https//'\n4)maybe this sound or video not allowed in your country")
        self.entry_playlist_link.configure(state="normal")  
        self.pause_and_play.configure(state="disabled")