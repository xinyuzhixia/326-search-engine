from bottle import *
@route('/')
def home():
	return '<p>hello </p>'

run(app,host='0.0.0.0', port=8080, debug=True)