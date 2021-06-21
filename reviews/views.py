from django.shortcuts import render
from django.shortcuts import render
from plotly.offline import plot
from plotly.graph_objs import Scatter

# Create your views here.
def show(request):
    x_data = [0,1,2,3]
    y_data = [x**2 for x in x_data]
    plot_div = plot([Scatter(x=x_data, y=y_data,
                        mode='lines', name='test',
                        opacity=0.8, marker_color='green')],
               output_type='div',
               include_plotlyjs=False)
    return render(request, "show.html", context={'plot_div': plot_div})
