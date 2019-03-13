# -*- coding: utf-8 -*-

# Note: import the app of what you are working on
from initial_demo import app
#from vis_scatter_plot import app
#from vis_dash_interaction_connected_graphs import app
#from vis_dash_interaction import app
from exercise1 import app
from exercise2 import app
from exercise3 import app


server = app.server

if __name__ == '__main__':
    # start the Dash app
    app.run_server(debug=True)



