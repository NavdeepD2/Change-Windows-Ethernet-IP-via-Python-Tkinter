import tkinter as tk
from threading import Thread
import subprocess
import ctypes
import sys

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def check_connection():
    try:
        # CMD command to ping
        cmd = 'ping -n 1 136.1.1.100'
        result = subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if result.returncode == 0:
            label.config(text="ZTE OLT IP: Connected", fg="green")
        else:
            label.config(text="ZTE OLT IP: Not Connected", fg="red")
    except Exception as e:
        print("An error occurred:", e)

def clear_ip():
    if not is_admin():
        # Re-run the script as administrator
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
        sys.exit()

    try:
        # PowerShell command to enable DHCP
        cmd = 'powershell.exe Get-NetAdapter -Name "Ethernet 2" | Set-NetIPInterface -Dhcp Enabled'
        subprocess.run(cmd, shell=True)
        print("IP settings cleared successfully.")
    except Exception as e:
        print("An error occurred:", e)

def set_zte_olt_ip():
    try:
        # CMD command to set static IP address
        cmd = 'netsh.exe interface ip set address name="Ethernet 2" static 136.1.1.99 255.255.0.0'
        subprocess.run(cmd, shell=True)
        print("ZTE OLT IP set successfully.")
    except Exception as e:
        print("An error occurred:", e)

def run_check_loop():
    while True:
        check_connection()
        root.after(2000, check_connection)  # Check connection every 5 seconds

# Create the main window
root = tk.Tk()
root.title("Network Configuration")

# Center the window
window_width = 300
window_height = 200
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 2) - (window_height // 2)
root.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Create buttons
clear_ip_button = tk.Button(root, text="Clear IP", command=clear_ip, width=20, height=2)
clear_ip_button.pack(pady=10)

zte_olt_ip_button = tk.Button(root, text="ZTE OLT IP", command=set_zte_olt_ip, width=20, height=2)
zte_olt_ip_button.pack(pady=10)

# Create label for connection status
label = tk.Label(root, text="Checking connection...", font=("Arial", 12))
label.pack(pady=10)

# Create footer label
footer_label = tk.Label(root, text="Developed by D2 Automation | Navdeep Singh", font=("Arial", 8), fg="gray")
footer_label.pack(side="bottom", pady=5)

# Start a thread to continuously check connection
thread = Thread(target=run_check_loop)
thread.daemon = True
thread.start()

# Run the GUI
root.mainloop()
