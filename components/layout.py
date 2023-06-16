import pandas as pd

from dash import Input, Output, State, html, dcc
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import ThemeSwitchAIO, template_from_url

import plotly.express as px
import plotly.graph_objects as go

from data import *
from app import *

# Margens padrão
graph_margin=dict(l=25, r=25, t=25, b=0)


# Barra lateral do aplicativo 
left_side =  dbc.Row([
            dbc.Card([
                dbc.CardHeader([
                    # Titulo da sidebar =======================
                    html.H2("Brazil Car Analysis - 2022", style={"textAlign":"center","padding-bottom":10}),
                    html.P("Created by: Gabriel Iuskov", style={"padding-bottom":10}),

                    # tema da sidebar =======================
                    dbc.Row([
                        dbc.Col([
                        
                        ThemeSwitchAIO(aio_id="theme", themes=[url_theme1, url_theme2])
                    ], sm=12, md=6),
                    # tema da sidebar =======================
                    dbc.Col([
                        html.I(className="fas fa-car", style={"font-size":50})
                    ], sm=12, md=6)
                    ], className="d-flex align-items-center justify-content-center")
                    
                ], className="w-100", style={"textAlign":"center"}),

                dbc.CardBody([
                    # Filtros de seleção ========================
                    # Filtro de marcas
                    html.H4("Marcas:",className="labels"),
                    dcc.Dropdown(id="marcas-select",
                            options=[{"label": i, "value": i} for i in marcas_data],
                            value=[marcas_data[0]],
                            multi=True,
                            clearable=False,
                            placeholder="Ex: Bmw, Caoa Chery",
                            className="dropdownsEsliders"              
                            ),
                    
                    # Filtro de cambio
                    html.H4("Tipo de câmbio:",className="labels"),
                    dcc.Dropdown(id="cambio-select",
                            options=[{"label": i, "value": i} for i in gear_data],
                            value=[gear_data[1]],
                            multi=True,
                            clearable=False,
                            placeholder="Ex: Manual",
                            className="dropdownsEsliders"              
                            ),


                    # Filtro de mês
                    html.H4("Mês de referência:",className="labels"),
                    dcc.RangeSlider(
                        id="mes-slider",
                        marks={j: str(i+1) for i, j in enumerate(month_data)},
                        min=1,
                        max=12,
                        value = [1,12],
                        step=1,
                        className="dropdownsEsliders"
                    ),

                    # Filtro de potencia
                    html.H4("Potência [cm³]:",className="labels"),
                    dcc.RangeSlider(
                        id="engine-slider",
                        marks={i: str(i) for i in engine_data},
                        min=0,
                        max=maior_engine,
                        value = values_engine,
                        step=None,
                        className="dropdownsEsliders"
                    ),

                    # Filtro de fabricação
                    html.H4("Ano de fabricação:",className="labels"),
                    dcc.Dropdown(id="veiculo-select",
                            options=[{"label": i, "value": i} for i in veiculo_anos_data],
                            value=[veiculo_anos_data[10]],
                            clearable=False,
                            multi=True,
                            placeholder="Ex: 2021",
                            className="dropdownsEsliders"                
                            ),

                ])
            ],class_name="card_tab")
        ])

graficos = [
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    # Grafico de preço médio por marca
                    dbc.Spinner(dcc.Graph(id="price-brand-graph", config={"displayModeBar": False, "showTips": False}))
                ])
            ], class_name="card")
        ])
    ]),

    dbc.Row([
        dbc.Col([

            dbc.Card([
                dbc.CardBody([
                    # Grafico de preço médio por mês por marca
                    dbc.Spinner(dcc.Graph(id="price-year-graph", config={"displayModeBar": False, "showTips": False}))
                ])
            ], class_name="card")     
        ])
    ]),

    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    # Grafico de preço médio por cambio
                    dbc.Spinner(dcc.Graph(id="price-engine-graph", config={"displayModeBar": False, "showTips": False}))
                ])
            ], style={"height":650})  
            
        ], sm=12, md=6),

        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    # Veículo mais barato
                    dbc.Spinner(dcc.Graph(id="cheap", config={"displayModeBar": False, "showTips": False})),

                    # Veículo mais caro
                    dbc.Spinner(dcc.Graph(id="expensive", config={"displayModeBar": False, "showTips": False}))
                ])
            ], style={"height":650})  
        ], sm=12, md=6),
    ],class_name="g-3 my-auto")
]

right_side = [
    html.Div(
    id="dashboard",
    children=graficos),    
]


# ========== Callbacks =================
@app.callback(
    Output("marcas-select", "value"),
    Input("marcas-select", "value"),

    prevent_initial_call=True
)
def verifica_marca(value):

    if value == []:
        return [marcas_data[0]]
    return value

@app.callback(
    Output("cambio-select", "value"),
    Input("cambio-select", "value"),

    prevent_initial_call=True
)
def verifica_cambio(value):

    if value == []:
        return [gear_data[1]]
    return value


@app.callback(
    Output("veiculo-select", "value"),
    Input("veiculo-select", "value"),

    prevent_initial_call=True
)
def verifica_ano(value):

    if value == []:
        return veiculo_anos_data[10]
    return value


# Callback para avaliar se existem dados para o filtro selecionado
@app.callback(
    Output("dashboard", "children"),
    Output("store-backup", "data"),
    Output("dashboard", "style"),


    Input("marcas-select", "value"),
    Input("cambio-select", "value"),

    Input("mes-slider", "value"),
    Input("engine-slider", "value"),
    Input("veiculo-select", "value"),
    State("store", "data"),
)
def update_dashboard(marcas, cambio, mes, potencia, fabricacao, data):
    df_data = pd.DataFrame(data)

    mes_selecionado = []
    for i in range(mes[0], mes[1]):
        if i in mes_dashboard.keys():
            mes_selecionado.append(mes_dashboard[i])
        
    df_data = df_data[(df_data.brand.isin(marcas)) & (df_data.gear.isin(cambio))]
    df_data = df_data[(df_data.month_of_reference.isin(mes_selecionado)) & (df_data.engine_size >= potencia[0]) & (df_data.engine_size <= potencia[1])]
    df_data = df_data[df_data.year_model.isin(fabricacao)].reset_index(drop=True)

    if len(df_data) == 0:
        return [html.H1("Sem dados para os filtros selecionados!")], None, {"display": "flex", "justify-content": "center", "align-items": "center"}
    else:
        return graficos, df_data.to_dict(), {}



# Callback para atualizar os 5 graficos
@app.callback(
    Output("price-brand-graph", "figure"),
    Output("price-year-graph", "figure"),
    Output("price-engine-graph", "figure"),
    Output("cheap", "figure"),
    Output("expensive", "figure"),

    Input("store-backup", "data"),
    Input(ThemeSwitchAIO.ids.switch("theme"), "value"),

)
def update_graphs(data, url):
    df_data = pd.DataFrame(data)

    template = theme1 if url else theme2

    # Grafico de preço médio x marca
    df_graph1 = df_data.groupby("brand").mean("avg_price_brl")[["avg_price_brl"]].reset_index()
    
    fig1 = px.bar(
        df_graph1,
        x="brand", 
        y="avg_price_brl", 
        color="brand", 
        title="Preço médio x Marca",
        template=template
        )
    
    fig1.update_traces(
        hovertemplate="Valor: R$ %{y:,.0f}",
        )
    
    fig1.update_layout(
        xaxis_title="Marca",
        yaxis_title = "Preço médio",
        height=300,
        legend_title_text="Marca",
        margin=graph_margin
    )

    fig1.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')

    # Grafico de preço médio x marca ao longo do ano
    df_graph2 = df_data.groupby(["brand", "month_of_reference"]).mean("avg_price_brl")[["avg_price_brl"]].reset_index()
    df_graph2.month_of_reference = df_graph2.month_of_reference.map(mes_inverso)
    df_graph2 = df_graph2.sort_values("month_of_reference").reset_index(drop=True)

    fig2 = px.line(df_graph2,x="month_of_reference",markers=True, y="avg_price_brl", color="brand", title="Preço médio x mês", template=template)
    
    fig2.update_traces(
        hovertemplate="Valor: R$ %{y:,.0f}",
        )
    
    fig2.update_layout(
        xaxis_title="Mês",
        yaxis_title = "Preço médio",
        height=300,
        legend_title_text="Marca",
        margin=graph_margin,
        xaxis={'ticktext': df_graph2.month_of_reference.sort_values().unique(), 'tickvals': df_graph2.month_of_reference.sort_values().unique()}
    )

    fig2.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')

    # Grafico de preço médio x cambio
    df_graph3 = df_data.groupby("gear").mean("avg_price_brl")[["avg_price_brl"]].reset_index()

    fig3 = px.pie(
        df_graph3,values="avg_price_brl",
        names="gear", 
        title="Preço médio x câmbio",
        labels={"avg_price_brl":"Preço médio","gear": "Câmbio"}, 
        template=template
        )
    
    fig3.update_traces(
        hovertemplate='R$ %{value:,.0f}',  
        )
    
    fig3.update_layout(
        height=650,
        margin=graph_margin
    )

    fig3.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')

    # Indicador de carro mais barato
    df_cheap = df_data[df_data.avg_price_brl == df_data.avg_price_brl.min()][["brand","model", "gear", "year_model", "avg_price_brl", "engine_size"]].reset_index(drop=True)

    fig4 = go.Figure()

    fig4.add_trace(go.Indicator(
        title={"text": f'Mais barato: <br>{df_cheap.at[df_cheap.index[0],"brand"]} <br> {df_cheap.at[df_cheap.index[0],"model"]} <br> {df_cheap.at[df_cheap.index[0],"gear"]} - {df_cheap.at[df_cheap.index[0],"year_model"]} - Potência: {df_cheap.at[df_cheap.index[0],"engine_size"]}', "font": {"size":23}},
        value=df_cheap.at[df_cheap.index[0],"avg_price_brl"],
        number={"prefix": "R$", "valueformat": ":,.0f","font":{"size":50}}
    ))

    fig4.update_layout(
        height=300,
        template=template,
        margin=graph_margin
    )

    # Indicador de carro mais caro
    df_expensive = df_data[df_data.avg_price_brl == df_data.avg_price_brl.max()][["brand","model", "gear", "year_model", "avg_price_brl", "engine_size"]].reset_index(drop=True)

    fig5 = go.Figure()

    fig5.add_trace(go.Indicator(
        title={"text": f'Mais barato: <br>{df_expensive.at[df_expensive.index[0],"brand"]} <br> {df_expensive.at[df_expensive.index[0],"model"]} <br> {df_expensive.at[df_expensive.index[0],"gear"]} - {df_expensive.at[df_expensive.index[0],"year_model"]} - Potência: {df_expensive.at[df_expensive.index[0],"engine_size"]}', "font": {"size":23}},
        value=df_expensive.at[df_expensive.index[0],"avg_price_brl"],
        number={"prefix": "R$", "valueformat": ":,.0f","font":{"size":50}}
    ))

    fig5.update_layout(
        height=300,
        template=template,
        margin=graph_margin
    )

    return fig1, fig2, fig3, fig4, fig5
