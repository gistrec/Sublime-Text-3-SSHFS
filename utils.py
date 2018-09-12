import sublime
import sublime_plugin

# Функция нужна для вывода выпадающего списка
# с севрерами
def show_qp(window, choices, on_done):
	def show_timeout():
		window.show_quick_panel(choices, on_done)
	sublime.set_timeout(show_timeout, 10)