#Importação das bibliotecas Dash
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
#Importação das bibliotecas Plotly
import plotly.offline as py
import plotly.graph_objs as go

#Criação de listas que irão armazenar os dados
datas_totais = []
voos_domesticos = []
voos_internacionais = []
total_de_buscas_voos = []
dados = open('Gráfico 1.csv', 'r') #Arquivo .CSV é colocado em uma lista
for line in dados: #Leitura de linha por linha do arquivo
    line = line.strip() #Separação uma linha de outra por meio do .STRIP
    data, domes, inter, total = line.split(';')  #Sepação de cada elemento da linha em outras quatro variáveis
    datas_totais.append(data) #Adição da data de cada linha a lista
    voos_domesticos.append(domes) #Adição da porcentagem de domésticas de cada linha a lista
    voos_internacionais.append(inter) #Adição da porcentagem de internacionais de cada linha a lista
    total_de_buscas_voos.append(total) #Adição da porcentagem do total de buscas de cada linha a lista
#Deleta-se o primeiro elemento de cada lista por ser utilizado apenas para denominar as colunas no arquivo
del voos_domesticos[0]
del voos_internacionais[0]
del datas_totais[0]
del total_de_buscas_voos[0]

meses = ['Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', #É definida uma lista de valores para o filtro
 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Total']

#Função que ira receber um período escolhido no filtro e devolver os valores a serem exibidos
def escolhe_meses(mes_do_filtro):
    meses_abreviados = ['fev', 'mar', 'abr', 'mai', 'jun', 'jul', 'ago', 'set', 'out', 'total'] #Lista com as abreviações dos meses para facilitar a leitura do arquivo
    datas_x = [] #Lista que ira receber as datas filtradas a serem exibidas em X
    domesticas_y = [] #Lista que ira receber a porcentagem de buscas domésticas a serem exibidas no eixo Y
    internacionais_y = [] #Semelhante a lista anterior, só que com buscas internacionais
    total_de_buscas_y = [] #Semelhante a busca anterior, só que com o total de buscas

    #Ira ler a lista de meses e meses_abreviados ao mesmo tempo por meio da função "ZIP"
    for mes, abreviação in zip(meses, meses_abreviados): 
        if mes_do_filtro == mes: #Caso o mês escolhido para o parâmetro da função for igual ao mês lido pela função "FOR"...
            mes_escolhido = abreviação #É guardado em uma variável a abreviação correspondente ao mês escolhido
    for data in datas_totais: #Lê data por data
        posição = datas_totais.index(data) #Localiza e guarda em uma variável a posição de uma data específica 
        data = data.split() #Os elementos dessa data são divididos em uma lista de três elementos("15 de fev"->["15","de","fev"])
        if data[2] == mes_escolhido: #Se o último elemento dessa lista anteriormente criada for correspondente ao a abreviação do mês escolhido...
            data = " ".join(data) #Transforma-se e se armazena em uma variável os 3 elementos em um separados por um espaço, por meio do comando "JOIN"
            datas_x.append(data) #A lista com as datas filtradas recebe a data correspondente ao mês escolhido
            #A posição anteriormente definidade é usada para adicionar os dados restantes em suas listas, uma vez que todas as posições são correspondentes ao mesmo dado
            domesticas_y.append(voos_domesticos[posição])
            internacionais_y.append(voos_internacionais[posição])
            total_de_buscas_y.append(total_de_buscas_voos[posição])
        #Caso seja escolhido o total, são atribuidos todos os dados as suas respectivas listas
        if mes_escolhido == 'total':
            datas_x = datas_totais
            domesticas_y = voos_domesticos
            internacionais_y = voos_internacionais
            total_de_buscas_y = total_de_buscas_voos
    return datas_x, domesticas_y, internacionais_y, total_de_buscas_y #Retorna-se as quatro listas de dados filtradas

app = dash.Dash(__name__)
app.layout = html.Div([
    dcc.Dropdown(
        id = "filtro",
        options = [{'label': mes, 'value': mes}for mes in meses],
        value = 'Total',
        clearable = False
    ),
    dcc.Graph(
        id = "Gráfico")
])

@app.callback(
    Output(component_id='Gráfico', component_property= 'figure'),
    [Input(component_id='filtro', component_property='value')]
)

def update_gráfico(filtro):
    dados = escolhe_meses(filtro) #filtra-se os dados pela função "escolhe meses" e armazena-se em uma lista
    datas = dados[0] #A lista de datas filtradas(primeiro elemento da lista "dados") são armazenadas em uma variável
    domesticas = dados[1]
    internacionais = dados[2]
    total_de_buscas = dados[3]
    #Criação das linhas do gráfico
    trace1 = go.Scatter(x = datas, #As datas são atribuídas ao eixo X 
                    y = domesticas, #As porcentagens de busca por voos domésticos são atribuídos ao eixo Y
                    name = 'Domésticas', #Definido um nome a linha
                    text = datas, #Variável recebe os valores de X para exibição na função HOVER 
                    mode = 'lines', #É definido o tipo do gráfico
                    line = dict(color = 'rgb(242, 5, 5)'), #Atribuido uma cor para a linha 'Domésticas'
                    hovertemplate = '%{y}'.center(8) + '<br>'  + '%{text}' #São utilizados o as informações de Y e de X para vizualização do dado
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

    gráfico_de_linhas = [trace1, trace2, trace3] #Todas as linhas do gráfico são armazenadas em uma lista

    fig = go.Figure(gráfico_de_linhas) #A lista com as variáveis é transformada em um objeto para ser vizualizada na forma do gráfico

    #Definição do passo para exibição da legenda em X
    if len(datas) > 18: #Caso a quantidade de Datas for maior que 18...
        variação_legenda_x = len(datas)//18 #Divide-se a a quantidade de datas por 18, de forma que sejam exibidos no máximo 18 datas
    else: #Caso a quantidade de datas seja menor ou igual a 18...
        variação_legenda_x = 1 #Será atribuído passo 1 de forma a exibir todos as datas

    fig.update_layout( #Deifição das configurações de layout
        xaxis_title =dict( #Adição de um título que deixará mais claro que tipo de informação será exibida no eixo X
            text = "<b>Data<b>", #Texto que será exibido, colocado em negrito para maior destaque por meio do comando "<b><b>", da linguagem html
            font = dict( #São atribuídas algumas propriedades para o texto
                family = 'Arial', #A fonte do texto
                color = 'black', #A cor do texto
                size = 16 #Tamanho do texto em pixels
            )
        ),
        xaxis = dict( #São atribuídas propriedades para o eixo X e para seus dados
            rangeslider=dict(visible=True), #Um filtro do próprio Plotly
            showline = True, #Mostrar a linha do Eixo X
            tickmode = "linear", #É atribuído 'linear' no tipo de 'tick' para que se possa definir um valor incial para a exibição dos valores em X(tick0) e um passo(dtick)
            tick0 = datas[0], #Primeiro dado a ser exibido na legenda de X, no caso a primeira data
            dtick = variação_legenda_x, #Passo no qual os dados serão exibidos por meio da variável anteriormente definida
            showgrid = False, #Não mostrar a grade de linhas do eixo X
            linecolor = 'rgb(63, 64, 63)', #Cor da linha do eixo X
            linewidth = 2, #Espessura da linha do eixo X
            ticks = 'outside' #Adição de "traços" do lado de fora do gráfico para melhor vizualização dos dados
        ),
        yaxis = dict( #Atribuição de propriedades para o eixo Y e seus respectivos dados
            gridcolor = 'rgb(63, 64, 63)', #Definição da cor da grade de linhas do eixo Y
            zeroline = False, #Para que a linha zero do eixo Y se mostre é atribuido "False" ao comando "zeroline"
            linecolor = "rgb(63, 64, 63)", #É atrbuído uma cor a linha do eixo Y
            showticklabels = False, #É dado o comando para não mostrar a legenda padrão do Plotly
            ticksuffix = '%' #É adicionado '%' ao final de todos os dados do eixo Y
        ),
        margin = dict( #Configurações com relação as margens do gráfico
            t = 50, #Distância do gráfico do topo da página em pixels
            l = 100 #Distância do gráfico da lateral esquerda em pixels
        ),
        height = 580, #Altura do gráfico em pixels
        plot_bgcolor = 'white', #Definição de cor do background do gráfico
        hoverlabel = dict( #Atrubuição das propriedades para o HOVER
            bgcolor = '#3F3F3F', #Cor do background do HOVER
            align = 'auto', #Alinhamento do texto do hover automático
            font = dict( #Configurações para o texto do hover
                family = 'Arial', #Fonte do texto
                size = 16, #Tamanho do texto em pixels
                color = 'white' #Cor do texto
            )
        )
    )

    annotations = [] #Criação da lista anotações que ira ser utilizada pra duas legendas do eixo Y e a fonte de origem dos dados
    valores_de_y = [-50, 0, 50, 100] #Valores que serão exibidos no eixo Y

    for valor_y in valores_de_y: #Se percorre toda a lista anteriormente criada
        annotations.append(dict( #Cada valor da lista é adicionado com uma série de propriedades a lista "annotations"
            xref = 'paper', #Coordenada da informação no eixo X, recebe 'paper' que irá definir toda a extensão do gráfico como valendo 1
            x = 0.00005, #Coordenado do eixo X sendo definida entre 0 e 1, de acordo com a função 'paper' anteriormente definida
            y = valor_y, #A coordenada no eixo Y é definida de acordo com os elemntos da lista, uma vez que os mesmos são números
            xanchor = 'right', #Orientação do texto com relação ao eixo X
            yanchor = 'middle', #Orientação do texto com relação ao eixo Y
            text ='{}%'.format(valor_y), #Definição do texto que será exibido
            showarrow = False #Não mostrar uma seta indicando a coordenada exata das anotações
        ))

    #Definição de uma legenda  no eixo Y para deixar claro a que se referem as informações
    annotations.append(dict(
        xref = 'paper', x = -0.05, y = -80,
        xanchor = 'right', yanchor = 'bottom',
        text ='<b>Porcentagem de busca por voos<b>',
        textangle = -90, #Inclinação do texto na vertical para melhor vizualização no eixo Y
        font = dict(
            family = 'Arial',
            size = 16,
            color = 'black'
        ),
        showarrow = False 
        ))

    #Atribuição de um texto que dá a fonte dos dados
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

    fig.update_layout(annotations = annotations) #A lista com todas as legendas e outras informações são atribuidas ao comando annotations, e adicionadas as configurações de layout
    return fig 
#py.plot(fig, filename = 'Gráfico1.html')

if __name__ == '__main__':
    app.run_server(debug = True, use_reloader = False)