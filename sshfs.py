import sublime
import sublime_plugin


class ServersShowCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		print("Показать все сервера")
    # TODO!

class ServersEditCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		print("Отредактировать сервера")
    # TODO!
