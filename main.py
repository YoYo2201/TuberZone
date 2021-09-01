from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk
import tkinter.messagebox
import speech_recognition as sr
import time
import threading
import subprocess
import pygame
import stagger
from youtube_search import YoutubeSearch
from urllib.request import urlopen
from pydub import AudioSegment
import requests
from sys import platform
import io
import base64
import os
import shutil
import pafy
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, error

root = Tk()
root.title("TuberZone")
root.geometry("800x750")
root.resizable(width=False, height=False)
root.configure(bg='black')
pygame.mixer.init()
class YT():
    def __init__(self):
        self.p = 0
        self.t_music = 0
        self.play_on = 0
        self.progress_active = 0
        self.url_copy = ""
        self.imgarr = []
        self.ent = 0
        self.frame1 = 0
        self.frame2 = 0
        self.y = 0.82
        self.title = ''
        self.download_active = 0
        self.updatedir_active = 0
        self.download_label_text = ''
    
    def Exit(self):
        Exit = tkinter.messagebox.askyesno("TuberZone","Confirm if you want to exit")
        if Exit==1:
            self.play_on = 0
            try:
                self.stop_music()
            except:
                pass
            try:
                pygame.mixer.music.unload()
                music_player.play_active = 0
                time.sleep(1)
            except:
                pass
            root.destroy()
            return

    def showimage(self, a):
        if music_player.pl == 0:
            self.frame1 = Frame(root, background="black")
            b = self.frame1
        else:
            self.frame3 = Frame(root, bg="black", width=800, height=759)
            b = self.frame3
        img = Image.open(a)
        res = img.resize((800, 750))
        image = ImageTk.PhotoImage(res)
        label1 = Label(b, image=image, bg="black")
        label1.image = image
        if music_player.pl == 0:
            label1.pack()
            b.pack()
        else:
            label1.place(relx=0, rely=0)
            self.frame3.place(relx=0, rely=0)
            self.frame3.pack_propagate(0)
    
    def destroy_allframes(self):
        try:
            self.frame1.destroy()
        except:
            pass
        try:
            self.frame3.destroy()
        except:
            pass
        try:
            self.frame2.destroy()
        except:
            pass
        try:
            music_player.scrollbar1.destroy()
        except:
            pass
    
    def show(self):
        self.label_mic = Label(self.frame1, text='Speak Now...', fg='white', bg='black', font=('arial', 20, 'bold'))
        self.label_mic.place(relx=0.5, rely=0.97, anchor='center')

    def speak(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            audio_text = r.record(source, duration=3)
        try:
            self.label_mic.destroy()
            a = r.recognize_google(audio_text)
            if str(self.ent.get()) == 'Search for a song...':
                self.ent.delete(0, 'end')
            b = len(str(self.ent.get()))
            self.ent.focus_set()
            if b == 0:
                self.ent.insert(0, a)
            else:
                self.ent.insert(b, ' '+ a)
        except:
            self.label_mic = Label(self.frame1, text="Sorry! Didn't get that", fg='white', bg='black', font=('arial', 20, 'bold'))
            self.label_mic.place(relx=0.5, rely=0.97, anchor='center')
            time.sleep(2)
            self.label_mic.destroy()
    
    def lab(self):
        self.label_mic = Label(self.frame1, text='Speak Now...', fg='white', bg='black', font=('arial', 20, 'bold'))
        self.label_mic.place(relx=0.5, rely=0.97, anchor='center')
        threading.Thread(target=self.speak).start()
    
    def stop_music(self):
        try:
            subprocess.call(['killall', 'ffplay'])
        except:
            pass
        self.t_music = 0
        self.destroy_bar()
        self.play_on = 0
        self.url_copy = ''
        self.mic_btn["image"] = self.play
        self.mic_btn.image = self.play
    
    def update_progress_bar(self):
        if float("{0:.1f}".format(self.t_music)).is_integer():
            try:
                self.progress['value'] = (self.t_music * 100)/self.dur
                self.label_text = self.timer(self.colon, self.t_music, self.duration)
                self.label_progress['text'] = self.label_text
            except:
                pass

    def timer(self, a, b, c):
        if a == 1:
            minute = int(int(b)/60)
            if minute < 10:
                minute = '0' + str(minute)
            else:
                minute = str(minute)
            seconds = int(int(b)%60)
            if seconds < 10:
                seconds = '0' + str(seconds)
            else:
                seconds = str(seconds)
            return minute + ':' + seconds + ' / ' + c
        else:
            hours = int(int(b)/3600)
            if hours < 10:
                hours = '0' + str(hours)
            else:
                hours = str(hours)
            minute = int(int(int(b)%3600)/60)
            if minute < 10:
                minute = '0' + str(minute)
            else:
                minute = str(minute)
            seconds = int(int(int(b)%3600)%60)
            if seconds < 10:
                seconds = '0' + str(seconds)
            else:
                seconds = str(seconds)
            return hours + ':' + minute + ':' + seconds + ' / ' + c

    def show_progress_bar(self):
        self.destroy_bar()
        s = ttk.Style()
        s.theme_use('default')
        s.configure("blue.Horizontal.TProgressbar", foreground='blue', background='blue', thickness=3)
        self.progress = ttk.Progressbar(self.frame1, style="blue.Horizontal.TProgressbar", orient=HORIZONTAL, length=750, mode='determinate')
        self.progress.place(relx=0.03, rely=self.y)
        self.progress['value'] = (self.t_music * 100)/self.dur
        self.label_text = self.timer(self.colon, self.t_music, self.duration)
        self.label_progress = Label(self.frame1, text=self.label_text, font=('arial', 15), fg='white', bg='black')
        self.label_progress.place(relx=0.03, rely=self.y+0.01)
        self.progress_active = 1

    def inc(self):
        self.show_progress_bar()
        while(1):
            if self.play_on:
                self.t_music += 0.1
                if self.progress_active:
                    threading.Thread(target=self.update_progress_bar).start()
                time.sleep(0.1)
            else:
                break
            if self.t_music >= self.dur:
                self.t_music = 0
                try:
                    self.stop_music()
                except:
                    pass
                try:
                    self.progress.destroy()
                    self.label_progress.destroy()
                except:
                    pass
                self.url_copy = ''
                break
    
    def play_music_continue(self):
        cat = subprocess.Popen(['youtube-dl', '-f', '251', str(self.url), '-o', '-'],
                                 stdout=subprocess.PIPE,
        )
        grep = subprocess.Popen(['ffplay', '-nodisp', '-autoexit', '-ss', str(self.t_music), '-i', '-'],
                                stdin=cat.stdout,
                                stdout=subprocess.PIPE,
        )
    
    def play_music(self, i):
        self.url_copy = self.url
        self.dur = self.results[i]["duration"]
        self.colon = 0
        t = 0
        n = 0
        j = ''
        for k in self.dur:
            if k == ':':
                t = t + int(j)*60
                j = ''
                self.colon += 1
            else:
                j = j + str(k)
        t += int(j)
        self.dur = t
        self.play_on = 1
        self.mic_btn["image"] = self.pause
        self.mic_btn.image = self.pause
        try:
            pygame.mixer.music.unload()
            music_player.play_active = 0
        except:
            pass
        self.play_music_continue()
        if self.download_active == 1 and self.title == self.results[i]["title"]:
            self.y = 0.78
            root.geometry('800x850')
            self.show_download_progress()
        self.thr = threading.Thread(target=self.inc)
        self.thr.start()

    def select_play_pause(self, i):
        if self.play_on == 0:
            self.play_music(i)
        else:
            if self.url_copy == self.url:
                subprocess.call(['killall', 'ffplay'])
                self.play_on = 0
                self.mic_btn["image"] = self.play
                self.mic_btn.image = self.play
            else:
                self.t_music = 0
                self.stop_music()
                time.sleep(1)
                self.play_music(i)
    
    def rlist(self):
        l = []
        grp = []
        var = 0
        p = []
        pq = 0
        for i in self.streams:
            cp = str(i).split(' ')
            f = cp[3][5:-1]
            if pq == 1:
                break
            if str(f) == '144p':
                pq = 1
            if str(f) in l:
                pass
            else:
                l.append(str(f))
                p.append(str(f))
                p.append(var)
                grp.append(p)
                p = []
            var += 1
        return grp
    
    def showmsg(self):
        messagebox.showinfo("Download Info", "Downloaded!!!")
    
    def update_download_progress(self):
        try:
            self.download_progress['value'] = round(self.ratio*100, 1)
            self.download_label_text = str(self.recvd) + ' / ' + str(self.total) + ' (' + str(round(self.ratio*100, 1)) + '%)  Time Left : ' + str(self.eta)
            self.download_label_progress['text'] = self.download_label_text
        except:
            pass
        if self.ratio == 1:
            self.download_label_progress['text'] = 'Processing...'
            if self.audiostreams[2].extension == 'm4a':
                audio1 = AudioSegment.from_file(self.title+".m4a", format="m4a")
            elif self.audiostreams[2].extension == 'webm':
                audio1 = AudioSegment.from_file(self.title+".webm", format="webm")
            audio1.export(self.title+".mp3", format="mp3")
            try:
                os.remove(self.title+".m4a")
            except:
                os.remove(self.title+".webm")
            audio_path = self.title+'.mp3'
            res = requests.get(self.thumbnail)
            file = open(self.title+".jpg", "wb")
            file.write(res.content)
            file.close()
            image_path = self.title+".jpg"
            audio = MP3(audio_path, ID3=ID3)
            try:
                audio.add_tags()
            except error:
                pass
            audio.tags.add(APIC(mime='image/jpeg',type=3,desc=u'Cover',data=open(image_path,'rb').read()))
            audio.save()
            os.remove(image_path)
            try:
                shutil.move(self.title+'.mp3', self.dirname)
            except:
                pass
            time.sleep(1)
            self.download_progress.destroy()
            self.download_label_progress.destroy()
            threading.Thread(target=self.showmsg).start()
            root.geometry('800x750')
            self.y = 0.82
            if self.url_copy == self.url:
                self.show_progress_bar()
            self.download_active = 0
            self.title = ''
            if self.updatedir_active == 0:
                self.updatedir_active = 1
                menubar.entryconfig(3, label="Update Directory", command=self.updatedir)
                menubar.add_command(label="Exit", command=self.Exit)
            self.total_calc = 0
    
    def byteconvert(self, a):
        if a < 1024:
            a = str(a) + 'bytes'
        elif a >= 1024 and a < 1048576:
            a = str(float("{0:.2f}".format(a/1024))) + 'KB'
        elif a >= 1048576 and a < 1073741824:
            a = str(float("{0:.2f}".format(a/1048576))) + 'MB'
        elif a >= 1073741824:
            a = str(float("{0:.2f}".format(a/1073741824))) + 'GB'
        return a
    
    def time_convert(self):
        hours = int(int(self.eta)/3600)
        if hours < 10:
            hours = '0' + str(hours)
        else:
            hours = str(hours)
        minute = int(int(int(self.eta)%3600)/60)
        if minute < 10:
            minute = '0' + str(minute)
        else:
            minute = str(minute)
        seconds = int(int(int(self.eta)%3600)%60)
        if seconds < 10:
            seconds = '0' + str(seconds)
        else:
            seconds = str(seconds)
        self.eta = hours + ':' + minute + ':' + seconds
            

    def video_progressbar(self, total, recvd, ratio, rate, eta):
        self.ratio = ratio
        self.recvd = recvd
        self.eta = eta
        self.recvd = self.byteconvert(self.recvd)
        if self.total_calc == 0:
            self.total = total
            self.total_calc = 1
            self.total = self.byteconvert(self.total)
        self.time_convert()
        threading.Thread(target=self.update_download_progress).start()
    
    def show_download_progress(self):
        try:
            self.download_progress.destroy()
            self.download_label_progress.destroy()
        except:
            pass
        s = ttk.Style()
        s.theme_use('default')
        s.configure("blue.Horizontal.TProgressbar", foreground='blue', background='blue', thickness=3)
        self.download_progress = ttk.Progressbar(self.frame1, style="blue.Horizontal.TProgressbar", orient=HORIZONTAL, length=750, mode='determinate')
        self.download_progress.place(relx=0.03, rely=0.85)
        self.download_progress['value'] = self.ratio
        self.download_label_progress = Label(self.frame1, text=self.download_label_text, font=('arial', 15), fg='white', bg='black')
        self.download_label_progress.place(relx=0.03, rely=0.86)
    
    def createdefaultdir(self):
        self.dirname = filedialog.askdirectory(title='Select a Folder for storing your downloaded music files')
        if not self.dirname:
            messagebox.showerror("Directory Error", "Please Select a Folder!!!")
            self.createdefaultdir()
        else:
            with open('/TuberZone.txt', 'wb') as f:
                f.write(self.dirname.encode('utf-8'))
            f.close()

    def downloadbtn(self, i):
        self.ratio = 0
        self.title = self.results[i]['title']
        if os.path.isfile('/TuberZone.txt'):
            with open('/TuberZone.txt', 'rb') as f:
                a = f.read()
                a = a.decode('utf-8')
            f.close()
            if os.path.isdir(a):
                self.dirname = a
            else:
                self.createdefaultdir()
        else:
            self.createdefaultdir()
        if os.path.isfile(self.dirname+'/'+str(self.title)+".mp3"):
            messagebox.showinfo("File Info", "File Already Exist!!!")
        else:
            self.download_active = 1
            video = pafy.new(self.url)
            self.audiostreams = video.audiostreams
            if self.url == self.url_copy:
                root.geometry('800x850')
                self.y = 0.78
                self.show_progress_bar()
            self.show_download_progress()
            self.total_calc = 0
            a = threading.Thread(target=self.audiostreams[2].download, kwargs={'callback': self.video_progressbar}, daemon=True).start()
    
    def updatedir(self):
        self.createdefaultdir()
        messagebox.showinfo("Directory Info", "Directory Updated!!!")
    
    def button_pressed(self, i):
        root.geometry('800x750')
        self.p = 1
        self.frame3.destroy()
        self.frame1 = Frame(root, bg="black")
        btn = Button(self.frame1, image=self.imgarr[i], bg="black")
        btn.image = self.imgarr[i]
        btn.pack()
        label = Label(self.frame1, text=self.results[i]["title"], fg='white', bg='black', font=('arial', 15, 'bold'))
        label.config(wraplength=650)
        label.pack(fill=BOTH)
        channel = Label(self.frame1, text='\nChannel : ' + self.results[i]["channel"], fg='white', bg='black', font=('arial', 30, 'bold'))
        channel.config(wraplength=650)
        channel.pack(fill=BOTH)
        self.duration = self.results[i]['duration']
        duration = Label(self.frame1, text='Duration : ' + self.results[i]["duration"], fg='white', bg='black', font=('arial', 30, 'bold'))
        duration.pack(fill=BOTH)
        img = Image.open('play.png')
        res = img.resize((50, 49))
        self.play = ImageTk.PhotoImage(res)
        img = Image.open('pause.jpg')
        res = img.resize((50, 49))
        self.pause = ImageTk.PhotoImage(res)
        self.url = str('http://youtube.com' + self.results[i]["url_suffix"])
        if self.title == self.results[i]["title"]:
            if self.download_active:
                self.show_download_progress()
        if self.url_copy == self.url:
            if self.play_on == 1:
                self.image = self.pause
                self.show_progress_bar()
            else:
                if self.t_music:
                   self.show_progress_bar()
                self.image = self.play
        else:
            self.image = self.play
        self.mic_btn = Button(self.frame1, image=self.image, bg="black", command=lambda: self.select_play_pause(i))
        self.mic_btn.config(highlightthickness=0, highlightbackground='black')
        self.mic_btn.image = self.image
        self.mic_btn.place(relx=0.17, rely=0.92)
        img = Image.open('reset.png')
        res = img.resize((50, 49))
        self.reset = ImageTk.PhotoImage(res)
        reset_btn = Button(self.frame1, image=self.reset, bg="black", command=self.stop_music)
        reset_btn.config(highlightthickness=0, highlightbackground='black')
        reset_btn.image = self.reset
        reset_btn.place(relx=0.47, rely=0.92)
        img = Image.open('download.jpg')
        res = img.resize((65, 49))
        self.download = ImageTk.PhotoImage(res)
        self.thumbnail = self.results[i]['thumbnails'][0]
        download_btn = Button(self.frame1, image=self.download, bg="black", command=lambda: self.downloadbtn(i))
        download_btn.config(highlightthickness=0, highlightbackground='black')
        download_btn.image = self.download
        download_btn.place(relx=0.77, rely=0.92)
        self.frame1.pack(fill=BOTH, expand=True)
    
    def destroy_bar(self):
        try:
            self.progress.destroy()
            self.label_progress.destroy()
            self.progress_active = 0
        except:
            pass
    
    def image_extract(self, i):
        raw_data = requests.get(self.results[i]["thumbnails"][0])
        image_b64 = raw_data.content
        img = Image.open(io.BytesIO(image_b64))
        res = img.resize((800, 400))
        self.imgarr.append(ImageTk.PhotoImage(res))

    def setimg_btn(self, i):
        imgbtn = Button(self.frame2, image=self.imgarr[i], bg="black", command= lambda: self.button_pressed(i))
        imgbtn.image = self.imgarr[i]
        imgbtn.pack()
        label = Label(self.frame2, text=self.results[i]["title"], fg='white', bg='black', font=('arial', 15, 'bold'))
        label.config(wraplength=650)
        label.pack(fill=BOTH)

    def create_canvas(self):
        try:
            self.frame2.destroy()
        except:
            pass
        self.destroy_bar()
        self.frame3 = Frame(root, bg="black")
        canvas = Canvas(self.frame3)
        canvas.pack(side=LEFT, fill=BOTH, expand=True)
        scroll = ttk.Scrollbar(self.frame3, orient=VERTICAL, command=canvas.yview)
        scroll.pack(side=RIGHT, fill=Y)
        canvas.configure(yscrollcommand=scroll.set)
        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
        self.frame2 = Frame(canvas, bg='black')
        canvas.create_window((0, 0), window=self.frame2, anchor='nw')
    
    def destroy_frame(self):
        self.frame1.destroy()
        self.stop_loading = 1
        try:
            self.frame3.pack(fill=BOTH, expand=True)
        except:
            pass
    
    def showres(self):
        self.imgarr = []
        self.create_canvas()
        for i in range(15):
            self.image_extract(i)
            self.setimg_btn(i)
        self.destroy_frame()
        
    def start_thread(self):
        try:
            self.results = YoutubeSearch(self.a, max_results=15).to_dict()
            self.showres()
        except:
            messagebox.showerror("Result Error", "Parsing Failure...Please try again!!!")
            self.Searchbyname()

    def loading_progress(self):
        try:
            self.progress1.destroy()
            self.progress2.destroy()
            self.progress3.destroy()
        except:
            pass
        try:
            time.sleep(0.5)
            s = ttk.Style()
            s.theme_use('default')
            if music_player.pl == 0:
                a = self.frame1
            else:
                a = self.frame3
            s.configure("red.Horizontal.TProgressbar", foreground='red', background='red', thickness=5)
            self.progress1 = ttk.Progressbar(a, style="red.Horizontal.TProgressbar", orient=HORIZONTAL, length=10, mode='determinate')
            self.progress1['value'] = 100
            self.progress1.place(relx=0.66, rely=0.52)
            time.sleep(0.5)
            s.configure("green.Horizontal.TProgressbar", foreground='green', background='green', thickness=5)
            self.progress2 = ttk.Progressbar(a, style="green.Horizontal.TProgressbar", orient=HORIZONTAL, length=10, mode='determinate')
            self.progress2['value'] = 100
            self.progress2.place(relx=0.69, rely=0.52)
            time.sleep(0.5)
            s.configure("blue.Horizontal.TProgressbar", foreground='blue', background='blue', thickness=5)
            self.progress3 = ttk.Progressbar(a, style="blue.Horizontal.TProgressbar", orient=HORIZONTAL, length=10, mode='determinate')
            self.progress3['value'] = 100
            self.progress3.place(relx=0.72, rely=0.52)
            time.sleep(0.5)
            if self.stop_loading == 0:
                self.loading_progress()
        except:
            pass
    
    def loading(self):
        self.stop_loading = 0
        if music_player.pl == 0:
            self.frame1.destroy()
        else:
            try:
                self.frame3.destroy()
            except:
                pass
            try:
                self.frame2.destroy()
            except:
                pass
        self.showimage('loading.png')
        threading.Thread(target=self.loading_progress).start()
    
    def search(self):
        self.a = str(self.ent.get())
        if len(self.a) != 0:
            self.loading()
            threading.Thread(target=self.start_thread).start()

    def check_for_enter(self, event):
        if event.keysym == 'Return':
            self.search()
    
    def close(self, event):
        if self.p == 1:
            self.create_canvas()
            for i in range(15):
                self.setimg_btn(i)
            self.destroy_frame()
        self.p = 0
    
    def click(self, *args):
        if str(self.ent.get()) == 'Search for a song...':
            self.ent.delete(0, 'end')
            self.ent['font'] = ('arial',20,'bold')
            self.ent['fg'] = 'black'

    def Searchbyname(self):
        music_player.pl = 0
        self.destroy_allframes()
        root.geometry('800x750')
        self.showimage("music.jpeg")
        self.ent = Entry(self.frame1, font=('arial',20), bd=5, justify=LEFT, width=30, bg='white', fg='grey')
        self.ent.insert(0, "Search for a song...")
        self.ent.place(relx=0.1, rely=0.1)
        img = Image.open('Mic2.png')
        res = img.resize((50, 39))
        image = ImageTk.PhotoImage(res)
        self.mic_btn1 = Button(self.frame1, image=image, command=self.lab)
        self.mic_btn1.image = image
        self.mic_btn1.place(relx=0.68, rely=0.1)
        self.btn1 = Button(self.frame1,text='Search',width=6,height=1,font=('arial',20,'bold'),bd=2,bg="black",fg='white', command=self.search)
        self.btn1.place(relx=0.78, rely=0.1)
        self.ent.bind("<Button-1>", self.click)
        self.ent.bind("<Key>", self.check_for_enter)


class MP():
    def __init__(self):
        self.play_active = 0
        self.b = 0
        self.playlist_empty = 1
        self.pl = 0
        self.over = 0
    
    def editimg(self, a, x, y, s):
        img = Image.open(a)
        res = img.resize((50, 49))
        image = ImageTk.PhotoImage(res)
        if s == 1:
            self.playimg = image
        elif s == 2:
            self.pauseimg = image
        else:
            pass
        btn = Button(obj.frame2, image=image, bg="black")
        btn.config(highlightthickness=0, highlightbackground='black')
        btn.image = image
        btn.place(relx=x, rely=y)
        return btn
    
    def stop_music(self):
        try:
            pygame.mixer.music.stop()
        except:
            pass
        self.destroy_bar()
        self.play_pause_btn['image'] = self.playimg
        self.play_pause_btn.image = self.playimg
        self.play_active = 0
        self.b = 0
    
    def play_pause(self):
        if self.play_active == 0:
            if pygame.mixer.music.get_pos() == -1:
                pygame.mixer.music.play(loops=0)
            else:
                pygame.mixer.music.unpause()
            self.play_pause_btn['image'] = self.pauseimg
            self.play_active = 1
            threading.Thread(target=self.inc).start()
        else:
            pygame.mixer.music.pause()
            self.play_active = 0
            self.play_pause_btn['image'] = self.playimg
    
    def for_rev(self, i):
        a = (pygame.mixer.music.get_pos()/1000) + self.b
        if a == (-1/1000):
            pass
        else:
            if a+i <= 0:
                self.b = 0
            else:
                self.b = a+i
            pygame.mixer.music.stop()
            try:
                pygame.mixer.music.play(loops=1, start=float(self.b))
            except:
                pass
    
    def destroy_bar(self):
        try:
            self.progress.destroy()
            self.label_progress.destroy()
            self.progress_active = 0
        except:
            pass
    
    def update_progress_bar(self):
        if float("{0:.1f}".format((pygame.mixer.music.get_pos()/1000)+self.b)).is_integer():
            try:
                self.progress['value'] = (((pygame.mixer.music.get_pos()/1000)+self.b)*100)/self.dur
                self.label_text = obj.timer(self.colon, (pygame.mixer.music.get_pos()/1000)+self.b, self.duration)
                self.label_progress['text'] = self.label_text
            except:
                pass
    
    def inc(self):
        self.show_progress_bar()
        while(1):
            if self.play_active == 1:
                try:
                    self.over = 0
                    threading.Thread(target=self.update_progress_bar).start()
                    time.sleep(0.1)
                except:
                    break
            if (pygame.mixer.music.get_pos()/1000)+self.b >= self.dur or (pygame.mixer.music.get_pos()/1000)+self.b < 0:
                try:
                    self.stop_music()
                except:
                    pass
                try:
                    self.progress.destroy()
                    self.label_progress.destroy()
                except:
                    pass
                if self.pl == 1:
                    self.songindex += 1
                    if self.songindex >= len(self.songpathlist):
                        self.over = 1
                        break
                    else:
                        self.over = 0
                    threading.Thread(target=self.loadsong).start()
                break
            if self.play_active == 0:
                break
    
        if self.over == 1:
            self.startplaylist()
    
    def show_progress_bar(self):
        self.destroy_bar()
        s = ttk.Style()
        s.theme_use('default')
        s.configure("blue.Horizontal.TProgressbar", foreground='blue', background='blue', thickness=3)
        self.progress = ttk.Progressbar(obj.frame2, style="blue.Horizontal.TProgressbar", orient=HORIZONTAL, length=750, mode='determinate')
        self.progress.place(relx=0.03, rely=0.84)
        self.progress['value'] = (((pygame.mixer.music.get_pos()/1000)+self.b)*100)/self.dur
        self.label_text = obj.timer(self.colon, (pygame.mixer.music.get_pos()/1000)+self.b, self.duration)
        self.label_progress = Label(obj.frame2, text=self.label_text, font=('arial', 15), fg='white', bg='black')
        self.label_progress.place(relx=0.03, rely=0.85)
        self.progress_active = 1
    
    def showimg(self):
        if self.pl == 0:
            obj.frame2 = Frame(root, bg='black')
        else:
            obj.frame2 = Frame(root, bg="black", width=800, height=759)
            obj.frame2.place(relx=0, rely=0)
            obj.frame2.pack_propagate(0)
            try:
                self.label1.destroy()
            except:
                pass
        mp3 = stagger.read_tag(self.file)
        by_data = mp3[stagger.id3.APIC][0].data
        im = io.BytesIO(by_data)
        img = Image.open(im)
        res = img.resize((800, 550))
        image = ImageTk.PhotoImage(res)
        imgbtn = Button(obj.frame2, image=image, bg="black")
        imgbtn.image = image
        imgbtn.pack(fill=BOTH)
        label = Label(obj.frame2, text=self.song_title, fg='white', bg='black', font=('arial', 15, 'bold'))
        label.config(wraplength=650)
        label.pack(fill=BOTH)
        reverse_btn = self.editimg('reverse.png', 0.25, 0.92, 0)
        self.play_pause_btn = self.editimg('play.png', 0.39, 0.92, 1)
        self.play_pause_btn = self.editimg('pause.jpg', 0.39, 0.92, 2)
        forward_btn = self.editimg('forward.png', 0.53, 0.92, 0)
        reset_btn = self.editimg('reset.png', 0.67, 0.92, 0)
        reset_btn['command'] = self.stop_music
        self.play_pause_btn['command'] = self.play_pause
        reverse_btn['command'] = lambda: self.for_rev(-5)
        forward_btn['command'] = lambda: self.for_rev(5)
        if self.pl == 0:
            obj.frame2.pack(fill=BOTH, expand=True)
        else:
            pass
    
    def playsong(self):
        AudioSegment.from_file(self.file).export('a.ogg', format='ogg')
        self.showimg()
        obj.stop_loading = 1
        if self.pl == 0:
            obj.frame1.destroy()
        else:
            obj.frame3.destroy()
        try:
            pygame.mixer.music.unload()
        except:
            pass
        self.b = 0
        pygame.mixer.music.load('a.ogg')
        pygame.mixer.music.play(loops=0)
        a = pygame.mixer.Sound('a.ogg')
        self.dur = int(round(a.get_length(), 0))
        if self.dur >= 3600:
            self.colon = 2
        else:
            self.colon = 1
        self.duration = obj.timer(self.colon, self.dur, '')
        self.duration = self.duration[0:-3]
        self.play_active = 1
        os.remove('a.ogg')
        threading.Thread(target=self.inc).start()
    
    def songtitle(self, x, y):
        a = str(x)[len(x)::-1]
        for i in a:
            if i == '/':
                break
            y = i + y
        z = x.replace(y, '')
        try:
            y = y.replace('.mp3', '')
        except:
            y = y.replace('.wav', '')
        return y, z
    
    def loadsong(self):
        if self.pl == 0:
            a = filedialog.askopenfilename(title='Select a Song', filetypes=(("mp3 files", "*.mp3"), ("wav files", "*.wav")))
        else:
            f = open('/PlayList.txt', 'r')
            lines = f.readlines()
            f.close()
            for n, line in enumerate(lines):
                if n == self.songindex:
                    a = str(line.replace('\n', ''))
                    break
        try:
            obj.stop_music()
        except:
            pass
        if a:
            self.file = a
            self.song_title = ''
            self.song_title, a = self.songtitle(self.file, self.song_title)
            self.play_active = 0
            obj.loading()
            threading.Thread(target=self.playsong).start()
        else:
            pass
    
    def insertplaylist(self, x):
        self.songlist = []
        count = 0
        f = open("/PlayList.txt", "w")
        for i in x:
            a, b = self.songtitle(i, '')
            self.songlist.append(a)
            self.songpathlist.append(i)
            self.path.append(b)
            self.playlist.insert(END, self.songlist[count])
            f.write(i+'\n')
            count += 1
        f.close()
        
    def createplaylist(self):
        self.songindex = -1
        x = filedialog.askopenfilenames(title='Select Songs to Add in PlayList', filetypes=(("mp3 files", "*.mp3"), ("wav files", "*.wav")))
        self.insertplaylist(x)
        if self.songpathlist:
            self.btn.destroy()
            self.playlist_empty = 0
    
    def checkplaylistsize(self):
        if os.path.isfile('/PlayList.txt'):
            f = open('/PlayList.txt', 'r')
            lines = f.readlines()
            f.close()
            count = 0
            f = open('/PlayList.txt', 'w')
            for n, line in enumerate(lines):
                line = line.replace('\n', '')
                if os.path.isfile(line):
                    self.playlist_empty = 0
                    f.write(line+'\n')
                    self.songpathlist.append(line)
                    a, b = self.songtitle(line, '')
                    self.songlist.append(a)
                    self.path.append(b)
                    self.playlist.insert(END, self.songlist[count])
                    count += 1
            f.close()
        else:
            self.playlist_empty = 1
    
    def addsong(self):
        if len(self.songpathlist) == 0:
            messagebox.showerror("Playlist Error", "No Playlist Found to add song!!!")
        else:
            l = filedialog.askopenfilenames(title='Select Songs to Add in PlayList', filetypes=(("mp3 files", "*.mp3"), ("wav files", "*.wav")))
            f = open('/PlayList.txt', 'r')
            lines = f.readlines()
            f.close()
            f = open('/PlayList.txt', 'a')
            alreadypresent = 0
            for n, line in enumerate(l):
                if line+'\n' in lines:
                    alreadypresent = 1
                else:
                    f.write(line+'\n')
                    a, b = self.songtitle(line, '')
                    self.songlist.append(a)
                    self.path.append(b)
                    self.songpathlist.append(line)
                    self.playlist.insert(END, a)
            if alreadypresent:
                messagebox.showwarning("Insertion Warning", "Some songs were not added as they were already present in the playlist!!!")
    
    def deletesong(self):
        if len(self.songpathlist) == 0:
            messagebox.showerror("Delete Error", "No song to delete!!!")
        else:
            a = str(self.playlist.get(ANCHOR))
            if a == '':
                pass
            else:
                index = list(self.playlist.get(0, "end")).index(a)
                try:
                    if index <= self.songindex:
                        self.songindex -= 1
                except:
                    pass
                self.playlist.delete(ANCHOR)
                self.path.pop(index)
                self.songlist.pop(index)
                self.songpathlist.pop(index)
                f = open("/PlayList.txt", 'r')
                lines = f.readlines()
                f.close()
                f = open('/PlayList.txt', 'w')
                for n, line in enumerate(lines):
                    if n is not index:
                        f.write(line)
                f.close()
                if len(self.songpathlist) == 0:
                    self.btn = Button(obj.frame1, text="Create a New PlayList", fg="black", bg="white", command=self.createplaylist)
                    self.btn.place(relx=0.5, rely=0.5, anchor='center')
    
    def clearsonglist(self):
        self.songlist = []
        self.songpathlist = []
        self.path = []
        f = open('/PlayList.txt', 'w')
        f.close()
        self.playlist.delete(0, END)
        self.btn = Button(obj.frame1, text="Create a New PlayList", fg="black", bg="white", command=self.createplaylist)
        self.btn.place(relx=0.5, rely=0.5, anchor='center')
    
    def startplaying(self, *args):
        a = str(self.playlist.get(ANCHOR))
        self.songindex = list(self.playlist.get(0, END)).index(a)
        self.loadsong()
    
    def startplaylist(self):
        self.pl = 1
        obj.destroy_allframes()
        root.geometry('1115x759')
        if self.play_active:
            self.showimg()
            self.show_progress_bar()
        else:
            obj.frame3 = Frame(root, bg="black", width=800, height=759)
            self.label1 = Label(obj.frame3, font=('arial', 15), text="Select a PlayList and Enjoy Music!!!", fg="white", bg="black")
            self.label1.place(relx=0.5, rely=0.5, anchor='center')
            obj.frame3.place(relx=0, rely=0)
            obj.frame3.pack_propagate(0)
        obj.frame1 = Frame(root, bg="white", width=300, height=759)
        lab = Label(obj.frame1, bg="white", height=2)
        lab.pack(fill=None, expand=False)
        btn1 = Button(obj.frame1, text="Add", fg="white", bg="black", command=self.addsong)
        btn1.place(relx=0.08, rely=0.005)
        btn2 = Button(obj.frame1, text="Delete", fg="white", bg="black", command=self.deletesong)
        btn2.place(relx=0.36, rely=0.005)
        btn3 = Button(obj.frame1, text="Clear", fg="white", bg="black", command=self.clearsonglist)
        btn3.place(relx=0.7, rely=0.005)
        self.scrollbar1 = ttk.Scrollbar(root, orient=VERTICAL)
        scrollbar2 = ttk.Scrollbar(obj.frame1, orient=HORIZONTAL)
        self.playlist = Listbox(obj.frame1, bg="white", fg="blue", width=37, height=39, yscrollcommand=self.scrollbar1.set, xscrollcommand=scrollbar2.set)
        self.playlist.pack(fill=None, expand=False)
        self.scrollbar1.pack(side=RIGHT, fill=BOTH)
        scrollbar2.pack(side=BOTTOM, fill=BOTH)
        self.scrollbar1.config(command=self.playlist.yview)
        scrollbar2.config(command=self.playlist.xview)
        obj.frame1.place(relx=0.72, rely=0)
        self.songpathlist = []
        self.songlist = []
        self.path = []
        self.playlist_empty = 1
        self.checkplaylistsize()
        if self.playlist_empty == 1:
            self.btn = Button(obj.frame1, text="Create a New PlayList", fg="black", bg="white", command=self.createplaylist)
            self.btn.place(relx=0.5, rely=0.5, anchor='center')
        self.playlist.bind('<Double-Button-1>', self.startplaying)
        
    def showmusicoptions(self):
        obj.destroy_allframes()
        self.pl = 0
        root.geometry('800x750')
        obj.showimage('Mic.jpg')
        btn1 = Button(obj.frame1,text='Play a Song',width=12,height=2,font=('arial',20,'bold'),bd=5,bg="black",fg='white', command=self.loadsong)
        btn1.place(relx=0.1, rely=0.33)
        btn2 = Button(obj.frame1,text='Start a Playlist',width=12,height=2,font=('arial',20,'bold'),bd=5,bg="black",fg='white', command=self.startplaylist)
        btn2.place(relx=0.1, rely=0.47)

obj = YT()
music_player = MP()
menubar=Menu(root, background='black', fg='white')
filemenu=Menu(menubar,tearoff=0)
menubar.add_command(label="Youtube Downloader", command=obj.Searchbyname)
menubar.add_command(label="Music Player", command=music_player.showmusicoptions)
if os.path.isfile('/TuberZone.txt'):
    obj.updatedir_active = 1
    menubar.add_command(label="Update Directory", command=obj.updatedir)
else:
    obj.updatedir_active = 0
menubar.add_command(label="Exit",command=obj.Exit)
root.config(menu=menubar)
root.protocol("WM_DELETE_WINDOW", obj.Exit)
obj.showimage("1.jpg")
root.bind('<Escape>', obj.close)
root.mainloop()