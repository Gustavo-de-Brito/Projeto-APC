#Importação do Dash
import dash
import dash_core_components as dcc
import dash_html_components as html

#Importação da biblioteca Plotly
import plotly.offline as py
import plotly.graph_objs as go

datas = []
domesticas = []
internacionais = []
total_de_buscas = []
dados = open('Gráfico 1.csv', 'r')
for line in dados:
    line = line.strip()
    Da, Do, In, To = line.split(';')
    datas.append(Da)
    domesticas.append(Do)
    internacionais.append(In)
    total_de_buscas.append(To)

#Transformação dos dados no gráfico com os comandos do Plotly
trace1 = go.Scatter(x = datas,
                   y = domesticas,
                   mode = 'lines',
                   name = 'Domésticas')

trace2 = go.Scatter(x = datas,
                   y = internacionais,
                   mode = 'lines',
                   name = 'Internacionais',)

trace3 = go.Scatter(x = datas,
                   y = total_de_buscas,
                   mode = 'lines',
                   name = 'Total de buscas',)

gráfico_de_linhas = [trace1, trace2, trace3]

fig = go.Figure(gráfico_de_linhas)

fig.update_layout(
    xaxis = dict(
        showline = True,
        showgrid = False,
        showticklabels = False,
        linecolor = 'rgb(204, 204, 204)',
        linewidth = 2,
        ticks = 'outside',
    ),
    yaxis = dict(
        showgrid = True,
        gridcolor = 'rgb(204, 204, 204)',
        zeroline = False,
        showline = False,
        showticklabels = False
    ),
    autosize = True,
    margin = dict(
        autoexpand = True,
        l = 100,
        r = 20,
        t = 100
    ),
    plot_bgcolor = 'white'
)

legenda_y = []
valores_de_y = [-50, 0, 50, 100]

for valor_y in valores_de_y:
    legenda_y.append(dict(
        xref = 'paper', x = 0, y = valor_y,
        xanchor = 'right', yanchor = 'middle',
        text ='{}%'.format(valor_y),
        showarrow = False 
    ))

valores_de_x = []
w = 1
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
    legenda_y.append(dict(
        xref = 'paper', yref = 'paper', x = coordenada_x, y = -0.1,
        xanchor = 'right', yanchor = 'bottom',
        text = valor_x,
        showarrow = False 
        ))
    coordenada_x = coordenada_x + variação_coordenadas_x

fig.update_layout(annotations=legenda_y)

py.plot(fig, filename = 'Gráfico1.html')

#app = dash.Dash()
#app.layout = html.Div([
#    dcc.Graph(figure = fig)
#])

#app.run_server(debug = True, use_reloader = False)