import sublime, sublime_plugin
import subprocess

class HamsterStopCommand(sublime_plugin.WindowCommand):
	def run(self):
		#check if we really to cancel the activity
		cancel = sublime.ok_cancel_dialog("Are you sure you want to stop tracking the current activity?")
		if cancel is True:
			#use hamster-cli to stop the current activity
			process = subprocess.Popen(["hamster-cli", "stop"])
			

class HamsterStartCommand(sublime_plugin.WindowCommand):
	def run(self):
		window = sublime.active_window()
		window.show_input_panel("caption", "initial_text", self._on_done, None, self._on_cancel)

	def _on_cancel(self):
		#nothing to do here, so simple return false
		return False

	def _on_done(self, str):
		#use hamster-cli to start a new activity
		#str can support the format: activity@category,tags notes
		process = subprocess.Popen(["hamster-cli", "start", str])
		return True
