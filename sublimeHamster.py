# Copyright (c) 2013 Robin Malburn
# See the file license.txt for copying permission.

import sublime, sublime_plugin
import subprocess
import json

def hamster_cli_start(str):
	"""Start the new activity str.  Str supports the format:
	activity@category[description, [#tags #tags]]"""
	subprocess.Popen(["hamster-cli", "start", str])

def hamster_cli_stop():
	"""End the current activity"""
	subprocess.Popen(["hamster-cli", "stop"])

class HamsterSwitchCommand(sublime_plugin.WindowCommand):
	def run(self):
		"""Switch to a previous Hamster activity"""
		# get the hamster_dbus_bridge path from settings
		settings = sublime.load_settings("sublime-hamster.sublime-settings")
		bridge_path = settings.get("hamster_dbus_bridge")
		bridge_path = bridge_path.replace("${packages}", sublime.packages_path())

		process = subprocess.Popen(["python", bridge_path], stdout=subprocess.PIPE)
		communication = process.communicate()
		response = json.loads(communication[0])
		self.facts = []
		messages = []
		for fact in response:
			activity = fact["activity"]
			category = fact["category"]
			tags = ", ".join(fact["tags"])
			desc = fact["description"]

			self.facts.append(fact)
			messages.append(["{0}@{1}".format(activity, category), "Description: {0}, Tags: {1}".format(desc, tags)])

		window = sublime.active_window()
		window.show_quick_panel(messages, self._on_done)

	def _on_done(self, index):
		"""on_done handler, parses the chosen fact and starts the activity"""
		if index > -1:
			fact = self.facts[index]
			str_fact = self._stringifiy_fact(fact)
			hamster_cli_start(str_fact)

	def _stringifiy_fact(self, fact):
		"""Convert a fact object into a hamster-cli friendly string supporting activity, category, description and tags"""
		result = "";
		result += "{0}@{1}".format(fact["activity"], fact["category"])

		if "description" in fact:
			result += " {0}, ".format(fact["description"])
		elif "tags" in fact and len(fact["tags"]) > 0:
			result += ", "
		
		if "tags" in fact and len(fact["tags"]) > 0:
			for tag in fact["tags"]:
				result += "#{0} ".format(tag)
			
		return result

class HamsterStopCommand(sublime_plugin.WindowCommand):
	def run(self):
		"""Stop the current activity, optionally asking for confirmation first based on the confirm_stop setting"""
		settings = sublime.load_settings("sublime-hamster.sublime-settings")
		cancel = False

		if settings.get("confirm_stop") is True:
			#check if we really want to cancel the activity
			cancel = sublime.ok_cancel_dialog("Are you sure you want to stop tracking the current activity?")
		
		if  settings.get("confirm_stop") is False or cancel is True:  
			#use hamster-cli to stop the current activity
			subprocess.Popen(["hamster-cli", "stop"])
			

class HamsterStartCommand(sublime_plugin.WindowCommand):
	def run(self):
		"""Show a prompt allowing the user to start a new activity"""
		window = sublime.active_window()
		window.show_input_panel("Start Activity (format: activity[@category[ description, [#tag1 #tag2 #etc]]] ):", "", self._on_done, None, self._on_cancel)

	def _on_cancel(self):
		"""An on_cancel handler, required for show_input_panel.  There's actually nothing to be cancelled here, so just returns False"""
		return False

	def _on_done(self, str):
		"""Once input is done, start the new activity"""
		hamster_cli_start(str)
		sublime.status_message(str)