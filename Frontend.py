from bottle import *
from collections import OrderedDict
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.client import flow_from_clientsecrets
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
from operator import itemgetter
from beaker.middleware import SessionMiddleware
from paste import httpserver
import httplib2
import bottle
historysearch={}
userRecentSearch={}
session_opts = {
    'session.type': 'file',
    'session.cookie_expires': 30,
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
		email = s['email']

	if request.query.keywords: 

		keywords = request.query.keywords
			#check how many times each word occurs in the user typed string	
		output = check_appearance(keywords)
		
		if sign==1:
				# store the searched string in the history dict
			store_history(output)
			store_recentsearch(email,output)
			d_sorted_by_value = sorted(historysearch.items(), key=lambda x: x[1],reverse = True)
			return template('index',results=output,keywords=keywords,history=d_sorted_by_value[:20],user_email=email,login=sign,recentsearch=userRecentSearch[email][0:20])
		else: 
			return template('index',results=output,keywords=keywords,login=sign)
	#display the main menu if the user does not enter a string
	if sign == 1:
		return template('Query',Login= sign,user_email=email)
	else: 
		return template('Query',Login= sign)
#google login 
@route('/login')
def login():
	flow = flow_from_clientsecrets("client_secrets.json",scope = 'https://www.googleapis.com/auth/plus.me https://www.googleapis.com/auth/userinfo.email',
		redirect_uri='http://ec2.34.237.47.138.compute-1.amazonaws.com:80/redirect')
	uri = flow.step1_get_authorize_url()
	redirect(str(uri))


@route('/logout')
def logout():
	session = request.environ.get('beaker.session')
	session.delete()
	redirect(str('/'))


#exchange code
@get('/redirect')
def redirect_page():
	code=request.query.get('code','')
	flow = OAuth2WebServerFlow(client_id = '975568128457-pa8684b9d0njq8mqdigac3tvu9o1j6u8.apps.googleusercontent.com',
	 client_secret='Ejb4FXaANO9e4PvUp7brfIIZ', scope='https://www.googleapis.com/auth/plus.me https://www.googleapis.com/auth/userinfo.email', 
	 redirect_uri='http://ec2.34.237.47.138.compute-1.amazonaws.com:80/redirect')
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


def store_history(output):
	for key in output:
		if key in historysearch:
			#if it has ever occured in the history, add the appearance
			historysearch[key] = historysearch[key] + output[key]
		else:
			#if it never occurs
			historysearch[key] = output[key]

	return

def store_recentsearch(email,keywords):
	if email not in userRecentSearch:
		userRecentSearch[email] = []
	#if has search history 
	for word in keywords:
		if word not in userRecentSearch[email]:
			userRecentSearch[email].insert(0,word)
		else:
			userRecentSearch[email].remove(word)
			userRecentSearch[email].insert(0,word)
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


httpserver.serve(application=app,host='0.0.0.0', port=80)