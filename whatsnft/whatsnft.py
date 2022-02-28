# interface with whatsapp
import ahk
from time import sleep
from ahk import AHK
from subprocess import Popen
import pywinauto
from pywinauto import Desktop, Application

# ahk = AHK()
# ahk.run_script( r'Run C:\Users\giova\AppData\Local\WhatsApp\WhatsApp.exe' )
# sleep(5)
# ahk.run_script( r'WinActivate, ahk_exe WhatsApp.exe' )
# sleep(5)
# ahk.run_script( r'WinMaximize, ahk_exe WhatsApp.exe' )
# sleep(5)
# ahk.run_script( r'WinMinimize, ahk_exe WhatsApp.exe' )
#ahk.run_script( r'WinClose, ahk_exe WhatsApp.exe' )
#sleep(2)

#Popen(r'C:\Users\giova\AppData\Local\WhatsApp\WhatsApp.exe', shell=True)
app = Application().start(r"C:\Users\giova\AppData\Local\WhatsApp\WhatsApp.exe")
#app = Application().connect(path=r"C:\Users\giova\AppData\Local\WhatsApp\WhatsApp.exe")
dlg = app.top_window()
dlg.wait('visible', timeout=5)
dlg.print_control_identifiers()
#dlg.window(auto_id="equalButton").click()


oi = input()

win = ahk.find_window(title=b'Whatsapp') # Find the opened window
#ahk_exe WhatsApp.exe

#ahk.run_script('Run % "C:\Users\giova\AppData\Local\WhatsApp\WhatsApp.exe"')