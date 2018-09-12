
# Позволяет получить массив с данными о сервере
# по его названию.
# Возвращает массив или None
def getServerByName(name):
	# Открываем файл с данными о серверах
	file_path = sublime.packages_path() + '/sshfs/sshfs.sublime-settings';
	with open(file_path) as file:
		config = json.load(file)

	# Для всех серверов сверяем название
	for server in config:
		if server['name'] == name:
			return server
	return None

# Позволяет получить массив с данными о сервере
# по пути монтирования сетевого диска
# Возвращает массив или None
def getServerByDir(dir):
	file_path = sublime.packages_path() + '/sshfs/sshfs.sublime-settings';
	with open(file_path) as file:
		config = json.load(file)

	for server in config:
		if server['name'] in dir:
			return server
	return None