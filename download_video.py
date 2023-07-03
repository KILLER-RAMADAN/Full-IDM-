    def download_info_dict(self):# to get all information from your video    #
        global ydl_opts
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio/best',
            'forcejson': True,
            'dump_single_json': True,
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            self.info_dict = ydl.extract_info(self.entry_link.get(), download=False)
            self.get_video_info=self.info_dict.get("title")
        return self.info_dict

    def setup_ydl_opts(self):
        youtube_link="https://youtu.be"
        if youtube_link in self.entry_link.get():
         format = self.ids[self.resolutions_fields.get()]

         return {
            'format': f"{format}+bestaudio",
            'merge_output_format': 'mkv' ,
            'quiet': True,
            'no_warnings': True,
            'progress':True,
            'progress_hooks': [self.progress_hook],
            "external_downloader_args": ['-loglevel', 'panic'],
            'outtmpl': os.path.join(f"{self.entry_path.get()}", '%(title)s.%(ext)s'
            ),
            }
        else:
            self.resolutions_fields.configure(state="disabled")
            # messagebox.showinfo("No Res Found","But you get highest res of the video..")
            return {
            'format': f"bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
            '--rm-cache-dir': True,
             'html5': '1',
             'c': 'TVHTML5',
             'cver': '6.20180913',
            'progress_hooks': [self.progress_hook],
            "external_downloader_args": ['-loglevel', 'panic'],
            'outtmpl': os.path.join(f"{self.entry_path.get()}",'%(title)s.%(ext)s'),
            }
    def download_video(self):
     try:
        # Retrieve the string from the entry fields
        youtube_url = self.entry_link.get()
        Basic_link="https://"
        Not_Basic_Link="/playlist?list"
        # Check if the entry fields are not empty
        if self.entry_link.get()=="":
            messagebox.showerror("Empty Field", "Enter Link....")
            self.download_video_button.configure(state="normal")
        elif Basic_link not in self.entry_link.get():
            messagebox.showerror("Error", "Invalid Link....")
            self.download_video_button.configure(state="normal")
        elif Not_Basic_Link  in self.entry_link.get():
            messagebox.showerror("Error", "This Link Is Playlist Link Make Sure To Put In his Field....")
        elif self.entry_path.get()=="":
            messagebox.showerror("Error", "Enter Location to Save your File...")
            self.download_video_button.configure(state="normal")
        elif self.entry_path.get()=="Enter Location":
            messagebox.showerror("Error", "Enter Location to Save your File...")
            self.download_video_button.configure(state="normal")
        else:
             self.status.configure(text=f" </> Downloading Video Please Wait </>")
             ydl_opts = self.setup_ydl_opts()
            # Download the video
             with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([youtube_url])
                ex=ydl.extract_info(self.entry_link.get(), download=False)
                self.get_info=ex.get("title")
            # Hide progress bar and show download complete message
             messagebox.showinfo(title='Download Complete', message=f' </> downloaded successfully </> {ex.get("title")}\n in "{self.entry_path.get()}" ')
             with youtube_dl.YoutubeDL(ydl_opts) as ydl:
              info_dict = ydl.extract_info(self.entry_link.get(), download=False)
              self.status.configure(text=f" </> Successful Download Video </> {ex.get('title')}")
              self.download_video_button.configure(state="disabled")
              self.resolutions_fields.configure(state="normal")
              self.entry_link.delete(0,1000)
              self.entry_path.delete(0,10000)
              self.style.configure('text.Horizontal.TProgressbar', text=f'No Download')
              self.progress_bar['value']=0
              self.resolutions_fields.delete(0,1000)
              self.pause_and_play.configure(state="disabled") 
     except:
         messagebox.showerror("Error","maybe some Error founded:\n\n1)check internet connection\n2)Enter Correct File Location\n3)Enter Basic Link that has 'https//'4)\nDont Forget to Search About Resolution. ")