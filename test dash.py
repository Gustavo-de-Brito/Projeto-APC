import dash
import dash_core_components as dcc
import dash_html_components as html

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

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),

    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': datas, 'y': domesticas, 'type': 'line', 'name': 'Domésticas'},
                {'x': datas, 'y': internacionais, 'type': 'line', 'name': u'Internacionais'},
            ],
            'layout': {
                'title': 'Busca de Voos Domésticos vs. Internacionais'
            }
        }
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)