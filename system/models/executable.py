# Primary Author:	Cristopher Matos (jasonmatos23@gmail.com)
# Course:			EEL 4915L Senior Design II, UCF Spring 2022
# File name:		executable.py
# Description:		Abstract object that should be "runnable"-like.

class Executable :

	def __init__(self) :
		raise NotImplementedError

	def Execute(self) -> None:
		raise NotImplementedError
