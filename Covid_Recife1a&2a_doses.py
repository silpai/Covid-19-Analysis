! pip install Plotly
! pip install cufflinks
! pip install chart_studio

# import packages
import pandas as pd # dataframes
from pandas import Series, DataFrame
import numpy as np

import matplotlib
import matplotlib.pyplot as plt


import datetime as dt

import cufflinks as cf  #for the plotly

import chart_studio
import chart_studio.plotly as py
import plotly.graph_objs as go

chart_studio.tools.set_credentials_file(username="silpai", api_key="")

#Calculate % of the doses applied

URL = 'https://conectarecife.recife.pe.gov.br/vacinometro/'
doses= pd.read_html(URL, thousands=".")[3] # get the 3rd table, recognize . as thousand
doses=doses.rename(columns={"Grupo Prioritário": "GrupoPrioritário", "Dose 1": "Dose1", "Dose 1.1": "Dose11", "Dose 2": "Dose2", "Dose 2.1": "Dose21"}, inplace = False)
doses = doses[~doses.Dose11.isin(['Total'])] # drop row with total 
doses['Pop2020_Rec'] =int(1653461)
doses['perct_1aDose'] = round((doses['Dose11'].astype(int)/ doses['Pop2020_Rec'].astype(int)*100),2)
doses['perct_2aDose'] = round(((doses['Dose21'].astype(int) ) / doses['Pop2020_Rec'].astype(int)*100),2)
doses['perct_Unica'] = round(((doses['Dose única.1'].astype(int)) / doses['Pop2020_Rec'].astype(int)*100),2)
doses['perct_2aDose_Unica'] = round(((doses['Dose21'].astype(int) +doses['Dose única.1'].astype(int)) / doses['Pop2020_Rec'].astype(int)*100),2)
doses

#Retreve date
dose_data = pd.read_html(URL, thousands=".")[3] # get the 3rd table, recognize . as thousand
dose_data['date'] = pd.to_datetime(dose_data['Dose 1'].head(1))
end=pd.to_datetime(dose_data['Dose 1'].head(1))
dose_data=dose_data.rename(columns={"Grupo Prioritário": "GrupoPrioritário", "Dose 1": "Dose1", "Dose 1.1": "Dose11", "Dose 2": "Dose2", "Dose 2.1": "Dose21"}, inplace = False)

dose_data = dose_data.head(1)[["date"]]
dose_data


dos = pd.concat((doses,dose_data),axis=1)
dos.where(pd.notna(dos), dos.date.head(1), axis="columns")
dos


#Speedometro 1a dose
fig1a = go.Figure(go.Indicator(
    domain = {'x': [0, 1], 'y': [0, 1]},
    value = float(dos['perct_1aDose'].tail(1)),
     number = {'suffix': "%"},
   mode = "gauge+number",
    title = {'text':"<b> RECIFE </b><br><span style='color: gray;font-size:0.8em'> % População com 1ª dose da vacina do Covid-19</span>", 
             'font': {"size": 20}},
    gauge = {'axis': {'range': [None, 100]},
             'bar': {'color': 'white'},
             'steps' : [ {'range': [0, 20], 'color': "#F2726F"},
                 {'range': [20, 50], 'color': "#fcff33"},
                 {'range': [50, 70], 'color': "#FFC533"},
                 {'range': [70, 100], 'color': "#89D958"}],
             'threshold' : {'line': {'color': "black", 'width': 4}, 'thickness': 0.75, 'value': 80}}))

fig1a.add_annotation(text= f"{dose_data} <br> Baseada na população do Recife de 1,653,461 habitantes <br> Repositório - https://github.com/silpai/Covid-19-Analysis<br> Dados: github.com/wcota/covid19br | conectarecife.recife.pe.gov.br/vacinometro <br>",
                  xref="paper", yref="paper",
                  x=0.50, y=-0.25, showarrow=False)

py.iplot(fig1a,filename="Recife-1aDose-Vacina-Covid19") # to show in jupter

#Speedometro 2a dose
fig2a = go.Figure(go.Indicator(
    domain = {'x': [0, 1], 'y': [0, 1]},
    value = float(dos['perct_2aDose_Unica'].tail(1)),
     number = {'suffix': "%"},
   mode = "gauge+number",
    title = {'text':"<b> RECIFE </b><br><span style='color: gray;font-size:0.8em'> % População com 2ª dose ou dose única da vacina do Covid-19</span>", 
             'font': {"size": 20}}, 
              gauge = {'axis': {'range': [None, 100]},
             'bar': {'color': 'white'},
             'steps' : [ {'range': [0, 20], 'color': "#F2726F"},
                 {'range': [20, 50], 'color': "#fcff33"},
                 {'range': [50, 70], 'color': "#FFC533"},
                 {'range': [70, 100], 'color': "#89D958"}],
             'threshold' : {'line': {'color': "black", 'width': 4}, 'thickness': 0.75, 'value': 80}}))
fig2a.add_annotation(text= f"{dose_data} <br> Baseada na população do Recife de 1,653,461 habitantes <br> Repositório - https://github.com/silpai/Covid-19-Analysis<br> Dados: github.com/wcota/covid19br | conectarecife.recife.pe.gov.br/vacinometro <br>",
                  xref="paper", yref="paper",
                  x=0.50, y=-0.25, showarrow=False)
py.iplot(fig2a,filename="Recife-2aDose-Vacina-Covid19") # to show in jupter

