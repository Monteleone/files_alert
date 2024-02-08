import tkinter as tk
from tkinter import Menu, filedialog
from tkinter import font as tkfont
import os
import ctypes
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
from screeninfo import get_monitors





class Watchdog(PatternMatchingEventHandler, Observer):
    def __init__(self, path='.', patterns='*', logfunc="", new_counter = 0, watch_paths=None):
        PatternMatchingEventHandler.__init__(self, patterns)
        Observer.__init__(self)
        self.schedule(self, path=path, recursive=False)
        self.watch_paths = watch_paths
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
        self.popup_width = 250
        self.popup_height = 300
        self.popup_x = screen_width - self.popup_width - 20
        self.popup_y = screen_height - taskbar_height - self.popup_height - 20

    def on_created(self, event):
        directory_parts = self.path.split("\\")
        last_directory = directory_parts[-1] 
        message = "Sono stati inseriti nuovi file in " + last_directory + "\n\n"
        
        for path in self.watch_paths:
            count = 0
            for p in os.listdir(path):
                
                if os.path.isfile(os.path.join(path, p)):
                    if p.lower().endswith('.pdf') or p.lower().endswith('.lnk'):
                        count += 1
                    elif os.path.islink(p):
                        self.log(p)
                        count += 1

            last_directory = os.path.basename(path) 
            message += "In {} sono presenti nr. {} file\n".format(last_directory, count)
        self.notify(message)

        
 
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
        return self.new_counter

    def notify(self, message="Hello World!", image=None, command=None):
        def on_click(event=None):
            if command: 
                command()
            self.popup.withdraw()  # Nascondi la finestra invece di distruggerla
            self.popup_open = False     

 
        if not self.popup_open:
            self.popup_open = True
            self.popup = tk.Toplevel(bg='green', relief=tk.RAISED, bd=3)
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

            self.message_label = tk.Message(self.popup, bg='green', fg='black', border=2, text=message, width=250,
                                 font=("Times New Roman", 12))

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
        # CONFIG WATCHDOG
        self.watchdogs = []  # Lista per tenere traccia dei watchdog
        self.watch_paths = ["path0",
                                "path1",
                                "path2",
                                "path3",
                                "path4",
                                "path5"]
        self.start_watchdogs()
        self.old_counts = [0] * len(self.watch_paths)
        self.new_counts = [0] * len(self.watch_paths)

        # CONFIG GUI
        self.root = tk.Tk()
        self.root.title('Files Alert')

        # Imposta l'icona della finestra
        icon_path = "./imgs/notification.ico"  # Sostituisci con il percorso reale dell'icona
        self.root.iconbitmap(icon_path)

        self.create_menu()

        # Imposta la finestra principale
        width = 584
        height = 212
        screenwidth = self.root.winfo_screenwidth()
        screenheight = self.root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % ((width, height, (screenwidth - width) / 2, (screenheight - height) / 2))
        self.root.geometry(alignstr)
        self.root.resizable(width=False, height=False)

        GLabel_469 = tk.Label(self.root)
        ft = tkfont.Font(family='Times', size=18)
        GLabel_469["font"] = ft
        GLabel_469["fg"] = "#333333"
        GLabel_469["justify"] = "center"
        GLabel_469["text"] = "FILES ALERT "
        GLabel_469["relief"] = "flat"
        GLabel_469.place(x=130, y=40, width=303, height=56)

        # Aggiungi un'immagine accanto alla label
        img = tk.PhotoImage(file="./imgs/icon_alert.png")
        img = img.subsample(12, 12)
        GLabel_469.img = img
        GLabel_469.configure(image=img, compound=tk.LEFT)

        GLabel_798 = tk.Label(self.root)
        ft = tkfont.Font(family='Times', size=10)
        GLabel_798["font"] = ft
        GLabel_798["fg"] = "#333333"
        GLabel_798["justify"] = "center"
        GLabel_798["text"] = "Label"
        GLabel_798.place(x=170, y=110, width=220, height=33)

        self.root.mainloop()

    def create_menu(self):
        # crea un menu
        menubar = Menu(self.root)
        file_menu = Menu(menubar, tearoff="off")

        # aggiungi un elemento di menu al menu
        file_menu.add_command(
            label='Cambia percorso file',
            compound='left',
            underline=0,
            command=self.changePathWindow
        )

        # aggiungi un elemento di menu al menu
        file_menu.add_command(
            label='Exit',
            compound='left',
            underline=0,
            command=self.root.destroy
        )

        # aggiungi il menu File al menubar
        menubar.add_cascade(
            label="File",
            menu=file_menu
        )

        self.root.config(menu=menubar)

    def changePathWindow(self):
        # crea una finestra figlia
        win = tk.Toplevel()
        win.grab_set()
        # impostazione del titolo
        win.title("Cambia Percorso File")

        # Imposta l'icona della finestra
        icon_path = "./imgs/notification.ico"  # Sostituisci con il percorso reale dell'icona
        win.iconbitmap(icon_path)

        # impostazione delle dimensioni della finestra
        width = 584
        height = 212
        screenwidth = win.winfo_screenwidth()
        screenheight = win.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % ((width, height, (screenwidth - width) / 2, (screenheight - height) / 2))
        win.geometry(alignstr)
        win.resizable(width=False, height=False)

        # Itera attraverso i percorsi di monitoraggio e crea elementi GUI per ciascuno
        for i, path in enumerate(self.watch_paths):
            GLabel = tk.Label(win)
            GLabel["bg"] = "#fad400"
            GLabel["cursor"] = "arrow"
            ft = tk.font.Font(family='Times', size=10)
            GLabel["font"] = ft
            GLabel["fg"] = "#333333"
            GLabel["justify"] = "center"
            GLabel["text"] =  "Seleziona la cartella per il percorso {}".format(i + 1)
            GLabel.place(x=20, y=40 + i * 40, width=390, height=30)

            label_path = tk.Label(win)
            ft = tk.font.Font(family='Times', size=10)
            label_path["font"] = ft
            label_path["fg"] = "#333333"
            label_path["justify"] = "center"
            label_path["text"] = path
            label_path["relief"] = "ridge"
            label_path.place(x=20, y=80 + i * 40, width=400, height=30)

            btn_browse_path = tk.Button(win)
            btn_browse_path["bg"] = "#f0f0f0"
            ft = tk.font.Font(family='Times', size=10)
            btn_browse_path["font"] = ft
            btn_browse_path["fg"] = "#000000"
            btn_browse_path["justify"] = "center"
            btn_browse_path["text"] = "Scegli"
            btn_browse_path.place(x=440, y=80 + i * 40, width=106, height=35)
            btn_browse_path["command"] = partial(self.getFolderPath, i, label_path)

    def getFolderPath(self, index, label):
        folder_selected = filedialog.askdirectory(title="Scegli il percorso")
        if folder_selected:
            label['text'] = folder_selected
            self.watch_paths[index] = folder_selected
            # Ferma e riavvia il servizio per aggiornare il percorso
            self.stop_watchdogs()
            self.start_watchdogs()

    def start_watchdogs(self):
        for path in self.watch_paths:
            watchdog = Watchdog(path=path, logfunc=self.log, watch_paths = self.watch_paths)
            watchdog.start()
            self.watchdogs.append(watchdog)
            self.log('Watchdog started for path: {}'.format(path))

    def stop_watchdogs(self):
        for watchdog in self.watchdogs:
            watchdog.stop()
            self.watchdogs.remove(watchdog)
            self.log('Watchdog stopped'.format())

    def log(self, message):
        print(message)


if __name__ == '__main__':
    GUI()
