"""
CO2 Emissions Visualization
This Python application is designed to visualize global CO2 emissions data using 
an interactive web-based interface. It leverages the Taipy GUI framework to 
create a dynamic and responsive app that displays CO2 emissions across different 
countries and years through a choropleth map and accompanying data tables.


"""
from taipy.gui import Gui 
import taipy.gui.builder as tgb
import pandas as pd
import plotly.express as px


df_all_countries = pd.read_csv('co2_total.csv')
df_all_countries = df_all_countries.drop(columns=['Unnamed: 0'])
df_world = pd.read_csv('co2_total_world.csv')
df_world = df_world.drop(columns=['Unnamed: 0'])

col = 'Annual CO₂ emissions'        
max = df_all_countries[col].max()      
min = df_all_countries[col].min()     
ymax = 2021 
ymin = 1950 

year = ymax                          

all_countries = list(df_all_countries['Entity'].unique())
countries = ['France','United Kingdom'] 

df_working_list = df_all_countries[
    (df_all_countries['Year']==year)&               
    (df_all_countries['Entity'].isin(countries))
    ]

def plot_choro(year):

    fig = px.choropleth(df_all_countries[df_all_countries['Year']==year], 
                        locations="Code",     
                        color=col,            
                        hover_name="Entity",   
                        range_color=(min,max),  
                        scope= 'world',    
                        projection='equirectangular', 
                        title='World CO2 Emissions',
                        color_continuous_scale=px.colors.sequential.Reds,
                        )
    fig.update_layout(margin={'r':50, 't':0, 'b':0, 'l':0}) 
    return fig

def update_data(state):

    state.df_working_list = state.df_all_countries[
        (state.df_all_countries['Year']==state.year)&
        (state.df_all_countries['Entity'].isin(state.countries))
        ]
    state.fig = plot_choro(state.year)

fig = plot_choro(ymax)

with tgb.Page() as page:

    tgb.text( "# World CO2 Emissions from {ymin} to {ymax}", mode='md')
    tgb.text("---", mode='md')

    with tgb.layout(columns="3 2"):

        with tgb.part():
            with tgb.layout(columns="1 1"):
                with tgb.part():
                    tgb.text(value="#### Use the slider to select a year", mode='md')
                    tgb.slider(value="{year}",min=ymin, max=ymax, on_change=update_data)                    
                with tgb.part():
                    tgb.text("#### Total global emissions for {year}:", mode='md')
                    tgb.text("##### {int(df_world[df_world['Year']==year]['Annual CO₂ emissions'].iloc[0])} tonnes", mode='md')            
            
                

            tgb.chart(figure="{fig}")

        with tgb.part():

            tgb.text(value="#### World temperature data", mode='md')
            tgb.text(value="##### Select or reject countries from the dropdown list", mode='md')
            with tgb.layout(columns="1 2"):
                tgb.selector(value="{countries}", lov="{all_countries}", multiple=True,dropdown=True, width=1000 ,on_change=update_data)            

                tgb.chart("{df_working_list}", type="bar", x="Entity", y=col)

    tgb.text("Global CO2 Emission Data from {ymin} to {ymax}. Data derived from  [Our World in Data](https://ourworldindata.org/) (with thanks)", mode='md')

Gui(page=page).run()