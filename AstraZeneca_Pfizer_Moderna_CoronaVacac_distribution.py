! pip install Plotly
! pip install cufflinks
! pip install chart_studio

# import packages
import pandas as pd 
from pandas import Series, DataFrame
import numpy as np

import matplotlib
import matplotlib.pyplot as plt




import datetime as dt

import cufflinks as cf  #for the plotly

import chart_studio
import chart_studio.plotly as py
import plotly.express as px

import html5lib

#chart_studio.tools.set_credentials_file(username="XXX", api_key="XXXX")

URL ='https://ourworldindata.org/covid-vaccinations'
df= pd.read_html(URL)
df=pd.concat(df) ##transform html list into dataframe
df['date'] = pd.to_datetime(df['Last observation date'])
df=df[["Location","date","Vaccines"]] # select columns


#split vaccines
split_df=df.join(df['Vaccines'].str.split(', ', 5, expand=True).rename(columns={0:'A', 1:'B',2:'C',3:'D',4:'E',5:'F',6:'G'}))

#pivot long
pivot= pd.melt(split_df, id_vars=["Location","date","Vaccines"], value_vars=['A','B','C','D','E'],
        var_name='position', value_name='vaccine_type').reset_index()
pivot=pivot.dropna() # remove the "None"

#pivot[pivot['Location']=="Brazil"]
#table[table['Location']=="Brazil"].dropna()
#pivot["vaccine_type"].unique()

conditions = [
    pivot['vaccine_type'].eq('Oxford/AstraZeneca'),
    pivot['vaccine_type'].eq('Sputnik V'),
    pivot['vaccine_type'].eq('Johnson&Johnson'),
    pivot['vaccine_type'].eq('Covaxin'),
    pivot['vaccine_type'].eq('Sinovac'),
    pivot['vaccine_type'].isin(['Pfizer/BioNTech', 'Moderna']),
    pivot['vaccine_type'].isin(['Sinopharm/Beijing','CanSino', 'Abdala', 'QazVac', 'EpiVacCorona','Soberana02', 'Sinopharm/HayatVax', 'RBD-Dimer', 'Sinopharm/Wuhan'])
]

choices = ["AstraZeneca","Sputnik V", "Johnson&Johnson","Moderna","CoronaVac","Pfizer | Moderna","Others"]

pivot['vac_category'] = np.select(conditions, choices)

# COVID-19 Oxford/AstraZeneca Vaccine Distribution
az=pivot[pivot['vac_category']=="AstraZeneca"]

fig_az = px.choropleth(az,locations= 'Location', 
                    locationmode="country names",
                    color= 'vac_category',
                    hover_name ='Location',
                    hover_data ={'Location':False, 'vac_category':False},
                    color_discrete_map={'AstraZeneca': '#c5a989'},
                    labels={'vac_category': ' '} # remove legend title               
                               
                    
                    
                   )
fig_az.update_layout(
    title_text='COVID-19 Oxford/AstraZeneca Vaccine Distribution',
    geo=dict(
        showframe=False,
        showcoastlines=False    )
)

fig_az.add_annotation(text= f" Source: https://ourworldindata.org/covid-vaccinations <br> Repository: https://github.com/silpai/Covid-19-Analysis | https://chart-studio.plotly.com/~silpai#/ <br>",
                  xref="paper", yref="paper",
                  x=0.50, y=-0.15, showarrow=False)
py.iplot(fig_az,filename="AstraZeneca_worldwide")


# COVID-19 Pfizer | Moderna Vaccine Distribution
pm=pivot[pivot['vac_category']=="Pfizer | Moderna"]


fig_pm = px.choropleth(pm,locations= 'Location', 
                    locationmode="country names",
                    color= 'vac_category',
                    hover_name ='Location',
                    hover_data ={'Location':False, 'vac_category':False},
                    color_discrete_map={'Pfizer | Moderna': '#ce9D33'},
                    labels={'vac_category': ' '} # remove legend title
                    
                             
                  
                    
                   )
fig_pm.update_layout(
    title_text='COVID-19 Pfizer | Moderna Vaccine Distribution',
    geo=dict(
        showframe=False,
        showcoastlines=False    )
)

fig_pm.add_annotation(text= f" Source: https://ourworldindata.org/covid-vaccinations <br> Repository: https://github.com/silpai/Covid-19-Analysis | https://chart-studio.plotly.com/~silpai#/ <br>",
                  xref="paper", yref="paper",
                  x=0.50, y=-0.15, showarrow=False)
py.iplot(fig_pm,filename="Pfizer_Moderna_worldwide") 

# COVID-19 CoronaVac Vaccine Distribution
c=pivot[pivot['vac_category']=="CoronaVac"]


fig_c = px.choropleth(c,locations= 'Location', 
                    locationmode="country names",
                    color= 'vac_category',
                    hover_name ='Location',
                    hover_data ={'Location':False, 'vac_category':False},
                    color_discrete_map={'CoronaVac': '#c62632'},
                    labels={'vac_category': ' '} # remove legend title
                    
                             
                  
                    
                   )
fig_c.update_layout(
    title_text='COVID-19 CoronaVac Vaccine Distribution',
    geo=dict(
        showframe=False,
        showcoastlines=False    )
)

fig_c.add_annotation(text= f" Source: https://ourworldindata.org/covid-vaccinations <br> Repository: https://github.com/silpai/Covid-19-Analysis | https://chart-studio.plotly.com/~silpai#/ <br>",
                  xref="paper", yref="paper",
                  x=0.50, y=-0.15, showarrow=False)
py.iplot(fig_c,filename="CoronaVac_worldwide") 
