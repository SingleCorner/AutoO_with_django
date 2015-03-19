from django import template
register = template.Library()

def str_to_br(val, arg1, arg2="<br>"):
	string = str(val)
	return string.replace(arg1, arg2)
register.filter(str_to_br)