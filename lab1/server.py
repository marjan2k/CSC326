from bottle import run, request, route, static_file, template

history = {}

@route('/static/<filename>')
def serve_static(filename):
    return static_file(filename, root='public')

@route('/')
def get_homepage():
    sorted_history = sorted(history.items(), reverse=True, key=lambda x: x[1])
    return template('home', history=sorted_history[0:20])

@route('/word_count', method='GET')
def get_word_count():
    count = {}
    keywords = request.query['keywords']
    words = keywords.lower().split()

    for word in words:
        count[word] = (count[word] if word in count else 0) + 1
        history[word] = (history[word] if word in history else 0) + 1
    return template('count', keywords=keywords, count=count)

run(host='localhost', port=8080, debug=True)
