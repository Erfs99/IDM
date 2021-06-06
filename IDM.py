from tkinter import *
import tkinter as tk
import time
import tkinter.ttk as ttk
from pathlib import Path
from tkinter.constants import *
from pySmartDL import SmartDL
import threading
import os
import subprocess
import webbrowser
from tkinter import messagebox,filedialog
from PIL import Image, ImageTk
from pytube import YouTube 
import sys
root=Tk()
root.title("Erfn Download Manager")
root.iconbitmap("icons/global.ico")
root.geometry("780x550")
root.resizable(False, False) 

color=""
objectt=""
default_browser=""
input_link=StringVar()
status_message=StringVar()
speed_message=StringVar()
destination_message=StringVar()
size_message=StringVar()
time_message=StringVar()
download_paths=StringVar()
is_paused=False


app_menu=Menu(root)
root.config(menu=app_menu)

menu_file=Menu(app_menu,tearoff=False,bg="white",fg="black",font=("Times", "10","bold") )
app_menu.add_cascade(label="File",menu=menu_file)

menu_edit=Menu(app_menu,tearoff=0,bg="white",fg="black",font=("Times", "10","bold") )
app_menu.add_cascade(label="Edit",menu=menu_edit)

menu_download=Menu(app_menu,tearoff=False,bg="white",fg="black",font=("Times", "10","bold") )
app_menu.add_cascade(label="Dowload",menu=menu_download)

menu_help=Menu(app_menu,tearoff=False,bg="white",fg="black",font=("Times", "10","bold") )
app_menu.add_cascade(label="Need Help?",menu=menu_help)

exit=Menu(app_menu,tearoff=False)
app_menu.add_radiobutton(label="about")

# -------------------------------------------------------------------

def cancel(obj):
    obj.stop()
    button_pause['state'] = DISABLED
    button_stop['text'] = 'Canceled!'
    button_stop['state'] = DISABLED
    button_stop["bg"]="gold"

def pause_resume(object):
    global is_paused
    if is_paused:
        object.resume()
        button_pause["text"]="Pause"
        button_pause["fg"]="red"
        button_pause["bg"]="black"
        button_pause.flash()
        is_paused=not is_paused
    else:
        object.pause()
        button_pause["text"]="Resume"
        button_pause["fg"]="green"
        button_pause["bg"]="black"
        button_pause.flash()   
        is_paused=not is_paused

def download(_url_):
    global speed_message
    global status_message
    global destination_message
    global size_message
    global time_message
    global progress
    global dest
    global objectt
    url=_url_
    
    download_folder=download_paths.get()

    button_stop["command"]=lambda: cancel(objectt)
    button_stop["state"]=NORMAL
    button_pause["command"]=lambda:pause_resume(objectt)
    button_pause["state"]=NORMAL
        
        
    def downloading(process):
        with process:
            try:
                objectt.start()
            except Exception as e:
                print(f"Error {objectt.get_errors()}")
                messagebox.showerror("Error","Something went wrong! Check Url")
                status_message.set(f"Status {e}")
                root.update_idletasks()
                
    def show_progress(process):
        with process:
            time.sleep(1)
            start_time = time.perf_counter()
            while not objectt.isFinished() and len(objectt.get_errors()) == 0:
                status_message.set(f"Status: {objectt.get_status()}")
                destination_message.set(f"Working directory: {download_folder}")
                size_message.set(f"Downloaded so far: {objectt.get_dl_size(human=True)}")
                time_message.set(f"Elapsed Time: {round(time.perf_counter() - start_time, 1)}" if objectt.get_status() != "paused" else "Elapsed Time: ")
                progress["value"]= 100 * objectt.get_progress()
                time.sleep(0.3)
                root.update_idletasks()
            if len(objectt.get_errors()) == 0:
                start_point=time.perf_counter()
                while time.perf_counter() - start_point < 2:
                    try:
                        status_message.set(f"Status: {objectt.get_status()}" )
                        speed_message.set(f"Speed: { objectt.get_speed(human=True)}")
                        size_message.set(f"Total File Size: { objectt.get_final_filesize(human=True)}")
                        time_message.set(f"Total Time: {str(objectt.get_dl_time(human=True))}")
                        progress['value'] = 100 * objectt.get_progress()
                        messagebox.showinfo("Download finished"," Your download has been completed! ")
                        time.sleep(0.2)
                        root.update_idletasks()
                    except:
                        pass
            else:
                status_message.set(f"Status: Failed ")
                speed_message.set(f"Reason: {objectt.get_errors()[0]}")
                root.update_idletasks()
    if len(url) == 0:
        button_download.flash()
    else:
        try:
            objectt = SmartDL(url,download_folder)
        except Exception as e:
            print(f"Error in {e}")
            status_message.set(f"Status: {e}")
            root.update_idletasks()
        semaphore = threading.Semaphore(2)
        threading.Thread(target=downloading,args=(semaphore,)).start()
        threading.Thread(target=show_progress,args=(semaphore,)).start()

            
def do_popup(event):
    try:
        m.tk_popup(event.x_root,event.y_root)
    finally:
        m.grab_release()


def cut(input):
    input=input
    entry_link.clipboard_clear()
    entry_link.clipboard_append(input)
    input_link.set("")

def copy(input):
    input=input
    entry_link.clipboard_clear()
    entry_link.clipboard_append(input)

def paste(input):
    input0=input
    input1=entry_link.clipboard_get()
    input_link.set(input0+input1)
 

def clear():
    input_link.set("")
    button_download["state"]=NORMAL
    button_stop["state"]=NORMAL
    button_stop["bg"]=color
    button_stop["text"]="Cancel"
    status_message.set("")
    speed_message.set("")
    destination_message.set("")
    size_message.set("")
    time_message.set("")
    download_paths.set("")

def start_downloading():
    global color
    link=entry_link.get()
    if link != "":
        download(link)
        button_download["state"]=DISABLED
        color=button_stop.cget("background")
    else:
        button_download.flash()
        messagebox.showwarning("Empty Field","please fill out this field!")


def browsing():
    webbrowser.open("C:/Users/Monjirayaneh/Downloads")
    print("folder opened")


def Exit():
    if messagebox.askyesno(" < Exit >","are you sure you want to leave program?!") == False:
        return False
    else:
        sys.exit(0)

def Browse(): 
    dest = filedialog.askdirectory(initialdir="YOUR DIRECTORY PATH")
    download_paths.set(dest)
    
   
def openyoutube(): 
    youtube_window = Toplevel(root) 
    youtube_window.title("Youtube Downloader") 
    youtube_window.geometry("550x200") 
    youtube_window.resizable(False, False) 
    video_Link = StringVar() 
    download_Path = StringVar() 


    def Browse(): 
        download_Directory = filedialog.askdirectory(initialdir="YOUR DIRECTORY PATH") 
        download_Path.set(download_Directory) 
  
    def Download(): 
        Youtube_link = video_Link.get() 
        download_Folder = download_Path.get() 
        getVideo = YouTube(Youtube_link) 
        videoStream = getVideo.streams.first() 
        videoStream.download(download_Folder) 
        messagebox.showinfo("downloaded successfully! ;)",  
                            "saved in\n" 
                            + download_Folder) 
    def do_popup1(event):
        try:
            s.tk_popup(event.x_root,event.y_root)
        finally:
            s.grab_release()
    
    def paste1(input):
        input0=input
        input1=entry_link.clipboard_get()
        video_Link.set(input0+input1)

    yout_bt=PhotoImage(file="icons/youtube1.png")
    im_youtube=Label(youtube_window,image=yout_bt)
    im_youtube.place(x=450,y=10)

    link_label = Label(youtube_window,  text="YouTube link", fg="black",font=("Times", "10","bold")) 
    link_label.place(x=10,y=80)
   
    youtube_link = Entry(youtube_window, width=30,textvariable=video_Link,bg="white",font=6) 
    youtube_link.place(x=100,y=80) 
    
    destination_label = Label(youtube_window,  text="Save as    ", fg="black",font=("Times", "10","bold")) 
    destination_label.place(x=10,y=110)

    attention_label=Label(youtube_window,text="This process may take some time, have patience! ;)",fg="orange red")
    attention_label.place(x=35,y=155)

   
    destinationText = Entry(youtube_window, width=30,textvariable=download_Path,bg="white",font=6) 
    destinationText.place(x=100,y=110) 
   
    browse_B = Button(youtube_window,  text="Browse", command=Browse, width=10, bg="dark cyan",fg="black",font=("Times", "8","bold")) 
    browse_B.place(x=450,y=112) 
    Download_B = Button(youtube_window, text="Download",  command=Download,  width=15, bg="yellow green",font=("Times", "9","bold")) 
    Download_B.place(x=415,y=145)  
    att_bt=PhotoImage(file="icons/attention.png")
    im_youtube=Label(youtube_window,image=att_bt)
    im_youtube.place(x=10,y=150)



    s=Menu(youtube_window,tearoff=0)
    s.add_command(label="Copy", command=lambda: copy(entry_link.get()))
    s.add_command(label="Cut",command=lambda:cut(entry_link.get()))
    s.add_command(label="Paste",command=lambda:paste1(entry_link.get()))
    s.add_separator()
    youtube_link.bind("<Button-3>", do_popup1)
    youtube_window.mainloop()
    

    

menu_file.add_command(label="Clear",command=clear)
menu_file.add_separator()
menu_file.add_command(label="Exit",command=root.destroy)

menu_edit.add_command(label="Cut",command=lambda: cut(entry_link.get()))
menu_edit.add_separator()
menu_edit.add_command(label="Copy",command=lambda: copy(entry_link.get()))
menu_edit.add_separator()
menu_edit.add_command(label="Paste",command=lambda: paste(entry_link.get()))
menu_edit.add_separator()

menu_download.add_command(label="Stop",command=lambda: cancel())
menu_download.add_separator()
menu_download.add_command(label="Pause/Resume",command=lambda: pause_resume(objectt))


frame_input=Frame(root,relief=RIDGE,bg="medium sea green")
frame_input.pack(fill=BOTH)

frame_buttons=LabelFrame(root,relief=FLAT,bg="medium sea green")
frame_buttons.pack(fill=BOTH)


frame_status=LabelFrame(root,relief=FLAT,bg="alice blue")
frame_status.pack(fill=BOTH)
 
frame_progress=Frame(root,relief=FLAT,bg="medium sea green")
frame_progress.pack(fill=BOTH,expand=1)


label_status=Label(frame_status,textvariable=status_message,justify=LEFT,fg="red",font=("Andalus", "12","bold"))
label_status.grid(row=1,column=1,sticky=W)

label_size=Label(frame_status,textvariable=size_message,justify=LEFT,fg="black",font=("Andalus", "11","bold"))
label_size.grid(row=3,column=1,sticky=W)

label_time=Label(frame_status,textvariable=time_message,justify=LEFT,fg="black",font=("Andalus", "11","bold"))
label_time.grid(row=4,column=1,sticky=W)

label_destination= Label(frame_status,textvariable=destination_message,justify=LEFT,fg="black",font=("Andalus", "11","bold"))
label_destination.grid(row=5,column=1,sticky=W)


progress=ttk.Progressbar(frame_progress,orient=HORIZONTAL,length=100,mode="determinate")
progress.pack(fill=X,padx=35,pady=44)
speed_bt=PhotoImage(file="icons/speed.png")
im5=Label(frame_progress,image=speed_bt)
im5.place(x=365,y=5)

label_link=Label(frame_input,text="URL Address",fg="black",bg="medium sea green",font=("Andalus", "15","bold"))
label_link.pack(pady=5)

entry_link=Entry(frame_input,textvariable=input_link,font=('Mono',"13","bold"))
entry_link.pack(fill=X,side=TOP,padx=110)

label_link1=Label(frame_input,text="Save As",fg="black",bg="medium sea green",font=("Andalus", "15","bold"))
label_link1.pack(pady=10)

entry_link2=Entry(frame_input,textvariable=download_paths,font=('Mono',"13","bold"),width=40)
entry_link2.pack(side=TOP,padx=110)

browse=tk.Button(frame_input,text="Browse",command=lambda:Browse(),width=14,bg="white",fg="black",font=("Times", "10","bold"))
browse.place(x=583,y=127)


button_download=tk.Button(frame_buttons,text="Download",command=lambda:start_downloading(),width=14,bg="beige",fg="black",font=("Times", "10","bold"))
button_download.grid(row=0,column=1,padx=40,pady=50)
start_bt=PhotoImage(file="icons/download.png")
im1=Label(frame_buttons,image=start_bt)
im1.place(x=75,y=10)

button_clear=Button(frame_buttons,text="Clear All",command=lambda: clear(),width=14,fg="black",bg="beige",font=("Times", "10","bold") )
button_clear.grid(row=0,column=2)
clear_bt=PhotoImage(file="icons/clear1.png")
im2=Label(frame_buttons,image=clear_bt)
im2.place(x=225,y=10)

Button_youtube=Button(frame_buttons, text='Youtube', command=lambda:openyoutube(),width=14,bg="beige",fg="black",font=("Times", "10","bold"))
Button_youtube.grid(row=0,column=3,padx=40)
open_youtube=PhotoImage(file="icons/youtube.png")
imy=Label(frame_buttons,image=open_youtube)
imy.place(x=372,y=10)


button_open=Button(frame_buttons,text="Open Downloads", command=lambda: browsing(),width=14,bg="beige",fg="black",font=("Times", "10","bold") )
button_open.grid(row=0,column=4)
open_bt=PhotoImage(file="icons/open.png")
im2=Label(frame_buttons,image=open_bt)
im2.place(x=520,y=10)

button_exit=Button(frame_buttons,text="Exit",command=lambda: Exit(),width=14,bg="beige",fg="black",font=("Times", "10","bold"))
button_exit.grid(row=0,column=5,padx=40,pady=50)
Exit_bt=PhotoImage(file="icons/Exit.png")
im2=Label(frame_buttons,image=Exit_bt)
im2.place(x=665,y=10)

button_pause=Button(frame_progress,state=DISABLED,text="Pause",width=15,fg="red",font=("Times", "10","bold"))
button_pause.place(x=220,y=80)

button_stop=Button(frame_progress,state=DISABLED,text="Cancel",width=15,fg="blue",font=("Times", "10","bold"))
button_stop.place(x=420,y=80)

label_details=Label(frame_status,text="Details",fg="black",bg="alice blue",font=("Andalus", "15","bold"))
label_details.place(x=355)
detail_bt=PhotoImage(file="icons/detail.png")
im5=Label(frame_status,image=detail_bt)
im5.place(x=420,y=5)

m=Menu(root,tearoff=0)
m.add_command(label="Copy", command=lambda: copy(entry_link.get()))
m.add_command(label="Cut",command=lambda:cut(entry_link.get()))
m.add_command(label="Paste",command=lambda:paste(entry_link.get()))
m.add_separator()
m.add_command(label="cancel",command=m.forget)
entry_link.bind("<Button-3>", do_popup)

root.mainloop()