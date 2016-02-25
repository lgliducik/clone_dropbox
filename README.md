# clone_dropbox
запуск сервера 
            cd /server
			зайти в виртуальное окружение my_venv\Scripts\activate
		    python server.py -s 'filesystem'
			логирование в файле logging.log
запуск клиента
            cd /client
			зайти в виртуальное окружение my_venv\Scripts\activate
			python dropbox_clon_main.py -f folder1 -l lida -p 123
			логирование в файле logging.log
