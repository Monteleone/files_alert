################################################################
#                                                              #
#                                                              #
#                     Email Alert v. 1.0                       #
#                                                              #
################################################################


import tkinter as tk
from tkinter import Menu
from tkinter import font as tkfont
from tkinter import filedialog

from functools import partial
import time
import os
import ctypes
import logging
import pyautogui
import threading
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
from watchdog.events import PatternMatchingEventHandler
import sys
from screeninfo import get_monitors
 
class Watchdog(PatternMatchingEventHandler, Observer):
    def __init__(self, path='.', patterns='*', logfunc="", new_counter = 0):
        PatternMatchingEventHandler.__init__(self, patterns)
        Observer.__init__(self)
        self.schedule(self, path=path, recursive=False)
        self.log = logfunc
        self.new_counter = new_counter  # Store the counter as an instance variable
        self.path = path
        self.popup_open = False
        self.popup = None
        self.message_label = ""


        selected_monitor = get_monitors()[0]
        screen_width = selected_monitor.width
        screen_height = selected_monitor.height

        # Ottieni le dimensioni della taskbar
        taskbar_height = ctypes.windll.user32.GetSystemMetrics(2)  # SM_CYSCREEN
        # Calcola la posizione della finestra popup
        self.popup_width = 200
        self.popup_height = 50
        self.popup_x = screen_width - self.popup_width - 20
        self.popup_y = screen_height - taskbar_height - self.popup_height - 20



    def on_created(self, event):
        # This function is called when a file is created
        self.log("hey, {event.src_path} has been created!")
        # Iterate directory
        count = 0
        for p in os.listdir(self.path):
            # check if current path is a file
            if os.path.isfile(os.path.join(self.path, p)):
                count += 1
        self.new_counter = count


        # Call notify to create a new popup or update the existing one
        self.notify("Ci sono nuovi file.\n " + str(self.new_counter) + " in totale.")
        

    def on_deleted(self, event):
        # This function is called when a file is deleted
        pass

    def on_modified(self, event):
        # This function is called when a file is modified
        pass

    def on_moved(self, event):
        # This function is called when a file is moved    
        pass

    def get_counter(self):
        return(self.new_counter)



    def notify(self, message="Hello World!", image=None, command=None):
        def on_click(event=None):
            if command: 
                command()
            self.popup.withdraw()  # Nascondi la finestra invece di distruggerla
            self.popup_open = False     
            
        if  not self.popup_open:
            self.popup_open = True
            self.popup = tk.Toplevel(bg='yellow', relief=tk.RAISED, bd=3)
            self.popup.overrideredirect(True)
            self.popup.geometry("{}x{}+{}+{}".format(self.popup_width, self.popup_height, self.popup_x, self.popup_y))
            self.popup.deiconify()  # Riporta la finestra alla visibilità

            if isinstance(image, str):
                image = tk.PhotoImage(file=image)
                self.popup.ref = image

            if image:
                lbl = tk.Label(self.popup, image=image)
                lbl.pack(side=tk.LEFT)
                lbl.bind('<1>', on_click)


            self.message_label = tk.Message(self.popup, bg='yellow', fg='black', border=2, text=message)
            self.message_label.pack()
            self.message_label.bind('<1>', on_click)
        
            self.popup.bind('<1>', on_click)

            self.popup.attributes('-topmost', True)
            self.popup.lift()
        else:
            # Se la finestra popup è già aperta, aggiorna solo il testo del messaggio
            self.message_label.config(text=message)
 
 

class GUI:
    def __init__(self):

        #CONFIG WATCHDOG
        self.watchdog = None
        self.watch_path = "path da monitorare"
        self.start_watchdog()
        self.old_count = 0
        self.new_count = 0

        #CONFIG GUI
        self.root = tk.Tk()
        self.root.title('Files Alert')

        # Imposta l'icona della finestra
        icon_path = "./imgs/notification.ico"  # Sostituisci con il percorso reale dell'icona
        self.root.iconbitmap(icon_path)


        self.create_menu()

        #setting window size
        width=584
        height=212
        screenwidth = self.root.winfo_screenwidth()
        screenheight = self.root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.root.geometry(alignstr)
        self.root.resizable(width=False, height=False)

        GLabel_469=tk.Label(self.root)
        ft =tkfont.Font(family='Times',size=18)
        GLabel_469["font"] = ft
        GLabel_469["fg"] = "#333333"
        GLabel_469["justify"] = "center"
        GLabel_469["text"] = "FILES ALERT "
        GLabel_469["relief"] = "flat"
        GLabel_469.place(x=130,y=40,width=303,height=56)

        # Aggiungi un'immagine accanto alla label
        img = tk.PhotoImage(file="./imgs/icon_alert.png") 
        img = img.subsample(12, 12)  
        GLabel_469.img = img  
        GLabel_469.configure(image=img, compound=tk.LEFT) 


        GLabel_798=tk.Label(self.root)
        ft = tkfont.Font(family='Times',size=10)
        GLabel_798["font"] = ft
        GLabel_798["fg"] = "#333333"
        GLabel_798["justify"] = "center"
        GLabel_798["text"] = "Label"
        GLabel_798.place(x=170,y=110,width=220,height=33)
 


        self.root.mainloop()

    def create_menu(self):
    
        # create a menu
        menubar = Menu(self.root)
        file_menu = Menu(menubar, tearoff="off")

        # add a menu item to the menu
        file_menu.add_command(
            label='Cambia percorso file',
            compound='left', 
            underline=0,
            command=self.changePathWindow
        )

        # add a menu item to the menu
        file_menu.add_command(
            label='Exit',
            compound='left', 
            underline=0,
            command=self.root.destroy
        )

        # add the File menu to the menubar
        menubar.add_cascade(
            label="File",
            menu=file_menu
        )
 
        self.root.config(menu=menubar)



       

    def changePathWindow(self):
        # create child window
        win = tk.Toplevel()
        win.grab_set()
        #setting title
        win.title("Cambia Percorso File")

        # Imposta l'icona della finestra
        icon_path = "./imgs/notification.ico"  # Sostituisci con il percorso reale dell'icona
        win.iconbitmap(icon_path)


        #setting window size
        width=584
        height=212
        screenwidth = win.winfo_screenwidth()
        screenheight = win.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        win.geometry(alignstr)
        win.resizable(width=False, height=False)

        GLabel_138=tk.Label(win)
        GLabel_138["bg"] = "#fad400"
        GLabel_138["cursor"] = "arrow"
        ft = tk.font.Font(family='Times',size=10)
        GLabel_138["font"] = ft
        GLabel_138["fg"] = "#333333"
        GLabel_138["justify"] = "center"
        GLabel_138["text"] = "seleziona la cartella che vuoi osservare"
        GLabel_138.place(x=20,y=80,width=390,height=30)

        label_emails_path=tk.Label(win)
        ft = tk.font.Font(family='Times',size=10)
        label_emails_path["font"] = ft
        label_emails_path["fg"] = "#333333"
        label_emails_path["justify"] = "center"
        label_emails_path["text"] = "Percorso file"
        label_emails_path["relief"] = "ridge"
        label_emails_path.place(x=20,y=40,width=400,height=30)

        btn_sfoglia_path=tk.Button(win)
        btn_sfoglia_path["bg"] = "#f0f0f0"
        ft = tk.font.Font(family='Times',size=10)
        btn_sfoglia_path["font"] = ft
        btn_sfoglia_path["fg"] = "#000000"
        btn_sfoglia_path["justify"] = "center"
        btn_sfoglia_path["text"] = "Scegli"
        btn_sfoglia_path.place(x=440,y=80,width=106,height=35)
        btn_sfoglia_path["command"] = lambda: self.getFolderPath(label_emails_path)
 


    def getFolderPath(self, label):
        label['text'] = self.watch_path
        folder_selected = filedialog.askdirectory(title="Scegli il percorso")
        if folder_selected:
            label['text'] = folder_selected
            self.watch_path = folder_selected
            #fermo il servizio e lo riavvio con il nuovo path
            self.stop_watchdog()
            self.start_watchdog()
        else:
            pass



    def start_watchdog(self):
        if self.watchdog is None:
            self.watchdog = Watchdog(path=self.watch_path, logfunc=self.log)
            self.watchdog.start()
            self.log('Watchdog started')
        else:
            self.log('Watchdog already started')

    def stop_watchdog(self):
        if self.watchdog:
            self.watchdog.stop()
            self.watchdog = None
            self.log('Watchdog stopped')
        else:
            self.log('Watchdog is not running')

    def select_path(self):
        path = filedialog.askdirectory()
        if path:
            self.watch_path = path
            self.log('Selected path: {path}')

    def log(self, message):

        print(self.watch_path)
        print(message)


if __name__ == '__main__':
    GUI()