import bottle
import httplib2
import pydash as _
from pymongo import MongoClient
from bottle import run, request, route, static_file, template, error
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
page_count = 0;
conn = MongoClient()
db = conn['crawler']
should_boost = True
boost_factor = {
    'title': 2.50,
    'url': 5.00,
    'word_frequency': 1.00
}

def get_word_id_from_lexicon(words):
    # find multiple words from mongodb and iterate through the cursor to retrive
    result = [word for word in db.lexicon.find({"word": {"$in": words}})]
    return result

def get_url_ids_from_inverted_index(word_list):
    word_ids = _.pluck(word_list, 'word_id')
    result = [doc for doc in db.inverted_index.find({"word_id": {"$in": word_ids}})]
    return result

def get_page_rank_scores(doc_list):
    # flatten, pluck and remove duplicates from the results list
    url_ids = _.chain(doc_list).pluck('doc_id_list').flatten().pluck('doc_id').uniq().value()
    ranks = db.page_rank.find({ "doc_id": {"$in": url_ids }})
    return {rank['doc_id']: rank['score'] for rank in ranks}

def boost_page_rank(words, word_index, ranks, docs, doc_list):
    if not should_boost: return ranks
    # index doc_list by the word_id for quick lookup
    indexed_doc_list = {doc['word_id']: doc['doc_id_list'] for doc in doc_list}
    # index word_index by word -> word_id
    word_index = {word['word']: word['word_id'] for word in word_index}
    # try to boost rank for each document
    for doc in docs:
        doc_id = doc['doc_id']
        url = doc['doc']
        text = doc['title'].lower()
        # iterate through search words and boost for each applicable factor
        for word in words:
            # boost for word occurance frequency
            count = _.find(indexed_doc_list[word_index[word]], {'doc_id': doc_id})
            count = count['count'] if count is not None else 0
            factor = boost_factor['word_frequency'] * count
            ranks[doc_id] *= factor
            # boost for title
            if text.find(word) != -1:
                ranks[doc_id] *= boost_factor['title']
                print 'can boost title!', text, word, doc_id, boost_factor['title']
            # boost for url
            if url.find(word) != -1:
                ranks[doc_id] *= boost_factor['url']
                print 'can boost url!', url, word, doc_id, boost_factor['url']

    return ranks

def sort_and_resolve_urls(words, word_index, ranks, doc_list):
    # flatten, pluck and remove duplicates from the results list
    url_ids = _.chain(doc_list).pluck('doc_id_list').flatten().pluck('doc_id').uniq().value()
    # resolve all the doc ids to their respective document information
    results = [doc for doc in db.doc_index.find({"doc_id": {"$in": url_ids}})]
    # boost page rank as appropriate
    ranks = boost_page_rank(words, word_index, ranks, results, doc_list)
    # sort and return the results
    return sorted(results, reverse=True, key=lambda doc: ranks[doc['doc_id']])

def fetch_urls(words):
    # fetch word_id for the given word (for now -> first word in the search query)
    word_index = get_word_id_from_lexicon(words)
    # if urls for the word does not exist in the db, return no results
    if len(word_index) == 0: return []
    # fetch list of url ids containing the word_id from the inverted_index
    doc_list = get_url_ids_from_inverted_index(word_index)
    # sort url_ids using the page rank scores
    ranks = get_page_rank_scores(doc_list)
    # resolved the url_ids to their respective urls
    return sort_and_resolve_urls(words, word_index, ranks, doc_list)

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

@route('/results', method='GET')
def page():
    keywords = request.query['keywords'].lower()
    words = keywords.split()
    start = int(request.query['start']) if 'start' in request.query else 0
    urls = fetch_urls(words)

    name = "" # TODO(Zen): Replace with user name later
    original_qs = "keywords=" + "+".join(words)
    num_pages = len(urls) / 5
    if (len(urls) % 5 != 0): num_pages += 1

    return template('results', name=name, curr_page=start/5, word=keywords, urls=urls[start:start+5], qs=original_qs, num_pages=num_pages)

@error(404)
def error404(error):
    return """
        <h1> This page/resource does not exist.
             Click <a href="/">here</a> to go to the home page
        </h1>
    """

run(app=app, host='0.0.0.0', port=8080, debug=True)
