# clone_dropbox
������ ������� 
            cd /server
			����� � ����������� ��������� my_venv\Scripts\activate
		    python server.py -s 'filesystem'
			python server.py -s 'cloud'
			����������� � ����� logging.log
������ �������
            cd /client
			����� � ����������� ��������� my_venv\Scripts\activate
			python dropbox_clon_main.py -f folder1 -l lida -p 123
			����������� � ����� logging.log
