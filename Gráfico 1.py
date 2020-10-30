import dash
import dash_core_components as dcc
import dash_html_components as html

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

trace1 = go.Scatter(x = datas,
                   y = domesticas, 
                   name = 'Domésticas',
                   text = 'Domésticas',
                   mode = 'lines',
                   line = dict(color = 'rgb(242, 5, 5)'),
                   hovertemplate = ''.center(4)+'%{y:.2f}%<br>'+ ''.center(2)+'%{x}'+''.center(2)
                   )

trace2 = go.Scatter(x = datas,
                   y = internacionais,
                   mode = 'lines',
                   name = 'Internacionais',
                   line = dict(color = 'rgb(5, 13, 166)'),
                   hovertemplate = ''.center(4)+'%{y:.2f}%<br>'+ ''.center(2)+'%{x}'+''.center(2)
                   )

trace3 = go.Scatter(x = datas,
                   y = total_de_buscas,
                   mode = 'lines',
                   name = 'Total de buscas',
                   line = dict(color = 'rgb(13, 13, 13)'),
                   hovertemplate = ''.center(4)+'%{y:.2f}%<br>'+ ''.center(2)+'%{x}'+''.center(2)
)

gráfico_de_linhas = [trace1, trace2, trace3]

fig = go.Figure(gráfico_de_linhas)

fig.update_layout(
    xaxis = dict(
        showline = True,
        showgrid = False,
        showticklabels = False,
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
        l = 150,
        r = 20,
        t = 40
    ),
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


valores_de_x = []
w = 0
while w < len(datas) - 1:
    valores_de_x.append(datas[w])
    w = w + 21
valores_de_x.append(datas[-1])

taxa_de_variação_x = 1/(len(datas) - 1)
coordenada_x = taxa_de_variação_x * 8
p = 1
variação_coordenadas_x = 0
while p <= 21:
    variação_coordenadas_x = variação_coordenadas_x + taxa_de_variação_x
    p = p + 1

for valor_x in valores_de_x:
    annotations.append(dict(
        xref = 'paper', yref = 'paper', x = coordenada_x, y = -0.08,
        xanchor = 'right', yanchor = 'bottom',
        text = valor_x,
        showarrow = False 
        ))
    coordenada_x = coordenada_x + variação_coordenadas_x
coordenada_x = coordenada_x + variação_coordenadas_x

annotations.append(dict(
    xref = 'paper', yref = 'paper', x = 0.5, y = -0.16,
    xanchor = 'center', yanchor = 'bottom',
    text ='<b>Datas<b>',
    font = dict(
        family = 'Arial',
        size = 16,
        color = 'black'
    ),
    showarrow = False 
    ))

annotations.append(dict(
    xref = 'paper', yref = 'paper', x = -0.05, y = 0.17,
    xanchor = 'right', yanchor = 'bottom',
    text ='<b>Porcentagem de busca de voos<b>',
    textangle = -90,
    font = dict(
        family = 'Arial',
        size = 16,
        color = 'black'
    ),
    showarrow = False 
    ))

annotations.append(dict(
    xref = 'paper', yref = 'paper', x = 0.5, y = -0.18,
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
