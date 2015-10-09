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
        <a href="/">Yase Search</a>
    </div>
    <div class="result-title">
        <h2 id="result-title"> Search for "{{keywords}}" </h2>
    </div>
    <div class="result-table">
      <table id=”results”>
          <tr>
              <th>Word</th>
              <th>Count</th>
          </tr>
          % for word in count:
            <tr>
              <td> {{word}} </td>
              <td> {{count[word]}} </td>
            </tr>
          % end
      </table>
    </div>
    <script src="http://code.jquery.com/jquery-2.1.4.min.js"></script>
    <script src="https://cdn.rawgit.com/mattboldt/typed.js/master/dist/typed.min.js"></script>
    <script src="/static/app.js"></script>
  </body>
</html>
