<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
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
    </div>
    % if qphase:
        <div class="result-title">
            <h2 id="result-title"> Result for {{query}} = </h2>
            <h2> {{result}} </h2>
        </div>
    % else:
        <div class="result-title">
            <h2 id="result-title"> Search for "{{word}}" </h2>
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
