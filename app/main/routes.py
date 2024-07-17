from flask import render_template
from app.main import bp
from app.utils import plot_to_html

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/plot')
def plot():
    plot_html = plot_to_html()
    return render_template('plot.html', plot_html=plot_html)
