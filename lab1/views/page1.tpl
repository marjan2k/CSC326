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
  	{{word}}
  	% for url in urls:
  	<div>
  		{{url}}
  	</div>
  	% end
  	% for i in range(num_pages):
  		% link = "/page?" + qs + "&start=" + str(i * 5)
  		<a href="{{link}}"> {{i}}</a>
  	% end

  </body>

</html>