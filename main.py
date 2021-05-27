###############################################
#          Import some packages               #
###############################################
import atexit
from bokeh.embed import server_document
from dominate.tags import img
from flask import Flask, render_template, Response
from flask.templating import render_template_string
from flask_bootstrap import Bootstrap
from flask_nav import Nav
from flask_nav.elements import *

import io
import base64

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style='white', font_scale=1.25)
plt.rc("axes.spines", top=False, right=False)
plt.rc('xtick', bottom=True)
plt.rc('ytick', left=True)

import subprocess

import numpy as np
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
print('Test')


###############################################
#          Render Home page                   #
###############################################
@app.route('/', methods=['GET'])
def get_home():
    return (render_template('home.html'))


###############################################
#          Render Cluster page                   #
###############################################
# @app.route('/cluster')
# def get_cluster():
#     return (render_template('cluster.html'))

bokeh_process = subprocess.Popen([
    'python', '-m', 'bokeh', 'serve',
    '--allow-websocket-origin=localhost:8001', 'bokeh_server.py'
],
                                 stdout=subprocess.PIPE)


@app.route('/cluster')
def get_cluster():

    bokeh_script = server_document(url='http://localhost:8001/bokeh_server')
    return render_template('cluster.html', bokeh_script=bokeh_script)


@atexit.register
def kill_server():
    bokeh_process.kill()


###############################################
#          Render State page                   #
###############################################
@app.route('/state/plot.png')
def plot_png():
    fig = create_figure()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')


def create_figure():
    fig, ax = plt.subplots(figsize=(6, 4))

    x = np.random.rand(10)
    y = np.random.rand(10)

    ax.scatter(x, y, color="#304C89")
    return fig


@app.route('/state', methods=["GET"])
def get_state():
    return render_template('state.html')


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