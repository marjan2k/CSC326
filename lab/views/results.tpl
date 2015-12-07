<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>YASE</title>
    <link href='https://fonts.googleapis.com/css?family=Raleway:400,100,200,300' rel='stylesheet' type='text/css'>
    <link href='https://fonts.googleapis.com/css?family=Inconsolata:400,700' rel='stylesheet' type='text/css'>
    <link href='https://fonts.googleapis.com/css?family=Monda' rel='stylesheet' type='text/css'>
    <link href='https://fonts.googleapis.com/css?family=Pacifico' rel='stylesheet' type='text/css'>
    <link rel="stylesheet" href="/static/style.css" media="screen" charset="utf-8" type='text/css'>
  </head>

  <body>
    <div class="logo">
        % if len(name):
            <div class="profile">
                <img src="{{picture}}"></img>
                <p> {{name}} </p>
                <a class="btn-login" id="logout" href='/logout'> Sign Out </button>
            </div>
        % end
        <a href="/">Yase Search</a>
        <div class="search-box ui-widget">
          <form action="/results", method="GET">
              <input name="keywords" id="search-input" autofocus></input>
              <button type="submit" id="search-btn"> SUBMIT </button>
          </form>
        </div>
    </div>
    % if qphase:
        <div class="result-title">
            <h2 id="result-title"> Result for {{query}} = </h2>
            <h2> {{result}} </h2>
        </div>
    % else:
        <div class="result-title">
            % if hasDiff:
                <h2 id="result-title">Search for "{{" ".join(corrected_words)}}" </h2>
                <span><i>corrected from: {{" ".join(words)}}</i></span>
            % else:
                <h2 id="result-title"> Search for "{{" ".join(corrected_words)}}" </h2>
            % end
            % if num_pages > 0:
                <p> Displaying page {{curr_page + 1}} out of {{num_pages}} pages </p>
            % else:
                <p> No results found </p>
            % end
        </div>
        <div class="results">
          % for url in urls:
              <div class="result">
                  <a href="{{url['doc']}}">{{url['title']}}</a><br>
                  <p> {{url['doc']}} </p>
              </div>
        	% end
        </div>
        <div class="pages">
          % for i in range(num_pages):
            % link = "/results?" + qs + "&start=" + str(i * 5)
            <a href="{{link}}"> {{i+1}}</a>
          % end
        </div>

      </body>
    % end
</html>
