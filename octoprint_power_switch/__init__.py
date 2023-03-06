# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import octoprint.plugin
import flask

from gpiozero import LED
from time import sleep

led = LED(18) 

class OctoPowerPlugin(
		octoprint.plugin.StartupPlugin,
		octoprint.plugin.TemplatePlugin,
		octoprint.plugin.SimpleApiPlugin,
		octoprint.plugin.SettingsPlugin,
		octoprint.plugin.EventHandlerPlugin,
		octoprint.plugin.RestartNeedingPlugin
	):

	power_state = False

	def get_settings_defaults(self):
		return dict(
			light_pin = 18,
			inverted_output = False
		)
	
	def get_template_configs(self):
		return [
			dict(type="navbar", custom_bindings=False),
			dict(type="settings", custom_bindings=False)
		]

	def on_event(self, event, payload): 
		events = [
			"PrintFailed",
			"PrintDone",
			"PrintCanceled"
		]
		print(event)
		if event in events:
			led.off()
			self.power_state = False


	def on_after_startup(self):
		self.power_state = False
		self._logger.info("--------------------------------------------")
		self._logger.info("OctoLight started, listening for GET request")
		self._logger.info("Light pin: {}, inverted_input: {}".format(
			self._settings.get(["light_pin"]),
			self._settings.get(["inverted_output"])
		))
		self._logger.info("--------------------------------------------")

		# Setting the default state of pin
		led.off()

	
	def on_api_get(self, request):
		# Sets the GPIO every time, if user changed it in the settings.
		
		# pin = int(self._settings.get(["light_pin"])) 
		if self.power_state:
			led.off()
		else:
			led.on()

		self.power_state = not self.power_state
		 
		return flask.jsonify(status="ok")
	
	 

__plugin_pythoncompat__ = ">=2.7,<4"
__plugin_implementation__ = OctoPowerPlugin()

 