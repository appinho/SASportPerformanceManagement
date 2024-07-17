# Utility functions data processing or plotting

# import plotly.graph_objs as go
# import plotly.io as pio

# def plot_to_html():
#     fig = go.Figure(data=[go.Bar(x=[1, 2, 3], y=[1, 3, 2])])
#     plot_html = pio.to_html(fig, full_html=False)
#     return plot_html

import matplotlib
matplotlib.use('Agg')

import seaborn as sns
import matplotlib.pyplot as plt
from io import BytesIO
import base64

def plot_to_html():
    # Example data
    tips = sns.load_dataset('tips')
    
    # Create a seaborn plot
    fig, ax = plt.subplots()
    sns.scatterplot(data=tips, x='total_bill', y='tip', ax=ax)
    
    # Save the plot to a BytesIO object
    img = BytesIO()
    fig.savefig(img, format='png')
    img.seek(0)
    
    # Encode the image to base64
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')
    
    # Return the plot as an HTML image tag
    return f'<img src="data:image/png;base64,{plot_url}" />'
