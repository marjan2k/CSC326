import bottle
import httplib2
from bottle import run, request, route, static_file, template
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.client import flow_from_clientsecrets
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
from beaker.middleware import SessionMiddleware

session_opts = {
    'session.type': 'file',
    'session.cookie_expires': 300,
    'session.data_dir': './data',
    'session.auto': True
}

app = SessionMiddleware(bottle.app(), session_opts)
history = {}

@route('/static/<filename>')
def serve_static(filename):
    return static_file(filename, root='public')

@route('/')
def get_homepage():
    session = bottle.request.environ.get('beaker.session')
    print session
    # retrieve user info from session object, set to defaults if it doesn't exist
    email = session['email'] if 'email' in session else False
    picture = session['picture'] if 'picture' in session else ""
    name = session['name'] if 'name' in session else ""
    # retrieve and sort the user search history
    user_history = history[email] if email in history else {}
    sorted_history = sorted(user_history.items(), reverse=True, key=lambda x: x[1])
    # render the the template with the history and user info
    return template('home', history=sorted_history[0:20], email=email, name=name, picture=picture)

@route('/logout')
def logout():
    # delete session object and redirect
    session = bottle.request.environ.get('beaker.session')
    session.delete()
    bottle.redirect('/')

@route('/auth')
def google_auth():
    # authenticate using googleapis
    flow = flow_from_clientsecrets(
        'client_secrets.json',
        scope='https://www.googleapis.com/auth/userinfo.email',
        redirect_uri='http://ec2-52-23-183-97.compute-1.amazonaws.com:8080/redirect'
    )
    uri = flow.step1_get_authorize_url()
    return bottle.redirect(str(uri))

@route('/redirect')
def redirect():
    print "here0"
    # Get access token via oauth2client and auth code returned by googleapis auth
    code = request.query.get('code', '')
    flow = OAuth2WebServerFlow(
        client_id='937294237328-tud9jsvdrdehdevi2clvm158lfm6vlgd.apps.googleusercontent.com',
        client_secret='fyEizCcCAr2JgqqWTVoXeye1',
        scope='https://www.googleapis.com/auth/userinfo.email',
        redirect_uri='http://ec2-52-23-183-97.compute-1.amazonaws.com:8080/redirect'
    )
    print "here"
    credentials = flow.step2_exchange(code)
    token = credentials.id_token['sub']
    http = httplib2.Http()
    http = credentials.authorize(http)
    users_service = build('oauth2', 'v2', http=http)
    user_document = users_service.userinfo().get().execute()
    # save user profile information in the session dict
    session = request.environ.get('beaker.session')
    session['email'] = user_document['email']
    session['picture'] = user_document['picture']
    session['name'] = user_document['name']
    session.save()
    # redirect to the homepage
    return bottle.redirect('/')

@route('/word_count', method='GET')
def get_word_count():
    count = {}
    session = request.environ.get('beaker.session')
    keywords = request.query['keywords']
    words = keywords.lower().split()

    # retrieve user info from session object, set to defaults if it doesn't exist
    name = session['name'] if 'name' in session else ""
    picture = session['picture'] if 'picture' in session else ""

    # create a search history on a per user basis
    local_history = {}
    if 'email' in session:
        if session['email'] not in history:
            history[session['email']] = {}
        local_history = history[session['email']]

    for word in words:
        count[word] = (count[word] if word in count else 0) + 1
        local_history[word] = (local_history[word] if word in local_history else 0) + 1

    return template('count', picture=picture, name=name, keywords=keywords, count=count)

run(app=app, host='0.0.0.0', port=8080, debug=True)
