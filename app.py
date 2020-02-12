from flask import Flask,render_template,flash,redirect,request,url_for,json
from twitterProject.__init__ import twitterGenerator
from flask_wtf import FlaskForm

# from config import Config

app = Flask(__name__)
# app.config.from_object(Config)
app.config['SECRET_KEY'] = 'any secret string'

@app.route('/')
def home():
    """Return a friendly HTTP greeting."""
    return render_template ('home.html')


@app.route('/project1.html',methods=['POST','GET'])
def submit():     
    if request.method == 'POST':
      reuqest_json = json.loads(request.data, strict=False)
      username = reuqest_json.get('username')
      result = twitterGenerator(username)
      return result
    else:
  
      return render_template('project1.html')

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404_page.html'), 404

if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(debug=False)
