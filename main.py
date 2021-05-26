###############################################
#          Import some packages               #
###############################################
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_nav import Nav
from flask_nav.elements import *
from dominate.tags import img

###############################################
#          Define flask app                   #
###############################################
logo = img(src='./static/img/logo.pn',
           height="50",
           width="50",
           style="margin-top:-15px")
topbar = Navbar(
    'Meta-Analytic Hematopoietic Cell Atlas',
    View('Home', 'get_home'),
    View('Clusters', 'get_cluster'),
    View('Cell State', 'get_state'),
    View('Pseudotime', 'get_pseudotime'),
    View('About', 'get_about'),
)

# registers the "top" menubar
nav = Nav()
nav.register_element('top', topbar)

app = Flask(__name__)
Bootstrap(app)


###############################################
#          Render Home page                   #
###############################################
@app.route('/', methods=['GET'])
def get_home():
    return (render_template('home.html'))


###############################################
#          Render Cluster page                   #
###############################################
@app.route('/cluster', methods=["GET"])
def get_cluster():
    return (render_template('cluster.html'))


###############################################
#          Render State page                   #
###############################################
@app.route('/state', methods=["GET"])
def get_state():
    return (render_template('state.html'))


###############################################
#          Render Pseudotime page                   #
###############################################
@app.route('/pseudotime', methods=["GET"])
def get_pseudotime():
    return (render_template('pseudotime.html'))


###############################################
#          Render About page                   #
###############################################
@app.route('/about', methods=["GET"])
def get_about():
    return (render_template('about.html'))


nav.init_app(app)

###############################################
#                Run app                      #
###############################################
if __name__ == '__main__':
    app.run(debug=True, port=8000, host="127.0.0.1")