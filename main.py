# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START gae_python37_app]
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
    # # form = TwitterForm()
    # if request.method == 'POST':
    # #     if form.validate_on_submit() == False:
    # #         return render_template('project1.html',  form=form,showResult = False)
    # #     else:
    # #         username = request.form.get('username')
    # #         return redirect(url_for(getUsername))
        
    # # elif request.method == 'GET':
    #     result = request.form['text']
    #     return render_template('prject1.html', result =result)
    # else:
    #     return render_template('project1.html')        
    if request.method == 'POST':
      username = request.form['username']
      
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
    app.run(debug=True)
# [END gae_python37_app]
