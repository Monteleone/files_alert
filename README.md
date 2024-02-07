

<center><img src="https://github.com/Monteleone/files_alert/blob/main/icon_alert.png" width="48"></center>

This Python code creates a GUI (Graphical User Interface) application called "Files Alert" that allows users to monitor a specific directory for the addition of new files and receive a desktop notifications when that happens. 
The popup notification alerting the user when new files have been added to the monitored directory is created using the Tkinter library. This choice was made because if the event were managed by the Windows notification manager, the notification would disappear after a few seconds. Instead, the desired behavior is for the notification to remain on the screen until the user clicks on it to dismiss it.



The code starts with importing necessary Python modules for:
- GUI (Tkinter);
- file handling (os);
- image manipulation (pyautogui);
- file monitoring (watchdog), and others.


**Watchdog Class**: This class extends PatternMatchingEventHandler and Observer classes from the watchdog module. It handles monitoring files in a specific directory and notifies users when new files are added.

**Watchdog Methods**: It includes methods to handle events like file creation, modification, deletion, or movement. When a new file is created, a notification is displayed.

**GUI Class**: This class manages the graphical interface of the application. It uses Tkinter to create a main window with a menu and options to change the path of the files to monitor.

**GUI Methods**: It includes methods to create the menu, manage the dialog window for changing the file path, and start/stop the file monitoring service.

**Main Function**: It starts the GUI application.


To make the code work, the user needs to follow these steps:

 1. Ensure Python is installed on the system. Install required Python
    packages using pip. This includes: Tkinter watchdog screeninfo
    
 2. Ensure the necessary images (e.g., notification.ico, icon_alert.png)
    are available in the specified paths or modify the paths
    accordingly.
 3. Set the desired directory to monitor by changing the
    self.watch_path variable in the GUI class to the desired directory
    path.
 4. Run the Python script. The application window "Files Alert"
    will appear. 
 5. Use the File menu to change the file path to monitor or
    exit the application. 
 6. When a new file is created in the monitored directory, a notification will pop up displaying the number of new files. Close the notification window to dismiss the alert.

 
