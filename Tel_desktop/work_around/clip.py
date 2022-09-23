import pyperclip
import time
p=''
while(1):
	s = pyperclip.paste()
	pyperclip.copy(s)

	if(s != p):
		print(s)
		p=s 
	time.sleep(1)