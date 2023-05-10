import requests

url = 'http://10.10.133.207/login'
#r = requests.get(url, allow_redirects=True)
# Just make sure the extension is matching here

#print (r.content)

myobj = {'username': 'admin', 'password': 'admin'}

x = requests.post(url, data = myobj)

print(x.text)

#regex 
# enabled</h3></b></label><br>([\d +\*\-\/]+)= \?<input