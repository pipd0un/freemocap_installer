import wget
import subprocess, 



pipPath = str()

def installPip():
    res = subprocess.run(['python/python.exe', 'getpip.py'], stdout=subprocess.PIPE, text=True)
    resultString = res.stdout.splitlines()[-1]
    print()
    return resultString

def installConda():
    res = subprocess.run(['Scripts/pip.exe', 'install', 'conda'], stdout=subprocess.PIPE, text=True)
    resultString = res.stdout.splitlines()[-1]
    print()
    return resultString

if __name__ == "__main__":
    # isPipInstalled = installPip()
    # print(isPipInstalled)

    # isCondaInstalled = installConda()
    # print(isCondaInstalled)

    res = subprocess.run(['Scripts/pip.exe', 'install', '-r', 'freemocap/requirements.txt'], stdout=subprocess.PIPE, text=True)
    resultString = res.stdout
    print(resultString)
    with subprocess.Popen(['Scripts/pip.exe', 'install', '-r', 'freemocap/requirements.txt'], stdout=PIPE) as proc:
    log.write(proc.stdout.read())
    

    



