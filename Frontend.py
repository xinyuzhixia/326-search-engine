from bottle import *
from collections import OrderedDict
historysearch={}



@route('/')
def search():
#if the user type in a string 
	if request.query.keywords: 
			keywords = request.query.keywords
			#check how many times each word occurs in the user typed string	
			output = check_appearance(keywords)
			string = '<p>Search for "%s"</p>'%(keywords)
			results = '<table id = "results"><tr> <th>Word</th> <th>Count</th></tr>'
			history = '<table id = "history"><tr> <th>Word</th> <th>Count</th></tr>'
			for key in output:
				tablecontent = '<tr><td>%s</td><td>%d</td></tr>'%(key,output[key])
				results = results+tablecontent
				# store the searched string in the history dict
				store_history(key,output[key])	
			results = results+'</table>'
			#order the history with decesending order of value
			for key,value in sorted(historysearch.iteritems(),key=lambda (k,v):(v,k),reverse=True):
				historyvalue='<tr><td>%s</td><td>%d</td></tr>'%(key,value)
				history = history+historyvalue
			history = history + '</table>'	
			return string + results + "<p>Search history</p>"+history

#display the main menu if the user does not enter a string
	else: 
		return template('Query.html')




def store_history(key,value):
	if key in historysearch:
		#if it has ever occured in the history, add the appearance
		historysearch[key] = historysearch[key] + value
	else:
		#if it never occurs and the history has less than 20 inputs 
		if len(historysearch) < 20:
			historysearch[key] = value
	return

#check the appearance of each word
def check_appearance(inputstring):
	#convert to lower case 
	inputstring = inputstring.lower()
	splitstring = inputstring.split()
	appearance = OrderedDict()
	for key in splitstring:
		if key not in appearance:
			#if it is the first time the word occurs
			appearance[key] = 1
		else: 
			appearance[key] = appearance[key] + 1

	return appearance


run(host='localhost', port=8080, debug=True)