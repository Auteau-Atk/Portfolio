# High-Availability Portfolio Project

## Introduction
This document outlines the steps to design, develop, and deploy a high-availability personal/professional portfolio with secure editing capabilities and integration of GitHub contributions using a CDN-enhanced widget.

## 1. OAuth Integration
### Objective
Enable secure login and editing capabilities using Google Cloud OAuth 2.0.

### Steps
1. **Google Cloud Setup**
    - Create a project in the [Google Cloud Console](https://console.cloud.google.com/).
    - Enable the "OAuth Consent Screen" and register your application.
    - Obtain client ID and secret. This will be used in the backend.

2. **Frontend Integration**
    - Include Google's OAuth API in your project.
    - Use JavaScript to initiate the OAuth flow.

3. **Backend Implementation**
    - Set up routes in your backend for handling OAuth callbacks.
    - Validate the tokens received from Google.
    - Restrict access to editing routes for authenticated users.

## 2. Load Balancing with HAProxy
### Objective
Ensure high availability by distributing traffic across multiple Nginx servers.

### Steps
1. **Install HAProxy**
    - Install HaProxy

    ```bash
    sudo apt install haproxy
    ```

2. **Configure HAProxy**
    - Define backend servers (two or more Nginx instances).
    - Configure health checks for these servers.

    ```bash
    sudo nano /etc/haproxy/haproxy.cfg
    ```

    Add to config file

    ```bash
    haproxy
    frontend http_front
        bind *:80
        stats uri /haproxy_stats
        default_backend servers

    backend servers
        balance roundrobin
        server server1 instance1:80 check
        server server2 instance2:80 check
    ```

## 3. Nginx Configuration
### Objective
Set up Nginx as a web server and reverse proxy.

### Steps
1. **Install Nginx**
    - Install Nginx on your servers.

    ```
    sudo apt install nginx
    ```

2. **Configure Nginx Instances**
    - Host the portfolio on each server.
    - Create a reverse proxy to the backend.

    ```bash
    sudo nano /etc/nginx/sites-available/default
    ```

    Replace the configuration:

    ```bash
    server {
        listen 80;
        server_name domain_ip/name;

        location / {
            proxy_pass app_ip;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
    ```

    Check nginx syntax

    ```bash
    sudo nginx -t
    ```

    Restart nginx 

    ```bash
    sudo systemctl restart nginx
    ```

    Repeat 1 or more times

## 4. GitHub Contributions Widget
### Objective
Embed and optimize a GitHub contributions calendar using a CDN.

### Steps
1. **Integrate the Widget**
    - Add the widget code from the GitHub Contributions Widget repository.

2. **Use the CDN**
    - Include the CDN link provided by the widget repository for optimal performance.

    Add the following in ```<head>``` 

    ```html
    <script type="module" defer src="https://cdn.jsdelivr.net/gh/imananoosheh/github-contributions-fetch@latest/github_calendar_widget.js"></script>
    ```

    In a container ```<div>``` add the following

    ```html
    <div id="calendar-component" username="<your-github-username>"></div>
    ```

    Add this to a file called ```index.html``` with the rest of your html in the ```templates``` folder 

    Example templates/index.html
    ```html
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>My Portfolio</title>
        <script type="module" defer src="https://cdn.jsdelivr.net/gh/imananoosheh/github-contributions-fetch@latest/github_calendar_widget.js"></script>
        <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
    </head>
    <body>
        <header>
            <h1>My Portfolio</h1>
            <p>Welcome to my professional portfolio</p>
            {% if email %}
                <button id="logout-btn" class="btn">Logout</button>
            {% else %}
                <button id="login-btn" class="btn">Login</button>
            {% endif %}
        </header>

        <nav>
            <a href="#about-me">About Me</a>
            <a href="#projects">Projects</a>
            <a href="#github-contributions">GitHub Contributions</a>
        </nav>

        <section id="about-me" class="scalable-container">
            <h2>About Me</h2>
            <p>Hello! I'm a developer passionate about building scalable and secure web applications. This portfolio highlights my projects and contributions to the tech community.</p>
            <p>Feel free to explore my work or log in to edit this portfolio if you have access.</p>
        </section>

        <section id="projects" class="scalable-container">
            <h2>Projects</h2>
            <ul id="project-list">
                {% for project in projects %}
                    <li>
                        <strong>{{ project.name }}:</strong> 
                        <span>{{ project.details }}</span>
                        {% if email %}
                            <button class="btn remove-project-btn" data-name="{{ project.name }}">Remove</button>
                        {% endif %}
                    </li>
                {% endfor %}
            </ul>
            {% if email %}
                <button id="add-project-btn" class="btn">Add Project</button>
            {% endif %}
        </section>

        <section id="github-contributions" class="scalable-container">
            <h2>GitHub Contributions</h2>
            <div id="github-calendar">
                <div id="calendar-component" username="Auteau-Atk" theme-color="#4285f4"></div>
            </div>
        </section>

        <footer>
            <p>&copy; 2024 My Portfolio. All rights reserved.</p>
        </footer>

        <script src="{{ url_for('static', filename='js/button.js') }}"></script>

    </body>
    </html>
    ```

    static/css/style.css
    ```css
    * {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    }   

    body {
        font-family: 'Arial', sans-serif;
        line-height: 1.6;
        background-color: #f9f9f9;
        color: #333;
    }

    header {
        background-color: #4CAF50;
        color: white;
        padding: 20px;
        text-align: center;
    }

    header h1 {
        font-size: 2.5em;
    }

    header .btn {
        margin-top: 10px;
        padding: 10px 20px;
        background: white;
        color: #4CAF50;
        border: none;
        border-radius: 5px;
        font-weight: bold;
        cursor: pointer;
        transition: background 0.3s;
    }

    header .btn:hover {
        background: #d4f0da;
    }

    nav {
        display: flex;
        justify-content: center;
        background: #333;
        padding: 10px 0;
    }

    nav a {
        color: white;
        text-decoration: none;
        margin: 0 15px;
        font-weight: bold;
    }

    nav a:hover {
        color: #4CAF50;
    }

    section {
        padding: 20px;
        margin: 20px auto;
        max-width: 90%;
        width: auto;
        background: white;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }

    section h2 {
        color: #4CAF50;
        margin-bottom: 15px;
    }

    ul {
        list-style: none;
        padding: 0;
    }

    li {
        padding: 10px 15px;
        margin-bottom: 10px;
        background: #f4f4f4;
        border: 1px solid #ddd;
        border-radius: 5px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    li strong {
        flex-grow: 1;
    }

    .btn {
        padding: 7px 15px;
        background: #4CAF50;
        color: white;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        font-weight: bold;
        transition: background 0.3s;
    }

    .btn:hover {
        background: #45a049;
    }

    #github-contributions {
        text-align: center;
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: column;
    }

    #github-calendar {
        display: flex;
        justify-content: center;
        align-items: center;
        max-width: 100%;
        overflow-x: auto;
    }

    #calendar-component {
        max-width: 100%;
        height: auto;
        display: block;
    }

    footer {
        text-align: center;
        padding: 15px;
        background: #333;
        color: white;
        margin-top: 20px;
    }

    footer p {
        margin: 0;
    }

    .scalable-container {
        display: flex;
        flex-direction: column;
        align-items: stretch;
        min-height: 0;
        height: auto;
        width: auto;
        margin: 10px auto;
        padding: 10px;
    }

    ```

    static/js/button.js
    ```js
    document.addEventListener("DOMContentLoaded", () => {
        const loginBtn = document.getElementById('login-btn');
        const logoutBtn = document.getElementById('logout-btn');
        const addProjectBtn = document.getElementById('add-project-btn');
        const projectList = document.getElementById('project-list');

        if (loginBtn) {
            loginBtn.addEventListener('click', () => {
                window.location.href = '/login';
            });
        }

        if (logoutBtn) {
            logoutBtn.addEventListener('click', () => {
                fetch('/logout', { method: 'POST' })
                    .then(() => {
                        alert('Logged out successfully!');
                        window.location.reload();
                    });
            });
        }

        if (addProjectBtn) {
            addProjectBtn.addEventListener('click', () => {
                const projectName = prompt('Enter the project name:');
                const projectDetails = prompt('Enter the project details:');
                if (projectName && projectDetails) {
                    fetch('/add_project', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ name: projectName, details: projectDetails })
                    })
                    .then(response => response.json())
                    .then(data => {
                        alert(data.message);
                        window.location.reload();
                    });
                }
            });
        }

        document.querySelectorAll('.remove-project-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const projectName = e.target.dataset.name;
                fetch('/remove_project', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ name: projectName })
                })
                .then(response => response.json())
                .then(data => {
                    alert(data.message);
                    window.location.reload();
                });
            });
        });
    });

    ```

3. **Customize Design**
    - Match the widget’s appearance with the portfolio theme using CSS

## 5. Backend OAuth implementation
### Objective
### Steps
Implement the OAuth into the application

1. **Install Dependencies**
    - install python + dependencies

    ```bash
    sudo apt install python3
    ```

    Install pip

    ```bash
    sudo apt install pip
    ```

    Install Flask, OAuth and Requests
    ```bash
    pip install Flask
    pip install Requests
    pip install Authlib Flask
    ```
    - Create a Flask application

2. **Create a Flask Application**
    - Create a new file for your Flask app, e.g., `app.py`.

    app.py
    ```python
    from flask import Flask, render_template, redirect, url_for, session, request, jsonify
    import os
    from authlib.integrations.flask_client import OAuth

    app = Flask(__name__)
    app.secret_key = 'your_secret_key'

    google = oauth.register(
    name='google',
    client_id='client_id',
    client_secret='client_secret',
    access_token_url="https://oauth2.googleapis.com/token",
    access_token_params=None,
    authorize_url="https://accounts.google.com/o/oauth2/v2/auth",
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid profile email'},
    )

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
    ```

3. **Run the Application**
    - Start your Flask application:

    ```bash
    flask run
    ```

4. **Test OAuth Flow**
    - Visit your domain in your browser.
    - Click "Login" to initiate the OAuth flow.
    - Authenticate using your Google account.
    - Verify that the user information is retrieved and displayed after successful login.

## 6. Testing and Deployment
### Testing
1. **Functional Testing**
    - Verify all features (OAuth login, GitHub widget, load balancing, editing) work as intended.

2. **Performance Testing**
    - Use tools like `Apache JMeter` or `siege` to simulate multiple users accessing the portfolio.
    - Ensure traffic is distributed evenly across Nginx servers via HAProxy.

3. **Availability Testing**
    - Test server failover scenarios by shutting down one Nginx instance and ensuring HAProxy routes traffic correctly.
