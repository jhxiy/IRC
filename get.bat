curl https://www.python.org/ftp/python/3.9.6/python-3.9.6.exe -o python.exe
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
curl https://raw.githubusercontent.com/jhxiy/IRC/main/irc_client.py -o irc_client.py
curl https://raw.githubusercontent.com/jhxiy/IRC/main/py_install.bat -o py_install.bat
curl https://raw.githubusercontent.com/jhxiy/IRC/main/pip_install.bat -o pip_install.bat
start py_install.bat
timeout 300
start pip_install.bat
timeout 100
start run.bat
