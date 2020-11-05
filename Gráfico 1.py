import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import plotly.offline as py
import plotly.graph_objs as go

datas = []
domesticas = []
internacionais = []
total_de_buscas = []
dados = open('Gráfico 1.csv', 'r')
for line in dados:
    line = line.strip()
    data, domes, inter, total = line.split(';')
    datas.append(data)
    domesticas.append(domes)
    internacionais.append(inter)
    total_de_buscas.append(total)
del domesticas[0]
del internacionais[0]
del datas[0]
del total_de_buscas[0]

trace1 = go.Scatter(x = datas,
                y = domesticas, 
                name = 'Domésticas',
                text = datas,
                mode = 'lines',
                line = dict(color = 'rgb(242, 5, 5)'),
                hovertemplate = '%{y}'.center(8) + '<br>'  + '%{text}'
                )

trace2 = go.Scatter(x = datas,
                y = internacionais,
                mode = 'lines',
                name = 'Internacionais',
                text = datas,
                line = dict(color = 'rgb(5, 13, 166)'),
                hovertemplate = '%{y}'.center(8) + '<br>'  + '%{text}'
                )

trace3 = go.Scatter(x = datas,
                y = total_de_buscas,
                mode = 'lines',
                name = 'Total de buscas',
                text = datas,
                line = dict(color = 'rgb(13, 13, 13)'),                
                hovertemplate = '%{y}'.center(8) + '<br>'  + '%{text}'
)

gráfico_de_linhas = [trace1, trace2, trace3]

fig = go.Figure(gráfico_de_linhas)

if len(datas) > 18:
    variação_legenda_x = len(datas)//18
else:
    variação_legenda_x = 1

fig.update_layout(
    xaxis_title =dict(
        text = "<b>Data<b>",
        font = dict(
            family = 'Arial',
            color = 'black',
            size = 16
        )
    ),
    xaxis = dict(
        rangeslider=dict(visible=True),
        type = 'category',
        showline = True,
        tickmode = "linear",
        tick0 = datas[0],
        dtick = variação_legenda_x,
        showgrid = False,
        linecolor = 'rgb(63, 64, 63)',
        linewidth = 2,
        ticks = 'outside'
    ),
    yaxis = dict(
        showgrid = True,
        gridcolor = 'rgb(63, 64, 63)',
        zeroline = False,
        showline = True,
        linecolor = "rgb(63, 64, 63)",
        showticklabels = False,
        ticksuffix = '%'
    ),
    autosize = True,
    margin = dict(
        autoexpand = True,
        t = 50,
        l = 100
    ),
    height = 580,
    plot_bgcolor = 'white',
    hoverlabel = dict(
        bgcolor = '#3F3F3F',
        align = 'auto',
        font = dict(
            family = 'Arial',
            size = 16,
            color = 'white'
        )
    )
)


annotations = []
valores_de_y = [-50, 0, 50, 100]

for valor_y in valores_de_y:
    annotations.append(dict(
        xref = 'paper', x = 0.00005, y = valor_y,
        xanchor = 'right', yanchor = 'middle',
        text ='{}%'.format(valor_y),
        showarrow = False 
    ))

annotations.append(dict(
    xref = 'paper', x = -0.05, y = -80,
    xanchor = 'right', yanchor = 'bottom',
    text ='<b>Porcentagem de busca por voos<b>',
    textangle = -90,
    font = dict(
        family = 'Arial',
        size = 16,
        color = 'black'
    ),
    showarrow = False 
    ))

annotations.append(dict(
    xref = 'paper', yref = 'paper', x = 0.5, y = -0.8,
    xanchor = 'center', yanchor = 'top',
    text = "Fonte: https://www.kayak.com.br/tendencias-viagens",
    font = dict(
        family = 'Arial',
        size = 12,
        color = 'Gray'
    ),
    showarrow = False 
    ))

fig.update_layout(annotations = annotations)
#py.plot(fig, filename = 'Gráfico1.html')

app = dash.Dash()
app.layout = html.Div([
    dcc.Graph(figure = fig)
])

app.run_server(debug = True, use_reloader = False)