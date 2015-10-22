# clone_dropbox
запуск сервера 
            cd /server
			зайти в виртуальное окружение my_venv\Scripts\activate
		    python server.py
			логирование в файле logging.log
запуск клиента
            cd /client
			зайти в виртуальное окружение my_venv\Scripts\activate
			python dropbox_clon_main.py -f <имя_папки> -l <логин> -p <пароль>
			логирование в файле logging.log
