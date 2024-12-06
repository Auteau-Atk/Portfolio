from flask import Flask, render_template, redirect, url_for, session, request, jsonify
import os
from authlib.integrations.flask_client import OAuth

app = Flask(__name__)
app.secret_key = 'keycaps'

oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id='119473968294-14tchprk18lb2hjiovkf78ev5l7so1jg.apps.googleusercontent.com',
    client_secret='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',
    access_token_url="https://oauth2.googleapis.com/token",
    access_token_params=None,
    authorize_url="https://accounts.google.com/o/oauth2/v2/auth",
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid profile email'},
)

# Store projects in memory for this example
projects = [
    {"name": "Project 1", "details": "Description of Project 1"},
    {"name": "Project 2", "details": "Description of Project 2"},
    {"name": "Project 3", "details": "Description of Project 3"},
]

@app.route('/')
def index():
    email = session.get('email')
    return render_template('index.html', email=email, projects=projects)

@app.route('/login')
def login():
    redirect_uri = url_for('authorize', _external=True)
    return google.authorize_redirect(redirect_uri)

@app.route('/authorize')
def authorize():
    token = google.authorize_access_token()
    resp = google.get('userinfo')
    user_info = resp.json()
    session['email'] = user_info['email']
    return redirect(url_for('index'))

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('email', None)
    return '', 204

@app.route('/add_project', methods=['POST'])
def add_project():
    if 'email' not in session:
        return jsonify({"error": "Unauthorized"}), 403
    data = request.json
    projects.append({"name": data['name'], "details": data['details']})
    return jsonify({"message": "Project added successfully", "projects": projects}), 200

@app.route('/remove_project', methods=['POST'])
def remove_project():
    if 'email' not in session:
        return jsonify({"error": "Unauthorized"}), 403
    data = request.json
    project_name = data['name']
    global projects
    projects = [p for p in projects if p['name'] != project_name]
    return jsonify({"message": "Project removed successfully", "projects": projects}), 200

if __name__ == "__main__":
    app.run(debug=True)
