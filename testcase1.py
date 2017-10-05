from bottle import *
@route('/SecondPage')
def second():
	return '<html><head><title>Second Page</title></head><body><h1>apple banana building</h1><body></html>'

@route('/ThirdPage')
def third():
	return '<html><head><title>Third Page</title></head><body><h1>love ece csc building</h1><body></html>'

@route('/HomePage')
def home():
	return '<html><head><title>Home Page</title></head>\
	<body><h1>apple banana dog cat</h1><a href="SecondPage"> Second Page</a> <a href="ThirdPage"> Thrid Page</a></body><html/>'

run(host='localhost', port=8080, debug=True)