import kivy
kivy.require('1.2.0')
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
from kivy.properties import ObjectProperty, NumericProperty, ListProperty
from kivy.factory import Factory
from kivy.config import ConfigParser
from kivy.uix.settings import Settings

class Calculator(Widget):
	ti = ObjectProperty(None)
	lastOp = ""
	memorynum = 0.0
	operation = False

	def _execute(self, op):
		if op in "0123456789.":
			if self.lastOp == "=":
				self.lastOp = ""
			self._setText(op)

		elif op in "+-/x^" and self.lastOp != "=":
			if self.lastOp != "":
				self._exeOp(op)
			else:
				self.memorynum = float(self.ti.text)
			self.lastOp = op
			self.operation = True

		elif op in "Cc":
			self.ti.text = ""
			self.memorynum = 0.0
			self.lastOp = ""

		elif op == "<" and self.lastOp != "=":
			self.ti.text = self.ti.text[:-1]

		elif op == "=" and self.lastOp != "=":
			self._exeOp(op)
			self.memorynum = 0.0
			self.lastOp = "="
			self.operation = True

		elif op == "1/2" and self.lastOp != "=":
			self.ti.text = str(float(self.ti.text)/2)

	def _exeOp(self, op):
		if self.lastOp == "+":
			self.memorynum += float(self.ti.text)
		elif self.lastOp == "-":
			self.memorynum -= float(self.ti.text)
		elif self.lastOp == "x":
			self.memorynum *= float(self.ti.text)
		elif self.lastOp == "/":
			self.memorynum /= float(self.ti.text)
		elif self.lastOp == "^":
			self.memorynum = self.memorynum ** float(self.ti.text)
		self.ti.text = str(self.memorynum)

	def _setText(self, op):
		if op == "." and "." in self.ti.text:
			return
		if self.operation:
			self.ti.text = op
			self.operation = False
		else:
			self.ti.text += op

class CalcApp(App):
	use_kivy_settings = False
	def build(self):
		self.Calc = Calculator()
		return self.Calc

	def build_config(self, config):
		config.setdefaults('Calculator Colors', \
			{
			'CC' : 'Off',
			'NB' : 'default',
			'NBT': 'default',
			'OB' : 'default',
			'OBT' : 'default',
			'SB' : 'default',
			'SBT' : 'default',
			'TIB' : 'default',
			'TIF' : 'default'
			})
	def on_config_change(self, config, section, key, value):
		if config is self.config:
			if key == "CC" and value == "On":
				print "fuck"
			else:
				print section, key, value
	def build_settings(self, settings):
		settings.add_json_panel('Customization',
				self.config,
				"settings_calc.json")
	def on_pause(self):
		return True
	def on_resume(self):
		pass

if __name__=='__main__':
	CA = CalcApp()
	CA.run()
