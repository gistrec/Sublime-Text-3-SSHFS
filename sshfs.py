import sublime
import sublime_plugin
import json

# Показать список в новом окне
def show_qp(window, choices, on_done):
	def show_timeout():
		window.show_quick_panel(choices, on_done)
	sublime.set_timeout(show_timeout, 10)


class ServersShowCommand(sublime_plugin.TextCommand):
	window = None
	window_id = None
	servers = None

	# Получаем индекс выбранного пункта
	def on_done(self, index):
		# Ничего не выбрано
		if index == -1:
			return
		# elif index == 0:
		#
		#    return
		else:
			server = self.servers[index]
			# TODO!
			return

	def run(self, edit):
		# Открываем файл с данными серверов
		file_path = sublime.packages_path() + '/sshfs/sshfs.sublime-settings';
		with open(file_path) as file:
			config = json.load(file)

		# Массив, который будет выводиться в окне
		choices = []

		self.servers = servers = []

		for server in config:
			servers.append(server)
			choices.append([server['user'] + '@' + server['name'], server['host']])
		# choices.insert(0, ['Добавить новый сервер...', ''])

		self.window = sublime.active_window()
		self.window_id = self.window.id()

		show_qp(self.window, choices, self.on_done)
