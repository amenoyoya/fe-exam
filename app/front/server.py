from flask import Flask, redirect, request

# home html
home_html: str = '''
<!DOCTYPE html>
<html lang="ja">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/bulma/0.7.5/css/bulma.min.css">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/animate.css/3.7.0/animate.min.css">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.9.0/css/all.min.css">
    </head>
    <body>
        <div id="app"></div>
        <script src="/static/js/bundle.js"></script>
    </body>
</html>
'''

# Flask server
app = Flask(__name__)

# root url
@app.route('/')
def index():
  return home_html

# 404 not found => redirect to root
@app.errorhandler(404)
def error_handler(error):
    return redirect('/?redirect=' + request.path)

if __name__ == '__main__':
  app.run(debug=True)
