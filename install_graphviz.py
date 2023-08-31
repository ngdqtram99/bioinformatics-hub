import platform
import subprocess
import requests
from zipfile import ZipFile
from pathlib import Path

def install_graphviz():

    system = platform.system().lower()

    if system == "windows":
        url = "https://gitlab.com/api/v4/projects/4207231/packages/generic/graphviz-releases/8.1.0/windows_10_msbuild_Release_graphviz-8.1.0-win32.zip"
        response = requests.get(url)
        with open("graphviz.zip", "wb") as zip_file:
            zip_file.write(response.content)
        
        with ZipFile("graphviz.zip", "r") as zip_ref:
            zip_ref.extractall("graphviz")
        Path("graphviz.zip").unlink()
        update_settings()
        print("Graphviz wurde erfolgreich installiert und zu PATH hinzugefügt")
    elif system == "linux":
        subprocess.run(["sudo", "apt-get", "install", "graphviz"], check=True)
        print("Graphviz wurde erfolgreich installiert.")
    else:
        print("graphviz konnte auf Ihrem System nicht automatisch installiert werden. Besuchen Sie https://graphviz.org/download/ und installieren Sie bitte graphviz auf Ihrem System")

def update_settings():
    settings_path = "swtp/settings.py"  
    
    with open(settings_path, "r") as f:
        lines = f.readlines()

    with open(settings_path, "w") as f:
        exists = False
        for line in lines:
            if line.startswith('os.environ["Path"] += os.pathsep + os.path.abspath("graphviz/Graphviz/bin")'):
                exists = True
                print('PATH für graphviz ist in settings.py bereits definiert')
                f.write(line)
            else:
                f.write(line)

        if not exists:
            f.write("\n# Graphviz Settings\n")
            f.write('os.environ["Path"] += os.pathsep + os.path.abspath("graphviz/Graphviz/bin")\n')

if __name__ == "__main__":
    install_graphviz()
    
