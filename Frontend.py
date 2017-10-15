from bottle import *
from collections import OrderedDict
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.client import flow_from_clientsecrets
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
from operator import itemgetter
from beaker.middleware import SessionMiddleware
import httplib2
import bottle
historysearch={}

session_opts = {
    'session.type': 'file',
    'session.cookie_expires': 300,
    'session.data_dir': './data',
    'session.auto': True
}
app = SessionMiddleware(bottle.app(), session_opts)

@route('/')
def search():
	sign = 0 
	s = request.environ.get('beaker.session')
	if s is not None and "email" in s:
		sign = 1
		#if the user type in a string 
		if request.query.keywords: 
				keywords = request.query.keywords
				#check how many times each word occurs in the user typed string	
				output = check_appearance(keywords)
				for key in output:
					# store the searched string in the history dict
					store_history(key,output[key])

				d_sorted_by_value = sorted(historysearch.items(), key=lambda x: x[1],reverse = True)
				return template('index',results=output,keywords=keywords,history=d_sorted_by_value[:20],user_email=email)
		else: 
			return template('Query',Login= sign,email = s['email']) 
	#display the main menu if the user does not enter a string
	return template('Query',Login= sign) 
#google login 
@route('/login')
def login():
	flow = flow_from_clientsecrets("client_secrets.json",scope = 'https://www.googleapis.com/auth/plus.me https://www.googleapis.com/auth/userinfo.email',redirect_uri='http://localhost:8080/redirect')
	uri = flow.step1_get_authorize_url()
	redirect(str(uri))

#exchange code
@get('/redirect')
def redirect_page():
	code=request.query.get('code','')
	flow = OAuth2WebServerFlow(client_id = '975568128457-pa8684b9d0njq8mqdigac3tvu9o1j6u8.apps.googleusercontent.com',
	 client_secret='Ejb4FXaANO9e4PvUp7brfIIZ', scope='https://www.googleapis.com/auth/plus.me https://www.googleapis.com/auth/userinfo.email', 
	 redirect_uri='http://localhost:8080/redirect')
	credentials=flow.step2_exchange(code)
	token=credentials.id_token['sub']
	http=httplib2.Http()
	http=credentials.authorize(http)
	users_service = build('oauth2','v2',http=http)
	user_document = users_service.userinfo().get().execute()
	user_email=user_document['email']
	session = request.environ.get('beaker.session')
	session['email'] = user_document['email']
	session.save()
	redirect(str("/"))


def store_history(key,value):
	if key in historysearch:
		#if it has ever occured in the history, add the appearance
		historysearch[key] = historysearch[key] + value
	else:
		#if it never occurs
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


run(app=app,host='localhost', port=8080, debug=True)