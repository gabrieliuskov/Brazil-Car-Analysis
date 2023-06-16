import dash
import dash_bootstrap_components as dbc

# ========== Style ===========
font_awesome = "https://use.fontawesome.com/releases/v5.10.2/css/all.css"
dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates@V1.0.4/dbc.min.css"
url_theme1 = dbc.themes.FLATLY
url_theme2 = dbc.themes.VAPOR
theme1 = "flatly"
theme2 = "vapor"

# ========== Instanciando o app ===========
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY, font_awesome, dbc_css], title="Brazil Car Analysis", update_title="Atualizando")


