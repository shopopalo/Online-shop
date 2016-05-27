"""
Используется для правильной загрузки сигналов
при инициализации программы
данный класс нужно вызывать в __init__ 
"""
from django.apps import AppConfig


class PaymentConfig(AppConfig):
	name = 'payment'
	verbose_name = 'Payment'

	def ready(self):
		import payment.signals
