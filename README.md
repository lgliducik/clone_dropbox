# Clone dropbox
Web application for save your files on the server and share between many clients.

## run
```

virtualenv .venv
. .venv/bin/activate
pip install -r requirements.txt
cd server
python server.py -s 'filesystem'
python server.py -s 'cloud'
cd client
python dropbox_clon_main.py -f folder1 -l lida -p 123
```
