from bottle import *
@route('/SecondPage')
def second():
	return '<html><head><title>CSC 326</title></head><body><h1>programming csc good!</h1><body></html>'

@route('/ThirdPage')
def third():
	return '<html><head><title>Third Page</title></head><body><h1> 467 complier janwen</h1><body></html>'

@route('/HomePage')
def home():
	return '<html><head><title>Home Page</title></head>\
	<body><h1> csc 467 </h1><a href="SecondPage"> languages </a> <a href="ThirdPage"> Thrid Page</a></body><html/>'

run(host='localhost', port=8080, debug=True)