import dash_bootstrap_components as dbc

from app import *
from components.layout import *

# ========== Montando o layout ===========

server = app.server

app.scripts.config.serve_locally = True
app.layout = dbc.Container([
    dcc.Store(id="store", data=store_data),
    dcc.Store(id="store-backup"),

    dbc.Row([
        dbc.Col([
            left_side
        ], sm=12, md=3),

        dbc.Col(right_side, sm=12, md=9)
    ], class_name="g-3 my-auto")
], fluid=True, style={"padding-left":20, "padding-top":5}, class_name="dbc")


# ========== Ligando o servidor ===========
if __name__ == "__main__":
    app.run_server(debug=False, port=8050, host="0.0.0.0")