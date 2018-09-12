import sublime
import sublime_plugin
import json
import os
import pprint

import sshfs.config

# Показать список в новом окне
def show_qp(window, choices, on_done):
	def show_timeout():
		window.show_quick_panel(choices, on_done)
	sublime.set_timeout(show_timeout, 10)

def get_view_by_group_index(window, group, index):
	return window.views_in_group(group)[index]

class OpenInConsoleCommand(sublime_plugin.TextCommand):
	def run(self, files, dirs):
		file_path = sublime.packages_path() + '/sshfs/sshfs.sublime-settings';
		with open(file_path) as file:
			config = json.load(file)

		server = getServerByDir(dirs[0])
		if server != None:
			mount_path = sublime.packages_path() + '/sshfs/mnt/' + server['name']
			dir = dir.replace(mount_path, '')
			dir = server['path'] + dir
			os.system('ssh -t ' + server['user'] + '@' + server['host'] +
				       '"cd ' + dir + '; bash"')

			# Команда должна быть вида
			# gnome-terminal -e "bash -c \"sshpass -p passwd ssh -t user@host 'cmd && bash'\"; exec bash;"

			cmd = "gnome-terminal -e \"bash -c \\\""
			cmd += "sshpass -p " + server['passwd']
			cmd += " ssh -o StrictHostKeyChecking=no -t "
			cmd += server['user'] + '@' + server['host']
			cmd += " 'cd " + dir + " && pwd && bash'\\\";"
			cmd += "exec bash; \""

			os.system(cmd)

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
			mount_path = '"' + sublime.packages_path() + '/sshfs/mnt/' + server['name'] + '"'
			print(mount_path)
			os.system('mkdir -p ' + mount_path)
			os.system('fusermount -uz ' + mount_path)
			print('echo "' + server['passwd'] + '" | sshfs ' + server['user'] + '@' + server['host'] + ':' + server['path'] + ' ' + mount_path + ' -o password_stdin')
			os.system('echo "' + server['passwd'] + '" | sshfs ' + server['user'] + '@' + server['host'] + ':' + server['path'] + ' ' + mount_path + ' -o password_stdin')
			os.system(sublime.executable_path() + ' ' + mount_path + ' -a')
			print(sublime.executable_path() + ' ' + mount_path + ' -a')
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
			choices.append([server['name'], server['user'] + '@' + server['host']])
		# choices.insert(0, ['Добавить новый сервер...', ''])

		self.window = sublime.active_window()
		self.window_id = self.window.id()

		show_qp(self.window, choices, self.on_done)

class EventListener(sublime_plugin.EventListener):
	def on_window_command(self, view, command_name, args):
		if command_name == 'remove_folder':
			# Получаем путь закрытой папки
			dir = args['dirs'][0]

			server = getServerByDir(dir)
			if server != None:
				mount_path = '"' + sublime.packages_path() + '/sshfs/mnt/' + server['name'] + '"'
				os.system('fusermount -uz ' + mount_path)
				print('Закрыта папка сервера ' + server['name'])
