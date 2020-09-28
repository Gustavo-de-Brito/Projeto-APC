#Importação do Dash
import dash
import dash_core_components as dcc
import dash_html_components as html

#Importação da biblioteca Plotly
import plotly.offline as py
import plotly.graph_objs as go
py.init_notebook_mode(connected=True)

#Leitura do documento .csv, separando as três fileiras do mesmo em três listas diferentes
datas = []
domesticas = []
internacionais = []
dados = open('Gráfico 1.csv', 'r')
for line in dados:
    line = line.strip()
    Da, Do, In = line.split(';')
    datas.append(Da)
    domesticas.append(Do)
    internacionais.append(In)

#Transformação dos dados no gráfico com os comandos do Plotly
trace1 = go.Scatter(x = datas,
                   y = domesticas,
                   mode = 'lines',
                   name = 'Domésticas')

trace2 = go.Scatter(x = datas,
                   y = internacionais,
                   mode = 'lines',
                   name = 'Internacionais',)

gráfico_de_linhas = [trace1, trace2]

#Importação do gráfico("gráfico_de_linhas") para exibição no Dash
fig = go.Figure(gráfico_de_linhas)
app = dash.Dash()
app.layout = html.Div([
    dcc.Graph(figure = fig)
])

app.run_server(debug = True, use_reloader = False)