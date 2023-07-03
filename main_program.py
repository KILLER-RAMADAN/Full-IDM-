import tkinter as tk
import sys
from tkinter import ttk, messagebox ,filedialog
from tkinter.ttk import *
import webbrowser
import threading
import yt_dlp as youtube_dl
import re
import os
import yt_dlp
import webbrowser
import tkinter.font as font
import install_laibrary
install_laibrary.install()
class video_downloader(tk.Tk):
    #___________________________________get res from youtube video_______________________#
    def get_unique_resolutions(self, inf_dict):
       youtube_link="https://youtu.be" 
       short_link="https://youtube.com/shorts/" 
       if youtube_link in self.entry_link.get() or short_link in self.entry_link.get():  
        resolutions = {}
        for format in inf_dict['formats']:
            if re.match(r'^\d+p', format["format_note"]):
                resolution_id = format['format_id']
                resolution = format["format_note"]
                if 'HDR' in resolution:
                    resolution = re.search(r'\d+p\d* HDR', resolution)[0]
                resolutions[resolution ] =resolution_id
                
        resolutions = [(v, k) for k, v in resolutions.items()]
        return sorted(resolutions, key=lambda k: [int(k[1].split('p')[0]), k[1].split('p')[-1]])
       else:
           return ""
    #___________________________________get res from youtube video_______________________#
    
    #___________________________________Enter res in compobox_______________________#
    def create_resolutions_dropdown(self, info_dict):
        resolutions = self.get_unique_resolutions(info_dict)
        self.resolutions_fields['values'] = [res[1] for res in resolutions]
        self.ids = {res[1]: res[0] for res in resolutions}
        self.resolutions_fields.current(0)
    #___________________________________Enter res in compobox_______________________#  
    
    
    #___________________________________progress_bar_downloading_______________________#
    def progress_hook(self , data):
        if data['status'] == 'downloading':
            downloaded = data['downloaded_bytes']

            total = data['total_bytes']  if data.get('total_bytes' ,None) else data['total_bytes_estimate']
            self.percentage = downloaded / total * 100
            self.percentage = round(self.percentage,2)
           
            self.progress_bar["value"] =  self.percentage
            self.progress_bar.update()
            
            self.style.configure('text.Horizontal.TProgressbar', text=f'%{self.percentage}')
            
                    
    #___________________________________progress_bar_downloading_______________________#
    
    #___________________________________We Call This Function When Press On (search res)_______________________#        
    def get_ready(self):
        Basic_link="https://"
        Not_Basic_Link="/playlist?list"
        youtube_link="https://youtu.be/"
        # Check if the entry fields are not empty
        if self.entry_link.get()=="":
            messagebox.showerror("Empty Field", "Enter Link....")
        elif Basic_link not in self.entry_link.get():
            messagebox.showerror("Error", "Invalid Link....")
        elif Not_Basic_Link  in self.entry_link.get():
            messagebox.showerror("Error", "This Link Is Playlist Link Make Sure To Put In his Field....")
        
        else:
            if youtube_link in self.entry_link.get():
             youtube_link in self.entry_link.get()
             self.download_video_button.configure(state="normal")
             info_dict = self.download_info_dict()
             self.create_resolutions_dropdown(info_dict)
            else:
                messagebox.showinfo("No Res Found","No Resolution Found For This Video")
                self.download_video_button.configure(state="normal")
                self.resolutions_fields.configure(state="disabled")
                return ""
    #___________________________________We Call This Function When Press On (search res)_______________________#  
##################
##########  
#####   
#_____________________download video_____________________#
    def download_info_dict(self):# to get all information from your video    #
        global ydl_opts
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio/best',
            'forcejson': True,
            'dump_single_json': True,
            "--geo-verification-proxy URL":True,
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
            "--no-playlist":True,
            "--geo-verification-proxy URL":True,
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
             "--no-playlist":True,
             "--ignore-no-formats-error ":True,
            'progress_hooks': [self.progress_hook],
            "--geo-verification-proxy URL":True,
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
         messagebox.showerror("Error","maybe some error founded:\n\n1)check internet connection\n2)enter correct file location\n3)enter basic link that has 'https//'\n4)maybe this sound or video not allowed in your country\n5)close program while downloading")
#_____________________download video_____________________#   
##################
##########  
#####   
#_____________________download Sound_____________________#   

    def down_sound(self):
         try:
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
             "--no-playlist":True,
             '--geo-verification-proxy URL':True,
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
         except:
          messagebox.showerror("Error","maybe some error founded:\n\n1)check internet connection\n2)enter correct file location\n3)enter basic link that has 'https//'\n4)maybe this sound or video not allowed in your country\n5)close program while downloading")
#_____________________download video_____________________#   
##################
##########  
#####   
#_____________________download Playlist_____________________#
    def down_playlist(self):
      try:
        # global home_directory
        Basic_link="https://"
        Not_Basic_Link="https://youtu.be/"
        
        if self.entry_playlist_link.get()=="":
            messagebox.showerror("Empty Field", "Enter Link....")  
            self.pause_and_play.configure(state="disabled")
            self.entry_playlist_link.configure(state="normal")
            self.download_Playlist_button.configure(state="normal") 
                  
        elif Not_Basic_Link  in self.entry_playlist_link.get():
            messagebox.showerror("Error", "This Link Is Youtube Link Make Sure To Put In his Field....")
            self.pause_and_play.configure(state="disabled")
            self.entry_playlist_link.configure(state="normal") 
            self.download_Playlist_button.configure(state="normal")
            
        elif Basic_link  not in self.entry_playlist_link.get():
            messagebox.showerror("Error", "Invalid Link...")
            self.pause_and_play.configure(state="disabled")
            self.entry_playlist_link.configure(state="normal")
            self.download_Playlist_button.configure(state="normal") 
    
        else:
             
             if self.resolutions_playlist_fields.get()=="mp4":
              playlist_info = yt_dlp.YoutubeDL().extract_info(f'{self.entry_playlist_link.get()}', download=False)
              playlist_count = playlist_info.get("playlist_count", None)
              playlist_title = playlist_info.get("title", None)
              self.status.config(text=f"</> Downloading </> Your Playlist ({playlist_title}) have ({playlist_count}) Videos Please Wait.")
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
              self.status.config(text=f"</> Downloading </> Your Playlist ({playlist_title})  have ({playlist_count}) Songs Please Wait.")
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
        messagebox.showerror("Error","maybe some error founded:\n\n1)check internet connection\n2)enter correct file location\n3)enter basic link that has 'https//'\n4)maybe this sound or video not allowed in your country\n5)close program while downloading")
        self.entry_playlist_link.configure(state="normal")  
        self.pause_and_play.configure(state="disabled")
#_____________________download Playlist_____________________#         
##################
##########  
#####   
#___________________________________all functions___________________________#
    def link_enter(self,e):
      self.entry_link.delete(0,"end")
    def link_leave(self,e):
        if self.get_link and self.entry_link.get()=="":
            self.entry_link.insert(0,self.get_link)
            self.status.configure(text="Link has been Pasted From Clipboard")
        else:
            return ""
        
    
    def link_playlist_enter(self,e):
      self.entry_playlist_link.delete(0,"end")
    def link_playlist_leave(self,e):
        if self.get_link and self.entry_playlist_link.get()=="":
            self.entry_playlist_link.insert(0,self.get_link)
            self.status.configure(text="Link has been Pasted From Clipboard")
        else:
            return ""
     
        
        
    def pass_enter(self,e):
      self.entry_path.delete(0,"end")
    def pass_leave(self,e):
     if self.entry_path.get()=="":
        self.entry_path.insert(0,"Enter Location")
    
    def search_res(self):
      self.get_ready()
      
      
      
    ## get video info ##
    def browse(self):
      self.entry_path.delete(0,10000)
      self.raed_file=filedialog.askdirectory(title="Select Path")
      self.entry_path.insert(0,self.raed_file)
    
      
      
      
      
    def thread_video(self):
     try:
      thre1=threading.Thread(target=self.download_video)
      thre1.start()
      self.download_video_button.configure(state="disabled")
      self.pause_and_play.configure(state="normal")
     except:
        messagebox.showerror("Error","maybe some error founded:\n\n1)check internet connection\n2)enter correct file location\n3)enter basic link that has 'https//'\n4)maybe this sound or video not allowed in your country\n5)close program while downloading")
      
      
    def thread_Playlist(self):
     try:
       thre2=threading.Thread(target=self.down_playlist)
       thre2.start()
       self.pause_and_play.configure(state="normal")
       self.download_Playlist_button.configure(state="disabled")
     except:
        messagebox.showerror("Error","maybe some error founded:\n\n1)check internet connection\n2)enter correct file location\n3)enter basic link that has 'https//'\n4)maybe this sound or video not allowed in your country\n5)close program while downloading")
      
         
     
      
      
    def thread_sound(self):
      try:
        Basic_link="https://"
        Not_Basic_Link="https://youtube.com/playlist"
        sound_cloud_playlist="https://soundcloud.com/soundcloud/sets/"
        if self.entry_link.get()=="":
            messagebox.showerror("Empty Field", "Enter Link....") 
            self.download_Sound_button.configure(state="normal")
        elif Basic_link not in self.entry_link.get():
            messagebox.showerror("Error", "Invalid Link....")
            self.download_Sound_button.configure(state="normal")
        elif self.entry_path.get()=="":
            messagebox.showerror("Error", "Enter Location to Save your File...")
            self.download_Sound_button.configure(state="normal")
        elif self.entry_path.get()=="Enter Location":
            messagebox.showerror("Error", "Enter Location to Save your File...")
            self.download_Sound_button.configure(state="normal")
        elif self.resolutions_song_fields.get()=="":
            messagebox.showerror("Empty Field", "Enter bitrate ..")
            self.download_Sound_button.configure(state="normal")
        elif sound_cloud_playlist  in self.entry_link.get():
            messagebox.showerror("Error", "This Link Is sound Cloud 'Playlist' Link Make Sure To Put In his Field....")
            self.download_Sound_button.configure(state="normal")
        elif Not_Basic_Link  in self.entry_link.get():
            messagebox.showerror("Error", "This Link Is Playlist Link Make Sure To Put In his Field....")
            self.download_Sound_button.configure(state="normal")
        else: 
         if self.progress_bar:
          thre3=threading.Thread(target=self.down_sound)
          thre3.start()
          self.download_Sound_button.configure(state="disabled")
          self.pause_and_play.configure(state="normal") 
      except:
          messagebox.showerror("Error","maybe some error founded:\n\n1)check internet connection\n2)enter correct file location\n3)enter basic link that has 'https//'\n4)maybe this sound or video not allowed in your country\n5)close program while downloading")
      
    
     ## Contact With Develober ##
    def git(self):
      webbrowser.open("https://github.com/KILLER-RAMADAN")
    
    def linkedin(self):
      webbrowser.open("https://www.linkedin.com/in/ahmed-ramadan-9b5a32221/")
      
    def gmail(self):
      webbrowser.open("https://mail.proton.me/u/0/inbox")
     
     
    ## Contact With Develober ##
     
    def exit_full_program(self):
        self.ask_user=messagebox.askquestion("Exit","do you want to exit!?")
        if self.ask_user=="no":
            return ""
        else:
         self.destroy()
         sys.exit()
     
    def stop_download(self):
     try:
      self.ask_download=messagebox.askquestion("Download","do you want to stop Downloading !?")
      if self.ask_download=="no":
         return ""
      else:
       self.update()   
       self.progress_bar['value']=0
       self.style.configure('text.Horizontal.TProgressbar', text=f'No Download')
       self.progress_bar.update()
       self.home_window()
     except Exception:
         messagebox.showerror("Error","maybe some Error founded:\ncheck internet connection\nEnter Correct File Location\nEnter Basic Link that has 'https//'\nThe video may be private ")
          
     
     
     
     
    def show_site(self):
      if self.entry_link.get()=="":
       messagebox.showerror("Error","Enter Link to Open in browser")
      else:
       self.open_wep=webbrowser.open_new_tab(self.entry_link.get())
    
    
    def pause(self):
        if not self.pause_download:
            self.pause_download=True
            self.pause_and_play.configure(image=self.img11)
        else:
            self.pause_download=False
            self.pause_and_play.configure(image=self.img10)
            
            
       
    
    
    def home_window(self):
      self.update()
      self.frame_window1=tk.Frame(self,bg="#353235",width=1500,height=750)
      self.frame_window1.place(x=260,y=50)
      self.title_lb.configure(text="Home Page")
      self.title("Home")
      self.entry_link=ttk.Entry(self.frame_window1,width=64,font=("arial",20),background="#353235",foreground="black")
      self.entry_link.place(x=160,y=350)
      try:
       self.get_link=self.clipboard_get()
       if self.get_link:
        self.entry_link.insert(0,self.get_link)
       else:
          return ""
      except:
          messagebox.showinfo("Copy Link ","Copy any Link and Paste in His Feild ")
      self.entry_link.bind("<FocusIn>",self.link_enter)
      self.entry_link.bind("<FocusOut>",self.link_leave)
      self.status.configure(text="</> Home Page </>")
      self.contact_gmail_button=tk.Button(self.frame_window1,text="Gmail",bg="#4a474a",command=self.gmail,bd=0,image=self.img8,compound="left",activebackground="#4a474a",fg="white",relief="flat",font=("arial",16))   
      self.contact_gmail_button.place(x=420,y=590)
      self.contact_git_button=tk.Button(self.frame_window1,text="Github",bg="#4a474a",command=self.git,bd=0,image=self.img7,compound="left",activebackground="#4a474a",fg="white",relief="flat",font=("arial",16))   
      self.contact_git_button.place(x=530,y=590)
      self.contact_linkedin_button=tk.Button(self.frame_window1,text="Linkedin",bg="#4a474a",command=self.linkedin,bd=0,image=self.img9,compound="left",activebackground="#4a474a",fg="white",relief="flat",font=("arial",16))   
      self.contact_linkedin_button.place(x=650,y=590)
      self.open_prowse_button=tk.Button(self.frame_window1,width=80,text="GO",command=self.show_site,bg="#4a474a",bd=0,activebackground="#4a474a",fg="white",relief="flat",font=("arial",16))   
      self.open_prowse_button.place(x=160,y=450)
      self.open_prowse_button.configure(text="GO")
      self.info_of_download_lablel=tk.Label(self.frame_window1,text="Enter the URL of the Website you want to load:",font=("arial",20),bg="#353235",fg="white")
      self.info_of_download_lablel.place(x=160,y=200)
      self.downloader_lablel=tk.Label(self.frame_window1,text="Downloader",image=self.img6,compound="right",font=("Roboto Slab",30),bg="#353235",fg="white")
      self.downloader_lablel.place(x=160,y=100)
      self.min_logo_lablel=tk.Label(self.frame_window1,image=self.img16,compound="right",font=("Roboto Slab",30),bg="#353235",fg="white")
      self.min_logo_lablel.place(x=730,y=70)
      self.configure(background='#353235')
      self.mainloop()
      
    
    def download_veideo(self):
     self.update()
     self.frame_window2=tk.Frame(self,bg="#353235",width=1500,height=750)
     self.frame_window2.place(x=260,y=50)
     self.title_lb.configure(text="Video Page")
     self.title("Download Video")
     self.entry_link=ttk.Entry(self.frame_window2,width=64,font=("arial",20),background="#353235",foreground="black")
     self.entry_link.place(x=160,y=250)
     self.get_link=self.clipboard_get()
     try:
       self.get_link=self.clipboard_get()
       if self.get_link:
        self.entry_link.insert(0,self.get_link)
       else:
          return ""
     except:
          messagebox.showinfo("Copy Link ","Copy any Link and Paste in His Feild ")
     self.entry_link.bind("<FocusIn>",self.link_enter)
     self.entry_link.bind("<FocusOut>",self.link_leave) 
     self.status.configure(text="</> Video Page </>")
     self.entry_path=ttk.Entry(self.frame_window2,width=64,font=("arial",20),background="#353235",foreground="black")
     self.entry_path.place(x=160,y=350)
     self.entry_path.insert(0,"Enter Location")
     self.entry_path.bind("<FocusIn>",self.pass_enter)
     self.entry_path.bind("<FocusOut>",self.pass_leave)
     self.resolutions_fields = ttk.Combobox(self.frame_window2,state= "readonly", width = 10, font = ("verdana", "8"))
     self.resolutions_fields.place(x=160,y=435)
     self.choose_format_label_text=tk.Label(self.frame_window2,text="Select Video Resolution",font=("arial",10),fg="white",bg="#4a474a")
     self.choose_format_label_text.place_configure(x=160,y=400)
     self.configure(background='#353235')
     self.download_video_button=tk.Button(self.frame_window2,width=80,text="Download Video",command=self.thread_video,bg="#4a474a",bd=0,activebackground="#4a474a",fg="white",relief="flat",font=("arial",16))   
     self.download_video_button.place(x=160,y=470)
     self.download_video_button.configure(state="disabled")
     self.download_video_button.configure(text="Download Video")
     self.info_of_download_lablel=tk.Label(self.frame_window2,text="Enter the URL of the Website you want to load:",font=("arial",20),bg="#353235",fg="white")
     self.info_of_download_lablel.place(x=160,y=200)
     self.downloader_lablel=tk.Label(self.frame_window2,text="Downloader",image=self.img6,compound="right",font=("Roboto Slab",30),bg="#353235",fg="white")
     self.downloader_lablel.place(x=160,y=100)
     self.downloader_lablel=tk.Label(self.frame_window2,text="Downloader",image=self.img6,compound="right",font=("Roboto Slab",30),bg="#353235",fg="white")
     self.downloader_lablel.place(x=160,y=100)
     self.downloader_lablel=tk.Label(self.frame_window2,text="Location:",compound="right",font=("Roboto Slab",20),bg="#353235",fg="white")
     self.downloader_lablel.place(x=160,y=300)
     self.Searche_res_button=tk.Button(self.frame_window2,width=10,text="Search res",command=self.search_res,bg="#4a474a",bd=0,activebackground="#4a474a",fg="white",relief="flat",font=("arial",16))   
     self.Searche_res_button.place(x=1130,y=470)
     self.select_Path_button=tk.Button(self.frame_window2,width=0,text="Select Path",command=self.browse,bg="#4a474a",bd=0,activebackground="#4a474a",fg="white",relief="flat",font=("arial",16))   
     self.select_Path_button.place(x=1130,y=350)
     self.contact_gmail_button=tk.Button(self.frame_window2,text="Gmail",bg="#4a474a",command=self.gmail,bd=0,image=self.img8,compound="left",activebackground="#4a474a",fg="white",relief="flat",font=("arial",16))   
     self.contact_gmail_button.place(x=420,y=610)
     self.contact_git_button=tk.Button(self.frame_window2,text="Github",bg="#4a474a",command=self.git,bd=0,image=self.img7,compound="left",activebackground="#4a474a",fg="white",relief="flat",font=("arial",16))   
     self.contact_git_button.place(x=530,y=610)
     self.contact_linkedin_button=tk.Button(self.frame_window2,text="Linkedin",bg="#4a474a",command=self.linkedin,bd=0,image=self.img9,compound="left",activebackground="#4a474a",fg="white",relief="flat",font=("arial",16))   
     self.contact_linkedin_button.place(x=650,y=610)
     self.info_of_download_lablel.configure(text="Enter the URL of the Video:")
     self.download_label_text=tk.Label(self.frame_window2,text="Downloading",font=("arial",10),fg="white",bg="#4a474a")
     self.download_label_text.place_configure(x=160,y=520)
     self.progress_bar = ttk.Progressbar( self.frame_window2,orient = tk.HORIZONTAL, style='text.Horizontal.TProgressbar',
                length = 250, mode = 'determinate')
     self.progress_bar.place_configure(x=160,y=560)           
     self.pause_and_play=tk.Button(self.frame_window2,bd=0,compound="left",font=("arial",20),bg="#353235",command=self.stop_download,activebackground="#353235")
     self.pause_and_play.configure(image=self.img12)  
     self.pause_and_play.configure(state="disabled") 
     self.pause_and_play.place_configure(x=415,y=557)
     self.mainloop()
     
     
     
     
    def download_Sound(self):
     self.frame_window3=tk.Frame(self,bg="#353235",width=1500,height=750)
     self.frame_window3.place(x=260,y=50)
     self.update()
     self.title_lb.configure(text="Sound Page")
     self.title("Download Sound")
     self.entry_link=ttk.Entry(self.frame_window3,width=64,font=("arial",20),background="#353235",foreground="black")
     self.entry_link.place(x=160,y=250)
     self.get_link=self.clipboard_get()
     try:
       self.get_link=self.clipboard_get()
       if self.get_link:
        self.entry_link.insert(0,self.get_link)
       else:
          return ""
     except:
          messagebox.showinfo("Copy Link ","Copy any Link and Paste in His Feild ")
     self.entry_link.bind("<FocusIn>",self.link_enter)
     self.entry_link.bind("<FocusOut>",self.link_leave)
     self.status.configure(text="</> Sound Page </>") 
     self.entry_path=ttk.Entry(self.frame_window3,width=64,font=("arial",20),background="#353235",foreground="black")
     self.entry_path.place(x=160,y=350)
     self.entry_path.insert(0,"Enter Location")
     self.entry_path.bind("<FocusIn>",self.pass_enter)
     self.entry_path.bind("<FocusOut>",self.pass_leave) 
     self.configure(background='#353235')
     self.contact_gmail_button=tk.Button(self.frame_window3,text="Gmail",bg="#4a474a",command=self.gmail,bd=0,image=self.img8,compound="left",activebackground="#4a474a",fg="white",relief="flat",font=("arial",16))   
     self.contact_gmail_button.place(x=420,y=610)
     self.contact_git_button=tk.Button(self.frame_window3,text="Github",bg="#4a474a",command=self.git,bd=0,image=self.img7,compound="left",activebackground="#4a474a",fg="white",relief="flat",font=("arial",16))   
     self.contact_git_button.place(x=530,y=610)
     self.contact_linkedin_button=tk.Button(self.frame_window3,text="Linkedin",bg="#4a474a",command=self.linkedin,bd=0,image=self.img9,compound="left",activebackground="#4a474a",fg="white",relief="flat",font=("arial",16))   
     self.contact_linkedin_button.place(x=650,y=610)
     self.resolutions_song_fields = ttk.Combobox(self.frame_window3,state= "readonly", width = 10, font = ("verdana", "8"))
     self.resolutions_song_fields.place(x=160,y=435)
     self.choose_format_label_text=tk.Label(self.frame_window3,text="Select Sound Bitrat",font=("arial",10),fg="white",bg="#4a474a")
     self.choose_format_label_text.place_configure(x=160,y=400)
     self.resolutions_song_fields['values']=("320kbps","251kbps","129kbps","128kbps","96kbps")
     self.resolutions_song_fields.set("320kbps")
     self.downloader_lablel=tk.Label(self.frame_window3,text="Location:",compound="right",font=("Roboto Slab",20),bg="#353235",fg="white")
     self.downloader_lablel.place(x=160,y=300)
     self.select_Path_button=tk.Button(self.frame_window3,width=0,text="Select Path",command=self.browse,bg="#4a474a",bd=0,activebackground="#4a474a",fg="white",relief="flat",font=("arial",16))   
     self.select_Path_button.place(x=1130,y=350)
     self.downloader_lablel=tk.Label(self.frame_window3,text="Downloader",image=self.img6,compound="right",font=("Roboto Slab",30),bg="#353235",fg="white")
     self.downloader_lablel.place(x=160,y=100)
     self.download_Sound_button=tk.Button(self.frame_window3,width=80,text="Download Sound",command=self.thread_sound,bg="#4a474a",bd=0,activebackground="#4a474a",fg="white",relief="flat",font=("arial",16))   
     self.download_Sound_button.place(x=160,y=470)
     self.info_of_download_lablel=tk.Label(self.frame_window3,text="Enter the URL of the Website you want to load:",font=("arial",20),bg="#353235",fg="white")
     self.info_of_download_lablel.place(x=160,y=200)
     self.info_of_download_lablel.configure(text="Enter the URL of the Sound:")
     self.download_label_text=tk.Label(self.frame_window3,text="Downloading",font=("arial",10),fg="white",bg="#4a474a")
     self.download_label_text.place_configure(x=160,y=520)
     self.progress_bar = ttk.Progressbar( self.frame_window3,orient = tk.HORIZONTAL, style='text.Horizontal.TProgressbar',
                length = 250, mode = 'determinate')
     self.progress_bar.place_configure(x=160,y=560)           
     self.pause_and_play=tk.Button(self.frame_window3,bd=0,compound="left",font=("arial",20),bg="#353235",command=self.stop_download,activebackground="#353235")
     self.pause_and_play.configure(image=self.img12)  
     self.pause_and_play.configure(state="disabled") 
     self.pause_and_play.place_configure(x=415,y=557)
     self.mainloop()
     
    def download_Playlist(self):
     self.update()
     self.frame_window4=tk.Frame(self,bg="#353235",width=1500,height=750)
     self.frame_window4.place(x=260,y=50)
     self.title_lb.configure(text="PLaylist Page")
     self.title("Download Playlist")
     self.entry_playlist_link=ttk.Entry(self.frame_window4,width=64,font=("arial",20),background="#353235",foreground="black")
     self.entry_playlist_link.place(x=160,y=350)
     self.get_link=self.clipboard_get()
     try:
       self.get_link=self.clipboard_get()
       if self.get_link:
        self.entry_playlist_link.insert(0,self.get_link)
       else:
          return ""
     except:
          messagebox.showinfo("Copy Link ","Copy any Link and Paste in His Feild ")
     self.entry_playlist_link.bind("<FocusIn>",self.link_playlist_enter)
     self.entry_playlist_link.bind("<FocusOut>",self.link_playlist_leave) 
     self.status.configure(text="</> PLaylist Page </>")
     self.contact_gmail_button=tk.Button(self.frame_window4,text="Gmail",bg="#4a474a",command=self.gmail,bd=0,image=self.img8,compound="left",activebackground="#4a474a",fg="white",relief="flat",font=("arial",16))   
     self.contact_gmail_button.place(x=420,y=610)
     self.contact_git_button=tk.Button(self.frame_window4,text="Github",bg="#4a474a",command=self.git,bd=0,image=self.img7,compound="left",activebackground="#4a474a",fg="white",relief="flat",font=("arial",16))   
     self.contact_git_button.place(x=530,y=610)
     self.contact_linkedin_button=tk.Button(self.frame_window4,text="Linkedin",bg="#4a474a",command=self.linkedin,bd=0,image=self.img9,compound="left",activebackground="#4a474a",fg="white",relief="flat",font=("arial",16))   
     self.contact_linkedin_button.place(x=650,y=610)
     self.resolutions_playlist_fields = ttk.Combobox(self.frame_window4, state= "readonly", width = 10, font = ("verdana", "8"))
     self.resolutions_playlist_fields.place(x=160,y=435)
     self.resolutions_playlist_fields['values']=("mp3","mp4")
     self.resolutions_playlist_fields.set("mp4")
     self.configure(background='#353235')
     self.download_Playlist_button=tk.Button(self.frame_window4,width=80,text="Download Playlist",command=self.thread_Playlist,bg="#4a474a",bd=0,activebackground="#4a474a",fg="white",relief="flat",font=("arial",16))   
     self.download_Playlist_button.place(x=160,y=470)
     self.info_of_download_lablel=tk.Label(self.frame_window4,text="Enter the URL of the Website you want to load:",font=("arial",20),bg="#353235",fg="white")
     self.info_of_download_lablel.place(x=160,y=300)
     self.info_of_download_lablel.configure(text="Enter the URL of the Playlist:")
     self.download_label_text=tk.Label(self.frame_window4,text="Downloading",font=("arial",10),fg="white",bg="#4a474a")
     self.download_label_text.place_configure(x=160,y=520)
     self.choose_format_label_text=tk.Label(self.frame_window4,text="Select Format",font=("arial",10),fg="white",bg="#4a474a")
     self.choose_format_label_text.place_configure(x=160,y=400)
     self.logo_label_text=tk.Label(self.frame_window4,image=self.img14,bg="#353235")
     self.logo_label_text.place_configure(x=160,y=0)
     self.progress_bar = ttk.Progressbar( self.frame_window4,orient = tk.HORIZONTAL, style='text.Horizontal.TProgressbar',
                length = 250, mode = 'determinate')
     self.progress_bar.place_configure(x=160,y=560)           
     self.pause_and_play=tk.Button(self.frame_window4,bd=0,compound="left",font=("arial",20),bg="#353235",command=self.stop_download,activebackground="#353235")
     self.pause_and_play.configure(image=self.img12)  
     self.pause_and_play.configure(state="disabled") 
     self.pause_and_play.place_configure(x=415,y=557)
     self.mainloop()
     
    
    def setting_window(self):
      self.update()
      self.frame_window5=tk.Frame(self,bg="#353235",width=1500,height=750)
      self.frame_window5.place(x=260,y=50)
      self.status.configure(text="</> Help Page </>")
      self.title_lb.configure(text="Help Page")
      self.title("Help")
      self.configure(background='#353235')
      self.envero_photo_lablel=tk.Label(self.frame_window5,image=self.img15,font=("Roboto Slab",30),bg="#353235",fg="white")
      self.envero_photo_lablel.place(x=160,y=50)
      self.envero_lablel=tk.Label(self.frame_window5,text="Work environment:",font=("arial",20),bg="#4a474a",fg="white")
      self.envero_lablel.place(x=160,y=10)
      self.contact_gmail_button=tk.Button(self.frame_window5,text="Gmail",bg="#4a474a",command=self.gmail,bd=0,image=self.img8,compound="left",activebackground="#4a474a",fg="white",relief="flat",font=("arial",16))   
      self.contact_gmail_button.place(x=430,y=670)
      self.contact_git_button=tk.Button(self.frame_window5,text="Github",bg="#4a474a",command=self.git,bd=0,image=self.img7,compound="left",activebackground="#4a474a",fg="white",relief="flat",font=("arial",16))   
      self.contact_git_button.place(x=540,y=670)
      self.contact_linkedin_button=tk.Button(self.frame_window5,text="Linkedin",bg="#4a474a",command=self.linkedin,bd=0,image=self.img9,compound="left",activebackground="#4a474a",fg="white",relief="flat",font=("arial",16))   
      self.contact_linkedin_button.place(x=660,y=670)
      self.developer_photo_lablel=tk.Label(self.frame_window5,image=self.img13,font=("Roboto Slab",30),bg="#353235",fg="white")
      self.developer_photo_lablel.place(x=160,y=350)
      self.develober_lablel=tk.Label(self.frame_window5,text="Developed by: </> Ahmed Ramadan </>",font=("arial",20),bg="#4a474a",fg="white")
      self.develober_lablel.place(x=160,y=300)
      self.contact_develober_lablel=tk.Label(self.frame_window5,text="To Contact With Developer:",font=("arial",20),bg="#4a474a",fg="white")
      self.contact_develober_lablel.place(x=160,y=600)
      self.lift()
      self.mainloop()
     
    
    
    def __init__(self):
        super().__init__()
        ## headers ##
        self.geometry(f'700x600+400+110')
        self.title('Full Downloader Program')
        self.attributes('-fullscreen', True)
        self.iconbitmap("images//down.ico")
        self.configure(bg="#353235")
        self.pause_download=False
        self.home_directory = os.path.expanduser( '~' )
       
        
        self.frame_window1=tk.Frame(self,bg="#353235",width=1500,height=800)
        self.frame_window1.place(x=260,y=50)
        
        self.img1=tk.PhotoImage(file="images//home.png")
        self.img2=tk.PhotoImage(file="images//downlogo.png")
        self.img3=tk.PhotoImage(file="images//help.png")
        self.img4=tk.PhotoImage(file="images//exit.png")
        self.img6=tk.PhotoImage(file="images//down_test.png")
        self.img7=tk.PhotoImage(file="images//github.png")
        self.img8=tk.PhotoImage(file="images//gmail.png")
        self.img9=tk.PhotoImage(file="images//linkedin.png")
        self.img10=tk.PhotoImage(file="images//play.png")
        self.img11=tk.PhotoImage(file="images//pause.png")
        self.img12=tk.PhotoImage(file="images//cancel.png")
        self.img13=tk.PhotoImage(file="images//Rlogo.png")
        self.img14=tk.PhotoImage(file="images//minlogo.png")
        self.img15=tk.PhotoImage(file="images//main laibrary.png")
        self.img16=tk.PhotoImage(file="images//min2logo.png")
        self.img17=tk.PhotoImage(file="images//min3logo.png")
        
        
        
        self.head_frame=tk.Frame(self,bg="#e77021")
        self.head_frame.pack(side=tk.TOP,fill=tk.X)
        self.head_frame.pack_propagate(False)
        self.head_frame.configure(height=50)
        
        myFont = font.Font(family='kanit', size=18, weight='bold')
        
        self.title_lb=tk.Label(self.head_frame,text="Home",image=self.img2,compound="right",bg="#e77021",fg="white")

        self.title_lb.place(x=0,y=3)
        
        self.title_lb['font']=myFont
        
        
        
        ## headers ##
        
        
        
        
        ## Frame And Buttons ## 
        
        
        
        
        self.toggel_menu_frame=tk.Frame(self,bg="#e77021",highlightbackground="#e77021",highlightthickness=1)

        self.window_hight=self.winfo_height()

        self.toggel_menu_frame.place(x=0,y=50,height=self.window_hight,width=260)
        myFont = font.Font(family='kanit', size=18, weight='bold')
        
        self.menu_home_button=tk.Button(self.toggel_menu_frame,text=" Home",command=self.home_window,image=self.img1,compound="left",relief="flat",bd=0,bg="#e77021",activebackground="#e77021",fg="white",activeforeground="white")
        self.menu_home_button['font']=myFont
         
        self.menu_home_button.place(x=0,y=20)
        
        
  
  
        self.menu_vedio_button=tk.Button(self.toggel_menu_frame,image=self.img2,command=self.download_veideo,compound="left",text=" Download Video",relief="flat",bd=0,bg="#e77021",activebackground="#e77021",fg="white",activeforeground="white")
  
        self.menu_vedio_button.place(x=0,y=100)
        
        self.menu_vedio_button['font']=myFont
  
        self.menu_sound_button=tk.Button(self.toggel_menu_frame,image=self.img2,command=self.download_Sound,compound="left",text=" Download Sound",bd=0,relief="flat",bg="#e77021",activebackground="#e77021",fg="white",activeforeground="white")
  
        self.menu_sound_button.place(x=0,y=180)
        self.menu_sound_button['font']=myFont
  
  
        self.menu_playlist_button=tk.Button(self.toggel_menu_frame,image=self.img2,command=self.download_Playlist,compound="left",text=" Download Playlist",bd=0,relief="flat",bg="#e77021",activebackground="#e77021",fg="white",activeforeground="white")
  
        self.menu_playlist_button.place(x=0,y=260)
        self.menu_playlist_button['font']=myFont
  
  
        self.menu_Setting_button=tk.Button(self.toggel_menu_frame,text=" Help",command=self.setting_window,image=self.img3,compound="left",bd=0,relief="flat",bg="#e77021",activebackground="#e77021",fg="white",activeforeground="white")
  
        self.menu_Setting_button.place(x=0,y=340)
        self.menu_Setting_button['font']=myFont
  
  
        self.Close_button=tk.Button(self.toggel_menu_frame,text=" Exit",image=self.img4,bd=0,compound="left",relief="flat",bg="#e77021",command=self.exit_full_program,activebackground="#e77021",fg="white",activeforeground="white")
  
        self.Close_button.place(x=0,y=420)
        
        self.Close_button['font']=myFont
        
        ## Frame And Buttons ## 
        
        
        style=Style()

        style.configure("TButton",font=('arial',20,'bold'),borderwidth="4")
        style.map("TButton",foreground=[('active','!disabled','#353235')],
        background=[('active','black')])
        
         
        
        
        
        
        
 
        
        
        
        
        
        
        # _____________________________ progress_bar__________________________________#
        self.style = ttk.Style(self)
        self.style.layout('text.Horizontal.TProgressbar',
                    [('Horizontal.Progressbar.trough',
                    {'children': [('Horizontal.Progressbar.pbar',
                                    {'side': 'left', 'sticky': 'ns'})],
                        'sticky': 'nswe'}),
                    ('Horizontal.Progressbar.label', {'sticky': ''})])
        self.style.configure('text.Horizontal.TProgressbar', text='No Download')

        

        # _____________________________ progress_bar__________________________________#
   
        
        
        self.status = tk.Label(self,text="State : Ready",width=0,fg="white",anchor="w",background="#4a474a",
                               font="arial 10 ",bd=1,relief="flat")
        self.status.place(x=260,y=845,relwidth=1)
        
        
        
        
         
        self.home_window()
        
        
        
        



app=video_downloader()
app.mainloop()