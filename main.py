import tkinter as tk
from tkinter import filedialog
import subprocess
import os

launcherStr = \
"""
import subprocess

#activating env
command = ["{}\\condabin\\conda.bat", "activate", "freemocap-gui"]  
subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

#run script with using conda's python
subprocess.run(["{}\\envs\\freemocap-gui\\python.exe", "{}\\freemocap-main\\src\\gui\\main\\main.py"], check=True)
    
"""

class Installer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Freemocap-GUI Installer")
        self.geometry("420x200")
        # self.iconbitmap("freemocap_skelly_logo.ico")

        self.install_button = tk.Button(self, text="Install", command=self.start_installation)
        self.install_button.pack(pady=20, padx=20)

        self.text_area = tk.Text(self)
        self.text_area.pack(fill="both", expand=True)


    def start_installation(self):
        self.install_button.config(state=tk.DISABLED)
        import threading
        self.install_thread = threading.Thread(target=self.install,daemon=True)
        self.install_thread.start()

    def install(self):
        self.startupinfo = subprocess.STARTUPINFO()
        self.startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

        if self.install_button["text"] == "Install":
            def createExec(condapath: str, mainpath: str):

                launcher = open(f"{mainpath}\\launcher.py","w")
                launcher.write(launcherStr.format(condapath,condapath,mainpath).replace("\\","\\\\"))
                launcher.close()

            self.main_path = filedialog.askdirectory().replace("/","\\")
            self.text_area.insert("end", f"Main path chosen: {self.main_path}\n")
            self.text_area.see("end")

            self.condaPath = self.main_path + "\\Miniconda3"

            # Check if conda is already installed
            try:
                subprocess.run([f"{self.condaPath}\\condabin\\conda.bat", "--version"], check=True, capture_output=True, startupinfo=self.startupinfo, creationflags=subprocess.CREATE_NO_WINDOW)
                self.text_area.insert("end", "Conda already installed\n")
            except:
                self.text_area.insert("end", "Conda not found!\n")
                if not os.path.exists(f"{self.main_path}/miniconda.exe"):
                    self.text_area.insert("end", "Downloading Miniconda... \n")
                    subprocess.run(["powershell", "-Command", f"Invoke-WebRequest -Uri https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe -OutFile {self.main_path}/miniconda.exe"], capture_output=True, startupinfo=self.startupinfo, creationflags=subprocess.CREATE_NO_WINDOW)
                
                ## silent install conda
                self.text_area.insert("end", "Installing Miniconda!\n")
                self.text_area.insert("end", "Please wait...\n")
                subprocess.run(f'start /wait "" {self.main_path}/miniconda.exe /InstallationType=JustMe /RegisterPython=0 /S /D=' + f'{self.main_path}' + '\\Miniconda3\\', shell=True, startupinfo=self.startupinfo, creationflags=subprocess.CREATE_NO_WINDOW)

                try:
                    version_check = subprocess.run([f"{self.condaPath}\\condabin\\conda.bat", "--version"], capture_output=True, startupinfo=self.startupinfo, creationflags=subprocess.CREATE_NO_WINDOW)
                    version = version_check.stdout.decode("utf-8").strip()
                    self.text_area.insert("end",f"Conda version {version} installed successfully")
                except:
                    self.text_area.insert("end","Conda installation failed")
                    subprocess.run(f"..\\{self.condaPath}\\Uninstall-Miniconda3.exe /S", shell=True, startupinfo=self.startupinfo, creationflags=subprocess.CREATE_NO_WINDOW)
                    raise Exception("Conda installation failed")

            # Download Freemocap repository
            if not os.path.exists(f"{self.main_path}\\freemocap-main"):
                self.text_area.insert("end", "\nDownloading Freemocap repository...\n")
                subprocess.run(["powershell", "-Command", f"Invoke-WebRequest -Uri https://github.com/freemocap/freemocap/archive/master.zip -OutFile {self.main_path}/freemocap.zip"], capture_output=True, startupinfo=self.startupinfo, creationflags=subprocess.CREATE_NO_WINDOW)
                subprocess.run(["powershell", "-Command", f"Expand-Archive -Path {self.main_path}/freemocap.zip -DestinationPath {self.main_path}"], capture_output=True, startupinfo=self.startupinfo, creationflags=subprocess.CREATE_NO_WINDOW)
            else:
                self.text_area.insert("end", "Freemocap repository already installed...\n")

            #check if env installed before
            if not os.path.exists(f"{self.condaPath}\\envs\\freemocap-gui"):
                # Create virtual environment
                self.text_area.insert("end", "Creating virtual environment...\n")
                try:
                    command = [f"{self.condaPath}\\condabin\\conda.bat", "create", "-n", "freemocap-gui", "python=3.9", "-y"]
                    subprocess.run(command, check=True, startupinfo=self.startupinfo, creationflags=subprocess.CREATE_NO_WINDOW, shell=True)

                except:
                    raise Exception("Creating or activating environment couldn't succeeded!\n")
            else:
                self.text_area.insert("end", "Freemocap-gui Environment already installed...\n")
                
            #check if requirements installed
            command = [f"{self.condaPath}\\envs\\freemocap-gui\\Scripts\\pip.exe", "install", "-r", f"{self.main_path}\\freemocap-main\\requirements.txt"]
            subprocess.run(command, capture_output=True, startupinfo=self.startupinfo, creationflags=subprocess.CREATE_NO_WINDOW)
            self.text_area.insert("end", "Requirements checked!\n")

            #install installer :D :P
            if not os.path.exists(f"{self.condaPath}\\envs\\freemocap-gui\\Scripts\\pyinstaller.exe"):
                command = [f"{self.condaPath}\\envs\\freemocap-gui\\Scripts\\pip.exe", "install", "pyinstaller"]
                subprocess.run(command, capture_output=True, startupinfo=self.startupinfo, creationflags=subprocess.CREATE_NO_WINDOW)
            self.text_area.insert("end", "PyInstaller fetched!\n")

            #creating launcher
            self.text_area.insert("end", "Creating launcher...\n")
            createExec(condapath=self.condaPath, mainpath=self.main_path)

            #py2exe
            cmd = f'{self.condaPath}\\envs\\freemocap-gui\\Scripts\\pyinstaller.exe --onefile -i "{self.main_path}\\freemocap-main\\assets\\logo\\freemocap_skelly_logo.ico" --add-data "{self.main_path}\\freemocap-main\\assets\\logo\\freemocap_skelly_logo.ico;." "{self.main_path}\\launcher.py" --distpath "{self.main_path}"'
            subprocess.run(cmd, check=True, startupinfo=self.startupinfo, creationflags=subprocess.CREATE_NO_WINDOW)

            self.text_area.insert("end", "Installation completed!\n")
            self.text_area.insert("end", "Cleaning caches...\n")
            self.install_button["text"] = "Close!"
            os.remove("launcher.spec")
            os.remove(f"{self.main_path}\\launcher.py")
            os.remove(f"{self.main_path}\\freemocap.zip")
            os.remove(f"{self.main_path}\\miniconda.exe")

            import shutil
            shutil.rmtree("build")
            self.text_area.insert("end", "All Done!\n")
            self.install_button.config(state=tk.NORMAL)
            self.text_area.see("end")

        else:
            self.destroy()
            exit(0)

if __name__ == "__main__":
    installer = Installer()
    installer.mainloop()

