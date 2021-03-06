
#importing the libraries
import pandas as pd

import webbrowser


import dash
import dash_html_components as html 
import dash_core_components as dcc 
from dash.exceptions import PreventUpdate


import plotly.graph_objects as go  
import plotly.express as px


app = dash.Dash()
app.config.suppress_callback_exceptions = True


def load_data():
  dataset_name = "global_terror.csv"
  global data
  data = pd.read_csv(dataset_name)
  

  global month_list,date_list,region_list,country_list,state_list,city_list,attack_type_list,year_list,year_dict,chart_dropdown_values
  month = {
         "January":1,
         "February": 2,
         "March": 3,
         "April":4,
         "May":5,
         "June":6,
         "July": 7,
         "August":8,
         "September":9,
         "October":10,
         "November":11,
         "December":12
         }
  month_list= [{"label":key, "value":values} for key,values in month.items()]
  date_list = [x for x in range(1, 32)]
  region_list = [{"label": str(i), "value": str(i)}  for i in sorted( data['region_txt'].unique().tolist() ) ]
  country_list = data.groupby("region_txt")["country_txt"].unique().apply(list).to_dict()
  state_list = data.groupby("country_txt")["provstate"].unique().apply(list).to_dict()
  city_list  = data.groupby("provstate")["city"].unique().apply(list).to_dict()
  attack_type_list = [{"label": str(i), "value": str(i)}  for i in data['attacktype1_txt'].unique().tolist()]
  year_list = sorted ( data['iyear'].unique().tolist()  )  
  year_dict = {str(year): str(year) for year in year_list}  
  chart_dropdown_values = {"Terrorist Organisation":'gname', 
                             "Target Nationality":'natlty1_txt', 
                             "Target Type":'targtype1_txt', 
                             "Type of Attack":'attacktype1_txt', 
                             "Weapon Type":'weaptype1_txt', 
                             "Region":'region_txt', 
                             "Country Attacked":'country_txt'
                          }
                              
  chart_dropdown_values = [{"label":keys, "value":value} for keys, value in chart_dropdown_values.items()]
  
def open_browser():
  # Open the default web browser
  webbrowser.open_new('http://127.0.0.1:8050/')
# Layout of your page
def create_app8_ui():
  # Create the UI of the Webpage here
  main_layout = html.Div(style={'background-color':'#6dd5ed'},children=[
  html.H1('Terrorism Analysis with Insights', id='Main_title',style={'background-color':'#cc0000','color':'#FFFFFF','font-size':'35px','textAlign':'center'}),
  dcc.Tabs(id="Tabs", value="Map",style={'background-color': ' #de6262' ,'color':'#ffffff','font-size':'20px'},children=[
      dcc.Tab(label="Map tool" ,id="Map tool",value="Map",style={'background-color': '#008080 ' ,'color':'#ffffff','font-size':'20px'}, children=[
          dcc.Tabs(id = "subtabs", value = "WorldMap",style={'background-color': '#008080' ,'color':'#ffffff','font-size':'20px'},children = [
              dcc.Tab(label="World Map tool", id="World", value="WorldMap",style={'background-color': '#008080' ,'color':'#ffffff','font-size':'20px'}),
              dcc.Tab(label="India Map tool", id="India", value="IndiaMap",style={'background-color': '#008080' ,'color':'#ffffff','font-size':'20px'})
              ]),
         
          dcc.Dropdown(
              id='month', 
                options=month_list,
                placeholder='Select Month',
                multi = True,style={
                            
                            
                             'background-color': '#d9d9d9 ' ,'color':'#000000','font-size':'20px',}
                  ),
                
          dcc.Dropdown(
                id='date', 
                placeholder='Select Day',
                multi = True,style={'background-color': '#d9d9d9 ' ,'color':'#000000','font-size':'20px',}
                  ),
          
          dcc.Dropdown(
                id='region-dropdown', 
                options=region_list,
                placeholder='Select Region',
                multi = True,style={'background-color': '#d9d9d9' ,'color':'#000000','font-size':'20px'}
                  ),
          dcc.Dropdown(
                id='country-dropdown', 
                options=[{'label': 'All', 'value': 'All'}],
                placeholder='Select Country',
                multi = True,style={'background-color': '#d9d9d9 ' ,'color':'#000000','font-size':'20px'}
                  ),
          dcc.Dropdown(
                id='state-dropdown', 
                options=[{'label': 'All', 'value': 'All'}],
                placeholder='Select State or Province',
                multi = True,style={'background-color': '#d9d9d9 ' ,'color':'#000000','font-size':'20px'}
                  ),
          dcc.Dropdown(
                id='city-dropdown', 
                options=[{'label': 'All', 'value': 'All'}],
                placeholder='Select City',
                multi = True,style={'background-color': '#d9d9d9 ' ,'color':'#000000','font-size':'20px'}
                  ),
          dcc.Dropdown(
                id='attacktype-dropdown', 
                options=attack_type_list,#[{'label': 'All', 'value': 'All'}],
                placeholder='Select Attack Type',
                multi = True,style={'background-color': '#d9d9d9' ,'color':'#000000','font-size':'20px'}
                  ),
          html.H5('Select the Year', id='year_title'),
          dcc.RangeSlider(
                    id='year-slider',
                    min=min(year_list),
                    max=max(year_list),
                    value=[min(year_list),max(year_list)],
                    marks=year_dict,
                    step=None
                      ),
          html.Br()
    ]),
      dcc.Tab(label = "Chart Tool", id="chart tool", value="Chart",style={'background-color': '#008080 ' ,'color':'#ffffff','font-size':'20px'}, children=[
          dcc.Tabs(id = "subtabs2", value = "WorldChart",style={'background-color': '#008080 ' ,'color':'#ffffff','font-size':'20px'},children = [
              dcc.Tab(label="World Chart tool", id="WorldC", value="WorldChart",style={'background-color': '#008080' ,'color':'#ffffff','font-size':'20px'}),          
            dcc.Tab(label="India Chart tool", id="IndiaC", value="IndiaChart",style={'background-color': '#008080' ,'color':'#ffffff','font-size':'20px'})]),
            dcc.Dropdown(id="Chart_Dropdown", options = chart_dropdown_values, placeholder="Select option", value = "region_txt",style={'background-color': '#d9d9d9 ' ,'color':'#000000','font-size':'20px'}), 
            html.Br(),
            html.Br(),
            html.Hr(),
            dcc.Input(id="search", placeholder="Search Filter",style={'background-color':'#9999ff','color':'#00000'}),
            html.Hr(),
            html.Br(),
            dcc.RangeSlider(
                    id='year_slider1',
                    min=min(year_list),
                    max=max(year_list),
                    value=[min(year_list),max(year_list)],
                    marks=year_dict,
                    step=None
                      ),
                  html.Br()
              ]),
         ]),
  html.Div(id = "graph-object", children ="Graph will be shown here")
  ])
        
  return main_layout

@app.callback(dash.dependencies.Output('graph-object', 'children'),
    [
     dash.dependencies.Input("Tabs", "value"),
    dash.dependencies.Input('month', 'value'),
    dash.dependencies.Input('date', 'value'),
    dash.dependencies.Input('region-dropdown', 'value'),
    dash.dependencies.Input('country-dropdown', 'value'),
    dash.dependencies.Input('state-dropdown', 'value'),
    dash.dependencies.Input('city-dropdown', 'value'),
    dash.dependencies.Input('attacktype-dropdown', 'value'),
    dash.dependencies.Input('year-slider', 'value'), 
    dash.dependencies.Input('year_slider1', 'value'), 
    
    dash.dependencies.Input("Chart_Dropdown", "value"),
    dash.dependencies.Input("search", "value"),
    dash.dependencies.Input("subtabs2", "value")
    ]
    )
def update_app9_ui(Tabs, month_value, date_value,region_value,country_value,state_value,city_value,attack_value,year_value,chart_year, chart_value, search,
                   subtabs2):
    fig = None
     
    if Tabs == "Map":
        print("Data Type of month value = " , str(type(month_value)))
        print("Data of month value = " , month_value)
        
        print("Data Type of Day value = " , str(type(date_value)))
        print("Data of Day value = " , date_value)
        
        print("Data Type of region value = " , str(type(region_value)))
        print("Data of region value = " , region_value)
        
        print("Data Type of country value = " , str(type(country_value)))
        print("Data of country value = " , country_value)
        
        print("Data Type of state value = " , str(type(state_value)))
        print("Data of state value = " , state_value)
        
        print("Data Type of city value = " , str(type(city_value)))
        print("Data of city value = " , city_value)
        
        print("Data Type of Attack value = " , str(type(attack_value)))
        print("Data of Attack value = " , attack_value)
        
        print("Data Type of year value = " , str(type(year_value)))
        print("Data of year value = " , year_value)
        # year_filter
        year_range = range(year_value[0], year_value[1]+1)
        new_data = data[data["iyear"].isin(year_range)]
        
        # month_filter
        if month_value==[] or month_value is None:
            pass
        else:
            if date_value==[] or date_value is None:
                new_data = new_data[new_data["imonth"].isin(month_value)]
            else:
                new_data = new_data[new_data["imonth"].isin(month_value)
                                & (new_data["iday"].isin(date_value))]
        # region, country, state, city filter
        if region_value==[] or region_value is None:
            pass
        else:
            if country_value==[] or country_value is None :
                new_data = new_data[new_data["region_txt"].isin(region_value)]
            else:
                if state_value == [] or state_value is None:
                    new_data = new_data[(new_data["region_txt"].isin(region_value))&
                                    (new_data["country_txt"].isin(country_value))]
                else:
                    if city_value == [] or city_value is None:
                        new_data = new_data[(new_data["region_txt"].isin(region_value))&
                        (new_data["country_txt"].isin(country_value)) &
                        (new_data["provstate"].isin(state_value))]
                    else:
                        new_data = new_data[(new_data["region_txt"].isin(region_value))&
                        (new_data["country_txt"].isin(country_value)) &
                        (new_data["provstate"].isin(state_value))&
                        (new_data["city"].isin(city_value))]
                        
        if attack_value == [] or attack_value is None:
            pass
        else:
            new_data = new_data[new_data["attacktype1_txt"].isin(attack_value)] 
        mapFigure = go.Figure()
        if new_data.shape[0]:
            pass
        else: 
            new_data = pd.DataFrame(columns = ['iyear', 'imonth', 'iday', 'country_txt', 'region_txt', 'provstate',
               'city', 'latitude', 'longitude', 'attacktype1_txt', 'nkill'])
            
            new_data.loc[0] = [0, 0 ,0, None, None, None, None, None, None, None, None]
            
        
        mapFigure = px.scatter_mapbox(new_data,
          lat="latitude", 
          lon="longitude",
          color="attacktype1_txt",
          hover_name="city", 
          hover_data=["region_txt", "country_txt", "provstate","city", "attacktype1_txt","nkill","iyear","imonth", "iday"],
          zoom=1
          )                       
        mapFigure.update_layout(mapbox_style="open-street-map",
          autosize=True,
          margin=dict(l=0, r=0, t=25, b=20),
          )
          
        fig = mapFigure
    elif Tabs=="Chart":
        fig = None
        
        
        year_range_c = range(chart_year[0], chart_year[1]+1)
        chart_data = data[data["iyear"].isin(year_range_c)]
        
        
        if subtabs2 == "WorldChart":
            pass
        elif subtabs2 == "IndiaChart":
            chart_data = chart_data[(chart_data["region_txt"]=="South Asia") &(chart_data["country_txt"]=="India")]
        if chart_value is not None and chart_data.shape[0]:
            if search is not None:
                chart_data = chart_data.groupby("iyear")[chart_value].value_counts().reset_index(name = "count")
                chart_data  = chart_data[chart_data[chart_value].str.contains(search, case=False)]
            else:
                chart_data = chart_data.groupby("iyear")[chart_value].value_counts().reset_index(name="count")
        
        
        if chart_data.shape[0]:
            pass
        else: 
            chart_data = pd.DataFrame(columns = ['iyear', 'count', chart_value])
            
            chart_data.loc[0] = [0, 0,"No data"]
        chartFigure = px.area(chart_data, x="iyear", y ="count", color = chart_value)
        fig = chartFigure
    return dcc.Graph(figure = fig)
@app.callback(
  dash.dependencies.Output("date", "options"),
  [dash.dependencies.Input("month", "value")])
def update_date(month):
    option = []
    if month:
        option= [{"label":m, "value":m} for m in date_list]
    return option
@app.callback([dash.dependencies.Output("region-dropdown", "value"),
               dash.dependencies.Output("region-dropdown", "disabled"),
               dash.dependencies.Output("country-dropdown", "value"),
               dash.dependencies.Output("country-dropdown", "disabled")],
              [dash.dependencies.Input("subtabs", "value")])
def update_r(tab):
    region = None
    disabled_r = False
    country = None
    disabled_c = False
    if tab == "WorldMap":
        pass
    elif tab=="IndiaMap":
        region = ["South Asia"]
        disabled_r = True
        country = ["India"]
        disabled_c = True
    return region, disabled_r, country, disabled_c
@app.callback(
    dash.dependencies.Output('country-dropdown', 'options'),
    [dash.dependencies.Input('region-dropdown', 'value')])
def set_country_options(region_value):
    option = []
    if region_value is  None:
        raise PreventUpdate
    else:
        for var in region_value:
            if var in country_list.keys():
                option.extend(country_list[var])
    return [{'label':m , 'value':m} for m in option]
@app.callback(
    dash.dependencies.Output('state-dropdown', 'options'),
    [dash.dependencies.Input('country-dropdown', 'value')])
def set_state_options(country_value):
  # Making the state Dropdown data
    option = []
    if country_value is None :
        raise PreventUpdate
    else:
        for var in country_value:
            if var in state_list.keys():
                option.extend(state_list[var])
    return [{'label':m , 'value':m} for m in option]
@app.callback(
    dash.dependencies.Output('city-dropdown', 'options'),
    [dash.dependencies.Input('state-dropdown', 'value')])
def set_city_options(state_value):
    option = []
    if state_value is None:
        raise PreventUpdate
    else:
        for var in state_value:
            if var in city_list.keys():
                option.extend(city_list[var])
    return [{'label':m , 'value':m} for m in option]

def main():
  load_data()
  
  open_browser()
  
  global app
  app.layout = create_app8_ui()
  app.title = "Terrorism Analysis with Insights" 
  app.run_server()

  print("Thanks for Using my app!!!")
  data = None
  app = None

if __name__ == '__main__':
    main()
