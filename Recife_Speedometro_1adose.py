pip install dash dash-renderer dash-html-components dash-core-components plotly 

import pandas as pd
import datetime

import plotly
import plotly.express as px  # (version 4.7.0)
import plotly.graph_objects as go

import dash  # (version 1.12.0) 
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_auth

app = dash.Dash(__name__)
server= Recife_Speedometro_1adose.server

# ---------- Import and clean data (importing csv into pandas)
URL = 'https://conectarecife.recife.pe.gov.br/vacinometro/'
data = pd.read_html(URL, thousands=".")[1] # get the 3rd table, recognize . as thousand
data['Atualização'] = pd.to_datetime(data['Dose 1'].head(1))
end=pd.to_datetime(data['Dose 1'].head(1))
data=data.rename(columns={"Grupo Prioritário": "GrupoPrioritário", "Dose 1": "Dose1", "Dose 1.1": "Dose11", "Dose 2": "Dose2", "Dose 2.1": "Dose21"}, inplace = False)

#Retreve date
dose_data = data.head(1)[["Atualização"]]

#Calculate % of the doses applied
doses = data[~data.Dose11.isin(['Total*'])] # drop row with total 
doses['Pop2020_Rec'] =int(1653461)
doses['perct_1aDose'] = round((doses['Dose11'].astype(int)/ doses['Pop2020_Rec'].astype(int)*100),2)
doses['perct_2aDose'] = round((doses['Dose21'].astype(int)/ doses['Pop2020_Rec'].astype(int)*100),2)

dos = pd.concat((dose_data,doses))
dos.where(pd.notna(dos), dos.Atualização.head(1), axis="columns")
dos



# ------------------------------------------------------------------------------
# App layout with dash components #https://dash.plotly.com/dash-core-components

app.layout = html.Div([
    #html.H1(children="Vacinas Covid-19", style={'text-align': 'center'}), # title url
    dcc.Graph(id='live-update-graph'),
    dcc.Interval(
            id='interval-component',
            interval=1*86400000, # in milliseconds
            n_intervals=0)
    ])

# ------------------------------------------------------------------------------
# Multiple components can update everytime interval gets fired.
@app.callback(Output('live-update-graph', 'figure'),
              Input('interval-component', 'n_intervals'))

# ------------------------------------------------------------------------------
def update_graph_live(n):
    URL = 'https://conectarecife.recife.pe.gov.br/vacinometro/'
    data = pd.read_html(URL, thousands=".")[1] # get the 3rd table, recognize . as thousand
    data['Atualização'] = pd.to_datetime(data['Dose 1'].head(1))
    end=pd.to_datetime(data['Dose 1'].head(1))
    data=data.rename(columns={"Grupo Prioritário": "GrupoPrioritário", "Dose 1": "Dose1", "Dose 1.1": "Dose11", "Dose 2": "Dose2", "Dose 2.1": "Dose21"}, inplace = False)
#Retreve date
    dose_data = data.head(1)[["Atualização"]]
#Calculate % of the doses applied
    doses = data[~data.Dose11.isin(['Total*'])] # drop row with total 
    doses['Pop2020_Rec'] =int(1653461)
    doses['perct_1aDose'] = round((doses['Dose11'].astype(int)/ doses['Pop2020_Rec'].astype(int)*100),2)
    doses['perct_2aDose'] = round((doses['Dose21'].astype(int)/ doses['Pop2020_Rec'].astype(int)*100),2)

    dos = pd.concat((dose_data,doses))
    dos.where(pd.notna(dos), dos.Atualização.head(1), axis="columns")
    

 # Create the graph with subplots
    fig1a = go.Figure(go.Indicator(
                domain = {'x': [0, 1], 'y': [0, 1]},
                value = float(dos['perct_1aDose'].tail(1)),
                number = {'suffix': "%"},
                mode = "gauge+number",
                title = {'text':"<b> RECIFE </b><br><span style='color: gray;font-size:0.8em'> % População com 1ª dose da vacina do Covid-19</span>", 
                 'font': {"size": 20}},
               gauge = {'axis': {'range': [None, 100]},
                'bar': {'color': 'lightgray'},
                'steps' : [ {'range': [0, 20], 'color': "#F2726F"},
                 {'range': [20, 50], 'color': "#fcff33"},
                 {'range': [50, 70], 'color': "#FFC533"},
                 {'range': [70, 100], 'color': "#89D958"}],
               'threshold' : {'line': {'color': "black", 'width': 4}, 'thickness': 0.75, 'value': 80}}))

    fig1a.add_annotation(text= f"{dose_data} <br> Basead na população do Recife de 1,653,461 habitantes <br> Repositório - https://github.com/silpai/Covid-19-Analysis/tree/master/Python/<br> Dados: github.com/wcota/covid19br | conectarecife.recife.pe.gov.br/vacinometro <br>",
                  xref="paper", yref="paper",
                  x=0.50, y=-0.25, showarrow=False),
                
 
    
                 
    return fig1a    
    
if __name__ == '__main__':
    #app.run_server(debug=False)
    app.run_server(debug=True, use_reloader= False)
