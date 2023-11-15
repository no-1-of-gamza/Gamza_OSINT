import json
import os


class Address:
	def __init__(self):
		with open(os.path.dirname(os.path.realpath(__file__))+"\\address.txt", "r", encoding="utf-8-sig") as file:
			data = file.read()
			self.address_book = json.loads(data)

	def get(self, address):
		try:
			value = self.address_book[address]
		except KeyError:
			value = -1
		
		return value