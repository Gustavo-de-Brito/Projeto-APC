import plotly.offline as py
import plotly.graph_objs as go
py.init_notebook_mode(connected=True)

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

trace1 = go.Scatter(x = datas,
                   y = domesticas,
                   mode = 'lines',
                   name = 'Domésticas')

trace2 = go.Scatter(x = datas,
                   y = internacionais,
                   mode = 'lines',
                   name = 'Internacionais',)

data = [trace1, trace2]
layout = go.Layout(title = 'Busca de Voos Domésticas vs. Internacionais',)
py.plot(data, filename='grafico.html')