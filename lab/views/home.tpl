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
    <link rel="stylesheet" href="//code.jquery.com/ui/1.11.4/themes/smoothness/jquery-ui.css">
    <script src="//code.jquery.com/jquery-1.10.2.js"></script>
    <script src="//code.jquery.com/ui/1.11.4/jquery-ui.js"></script>
    <script>
      $(function() {
          function split( val ) {
            return val.split( / \s*/ );
          }
          function extractLast( term ) {
            return split( term ).pop();
          }

          $( "#search-input" )
          
            .bind( "keydown", function( event ) {
                if ( event.keyCode === $.ui.keyCode.TAB &&
                    $( this ).autocomplete( "instance" ).menu.active ) {
                  event.preventDefault();
                }
            })

            .autocomplete({
              source: function( request, response ) {
                console.log("VOWH");
                $.getJSON( "/autocomplete", {
                  term: extractLast( request.term )
                }, response );
              },
              search: function() {
                // custom minLength
                var term = extractLast( this.value );
                if ( term.length < 2 ) {
                  return false;
                }
              },
              focus: function() {
                // prevent value inserted on focus
                return false;
              },
              select: function( event, ui ) {
                var terms = split( this.value );
                // remove the current input
                terms.pop();
                // add the selected item
                terms.push( ui.item.value );
                // add placeholder to get the comma-and-space at the end
                terms.push( "" );
                this.value = terms.join( " " );
                return false;
              }
        });
      });
    </script>
  </head>
  <body>
    <div class="logo">
        % if email:
            <div class="profile">
                <img src="{{picture}}"></img>
                <p>{{name}}</p>
                <a class="btn-login" id="logout" href='/logout'> Sign Out </button>
            </div>
        % end
        <a href="/"> Yase Search </a><br>
        <p> Made with &hearts; by Ridoy, Marjan and Zen </p>
        % if not email:
            <button class="btn-login" onclick="window.location.href='/auth'"> Login </button>
        % end
    </div>
    <div class="search-title">
        <h2 id="search-title"> enter your query. </h2>
    </div>
    <div class="search-box ui-widget">
        <form action="/results", method="GET">
            <input name="keywords" id="search-input" autofocus></input>
            <button type="submit" id="search-btn"> SUBMIT </button>
        </form>
        % if len(history) and email:
        <h2> Top {{len(history)}} searched keywords </h2>
        <div class="result-table">
            <table id="history">
                <tr>
                    <th>Word</th>
                    <th>Count</th>
                </tr>
                % for word in history:
                  <tr>
                    <td> {{word[0]}} </td>
                    <td> {{word[1]}} </td>
                  </tr>
                % end
            </table>
        </div>
        %end
    </div>
  </body>
</html>
