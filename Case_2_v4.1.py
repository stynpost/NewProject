#!/usr/bin/env python
# coding: utf-8

# In[3]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from datetime import datetime, date


# In[4]:


#Create a list of seasons
seasons = [2010, 2011, 2012,2013, 2014, 2015,2016, 2017, 2018,2019,2020,2021]

#Create DataFrame races_df
races_df = pd.DataFrame()

#Create DataFrame races_df1
races_df1 = pd.DataFrame()

#Read dataset F1 race results
for season in seasons:
   r = requests.get("http://ergast.com/api/f1/{}/results/.json?limit=450".format(season))
   data=r.json()
    
#Normalize F1 race results data and append this to DataFrame races_df
   races = pd.json_normalize(data['MRData']['RaceTable']['Races'])
   races_df = races_df.append(races)

#Read dataset F1 race qualifierresults
for season in seasons:
   r1 = requests.get("http://ergast.com/api/f1/{}/qualifying/.json?limit=450".format(season))
   data1=r1.json()
    
#Normalize F1 qualifier race results data and append this to DataFrame races_df1
   races1 = pd.json_normalize(data1['MRData']['RaceTable']['Races'])
   races_df1 = races_df1.append(races1)


# In[5]:


#Print header DataFrame races_df
races_df.head()


# In[6]:


#Print header DataFrame races_df1
races_df1.head()


# In[7]:


#Iterate race by race and append the results to the list results
results = []
for index, race in races_df.iterrows():
    race_data = pd.json_normalize(race['Results'])
    for index, row in race_data.iterrows():
        results.append((race['round'], 
                        race['raceName'],
                        race['season'],
                        race['date'],
                        race['Circuit.Location.country'], 
                        row['laps'], 
                        row['grid'],
                        row['position'],
                        row['Time.millis'],
                        row['status'],
                        row['Constructor.name'],
                       (row['Driver.givenName']+' '+ row['Driver.familyName']),
                        row['Driver.dateOfBirth'],
                        row['Driver.nationality']
                       )
                      )


# In[8]:


#Define column_names for DataFrame results_df
column_names = ['Race_Id',
                'Race_Name',
                'Season',
                'Race_Date',
                'Country',
                'Laps',
                'Grid',
                'Position',
                'Time_(ms)',
                'Status',
                'Team',
                'Driver_Name',
                'Driver_Date_Of_Birth',
                'Driver_Nationality',
               ]

#Create DataFrame results_df
results_df = pd.DataFrame(results, columns = column_names)


# In[9]:


#Print shape DataFrame results_df
results_df.shape


# In[10]:


#Iterate race by race and append the Qualifyingresults to the list results1
results1 = []
for index, race in races_df1.iterrows():
    race_data1 = pd.json_normalize(race['QualifyingResults'])
    for index, row in race_data1.iterrows():   
        results1.append((race['round'],
                        race['raceName'],
                        race['season'],
                        row['Q1'],
                        row['Q2'],
                        row['Constructor.name'],
                       (row['Driver.givenName']+' '+ row['Driver.familyName']),
                        row['Driver.dateOfBirth'],
                        row['Driver.nationality']
                       )
                      )


# In[11]:


#Define column_names for DataFrame results_df
column_names1 = [
                'Race_Id',
                'Race_Name',
                'Season',
                'Q1',
                'Q2',
                'Team',
                'Driver_Name',
                'Driver_Date_Of_Birth',
                'Driver_Nationality',
               ]

#Create DataFrame results_df
results_df1 = pd.DataFrame(results1, columns = column_names1)


# In[12]:


#Print shape DataFrame results_df1
results_df1.shape


# In[13]:


#Print header DataFrame results_df
results_df.head()


# In[14]:


#Print header DataFrame results_df1
results_df1.head()


# In[15]:


#Left join results_df with results_df1
results_df = results_df.merge(results_df1, on = ['Race_Id','Race_Name','Season', 'Team','Driver_Name','Driver_Date_Of_Birth','Driver_Nationality'], how = 'left')


# In[16]:


#Print header DataFrame results_df after left join
results_df.head()


# In[17]:


#Convert datatypes
convert_dict = {
    'Race_Id' : int,
    'Race_Name' : str,
    'Season' : int,
    'Country' : str,
    'Laps' : int,
    'Grid' : int,
    'Position' : int,
    'Status' : str,
    'Team' : str,
    'Driver_Name' : str,
    'Driver_Date_Of_Birth' : str,
    'Driver_Nationality' : str,
    'Q1': str,
    'Q2' : str,
}
results_df = results_df.astype(convert_dict)


# In[18]:


#Convert Q1 to datetime
results_df['Q1'] = pd.to_datetime(results_df['Q1'], format = '%M:%S.%f', errors = 'coerce')


# In[19]:


#Convert Q2 to datetime
results_df['Q2'] = pd.to_datetime(results_df['Q2'], format = '%M:%S.%f', errors = 'coerce')


# In[20]:


#Create Driver Race Age Column by returning age through date of birth and race date
results_df['Driver_Date_Of_Birth']= pd.to_datetime(results_df['Driver_Date_Of_Birth'], format='%Y-%m-%d')
results_df['Race_Date']= pd.to_datetime(results_df['Race_Date'], format='%Y-%m-%d')
results_df['Driver_Date_Of_Birth'] = results_df['Driver_Date_Of_Birth'].where(results_df['Driver_Date_Of_Birth'] < results_df['Race_Date'], results_df['Driver_Date_Of_Birth'])
results_df['Driver_Age_Race'] = (results_df['Race_Date'] - results_df['Driver_Date_Of_Birth']).astype('<m8[Y]')


# In[21]:


#Create Current Driver Age Column by returning age through date of birth and current date
results_df['Driver_Date_Of_Birth']= pd.to_datetime(results_df['Driver_Date_Of_Birth'], format='%Y-%m-%d')
now = pd.to_datetime('now')
results_df['Driver_Date_Of_Birth'] = results_df['Driver_Date_Of_Birth'].where(results_df['Driver_Date_Of_Birth'] < now, results_df['Driver_Date_Of_Birth'])
results_df['Driver_Age_Current'] = (now - results_df['Driver_Date_Of_Birth']).astype('<m8[Y]')


# In[22]:


#Print header DataFrame results_df after addition Driver_Age_Race and Driver_Age_Current
results_df.head()


# In[23]:


whos


# In[24]:


#Print shape DataFrame results_df after alterations
results_df.shape


# In[25]:


#Print datatypes DataFrame results_df after alterations
results_df.dtypes


# In[26]:


#Print info DataFrame results_df after alterations
results_df.info()


# In[27]:


#Look for null data DataFrame results_df after alterations
results_df.isnull().sum()


# In[28]:


#Look for unique values DataFrame results_df after alterations
results_df.nunique(axis=0)


# In[29]:


#Print describe DataFrame results_df after alterations
results_df.describe()


# In[30]:


#Create basic figure
fig = go.Figure()

#Loop through teams that won a race and plot in which country they won the grand prix
for team in ['Ferrari','McLaren','Red Bull', 'Mercedes','Williams','Lotus F1', 'AlphaTauri', 'Racing Point', 'Alpine F1 Team']:
    df = results_df[results_df['Team'] == team]
    df_1 = df[df['Position'] == 1] 
    fig.add_trace(go.Scattergeo(
        locations = df_1['Country'],
        locationmode = 'country names',
        name = team, 
        opacity = 0.7
    )
)
#Create dropdown elements
dropdown_buttons = [
    {'label' :'All Teams', 'method': 'update',
     'args': [{'visible': [True,True,True,True,True,True,True,True,True]},
             {'title':'Grand Prix Win Locations Per Team (2010-2021)'}]},
    {'label' :'Ferrari', 'method': 'update',
     'args': [{'visible': [True,False,False,False,False,False,False,False,False]},
             {'title':'Ferrari Grand Prix Win Locations (2010-2021)'}]},
    {'label' : 'McLaren', 'method': 'update',
     'args': [{'visible': [False,True,False,False,False,False,False,False,False]},
             {'title':'McLaren Grand Prix Win Locations (2010-2021)'}]},
    {'label' : 'Red Bull', 'method': 'update',
     'args': [{'visible': [False,False,True,False,False,False,False,False,False]},
             {'title':'Red Bull Grand Prix Win Locations (2010-2021)'}]},
    {'label' : 'Mercedes', 'method': 'update',
     'args': [{'visible': [False,False,False,True,False,False,False,False,False]},
             {'title':'Mercedes Grand Prix Win Locations (2010-2021)'}]},
    {'label' : 'Williams', 'method': 'update',
     'args': [{'visible': [False,False,False,False,True,False,False,False,False]},
             {'title':'Williams Grand Prix Win Locations (2010-2021)'}]},
    {'label' : 'Lotus F1', 'method': 'update',
     'args': [{'visible': [False,False,False,False,False,True,False,False,False]},
             {'title':'Lotus F1 Grand Prix Win Locations (2010-2021)'}]},
    {'label' : 'AlphaTauri', 'method': 'update',
     'args': [{'visible': [False,False,False,False,False,False,True,False,False]},
             {'title':'AlphaTauri Grand Prix Win Locations (2010-2021)'}]},
    {'label' : 'Racing Point', 'method': 'update',
     'args': [{'visible': [False,False,False,False,False,False,False,True,False]},
             {'title':'Racing Point Grand Prix Win Locations (2010-2021)'}]},
    {'label' : 'Alpine F1 Team', 'method': 'update',
     'args': [{'visible': [False,False,False,False,False,False,False,False,True]},
             {'tile':'Alpine F1 Team Grand Prix Win Locations (2010-2021)'}]}
    ]

# Update the figure to add dropdown buttons and show
fig.update_layout({
    'updatemenus':[{
        'type': 'dropdown',
        'x' : 1.2,
        'y' : 0.4,
        'showactive': True,
        'active' : 0,
        'buttons': dropdown_buttons
    }],
    'title': 
    {'text': 'Grand Prix Win Locations Per Team (2010-2021)',
      'x': 0.45, 
      'y': 0.9}    
    
})
# Show the plot
fig.show()


# In[31]:


df_slider = results_df[results_df['Grid'] == 1]
df_slider1 = results_df[results_df['Position'] == 1]




# Create the basic figure
fig = make_subplots(rows=2, cols=1, shared_xaxes=True)
 




# Loop through the states
for season in seasons:
    # Subset the DataFrame
    df = df_slider[df_slider.Season == season]

# Add a trace for each season
    fig.add_trace(go.Histogram(x=df["Driver_Name"], name=season),1,1)

for season in seasons:
    # Subset the DataFrame
    df = df_slider1[df_slider1.Season == season]

# Add a trace for each season
    fig.add_trace(go.Histogram(x=df["Driver_Name"], name=season ),2,1)




for i in [0,1, 2, 3 , 4, 5, 6, 7, 8, 9, 10 ,11,12,13,14,15,16,17,18,19,20,21,22,23]:
    fig.data[i].visible = False





# Create the slider elements
sliders = [{'steps':[
{'method': 'update', 'label': '2010', 'args': [{'visible': [True, False, False, False, False, False, False, False, False, False, False, False]}]},
{'method': 'update', 'label': '2011', 'args': [{'visible': [False, True, False, False, False, False, False, False, False, False, False, False]}]},
{'method': 'update', 'label': '2012', 'args': [{'visible': [False, False, True, False, False, False, False, False, False, False, False, False]}]},
{'method': 'update', 'label': '2013', 'args': [{'visible': [False, False, False, True, False, False, False, False, False, False, False, False]}]},
{'method': 'update', 'label': '2014', 'args': [{'visible': [False, False, False, False, True, False, False, False, False, False, False, False]}]},
{'method': 'update', 'label': '2015', 'args': [{'visible': [False, False, False, False, False, True, False, False, False, False, False, False]}]},
{'method': 'update', 'label': '2016', 'args': [{'visible': [False, False, False, False, False, False, True, False, False, False, False, False]}]},
{'method': 'update', 'label': '2017', 'args': [{'visible': [False, False, False, False, False, False, False, True, False, False, False, False]}]},
{'method': 'update', 'label': '2018', 'args': [{'visible': [False, False, False, False, False, False, False, False, True, False, False, False]}]},
{'method': 'update', 'label': '2019', 'args': [{'visible': [False, False, False, False, False, False, False, False, False, True, False, False]}]},
{'method': 'update', 'label': '2020', 'args': [{'visible': [False, False, False, False, False, False, False, False, False, False, True, False]}]},
{'method': 'update', 'label': '2021', 'args': [{'visible': [False, False, False, False, False, False, False, False, False, False, False, True]}]}]}]




fig.update_yaxes(title_text="Grid", row=1, col=1)
fig.update_yaxes(title_text="Wins", row=2, col=1)

fig.update_xaxes(title_text="Driver", row=2, col=1)

fig.update_layout(showlegend=False)

# Update the figure to add sliders and show
fig.update_layout({'sliders': sliders}, title='Grid Positions And Wins Per Driver (2010-2021)')
# Show the plot
fig.show()


# In[32]:


df_slider = results_df[results_df['Position'] == 1]

# Create the basic figure
fig = go.Figure()

# Loop through the states
for season in seasons:
    # Subset the DataFrame
    df = df_slider[df_slider.Season == season]
    # Add a trace for each season
    fig.add_trace(go.Histogram(x=df["Team"], name=season))

for i in [1, 2, 3 , 4, 5, 6, 7, 8, 9, 10 ,11]:
   fig.data[i].visible = False

# Create the slider elements
sliders = [{'steps':[
{'method': 'update', 'label': '2010', 'args': [{'visible': [True, False, False, False, False, False, False, False, False, False, False, False]}]},
{'method': 'update', 'label': '2011', 'args': [{'visible': [False, True, False, False, False, False, False, False, False, False, False, False]}]},
{'method': 'update', 'label': '2012', 'args': [{'visible': [False, False, True, False, False, False, False, False, False, False, False, False]}]},
{'method': 'update', 'label': '2013', 'args': [{'visible': [False, False, False, True, False, False, False, False, False, False, False, False]}]},
{'method': 'update', 'label': '2014', 'args': [{'visible': [False, False, False, False, True, False, False, False, False, False, False, False]}]},
{'method': 'update', 'label': '2015', 'args': [{'visible': [False, False, False, False, False, True, False, False, False, False, False, False]}]},
{'method': 'update', 'label': '2016', 'args': [{'visible': [False, False, False, False, False, False, True, False, False, False, False, False]}]},
{'method': 'update', 'label': '2017', 'args': [{'visible': [False, False, False, False, False, False, False, True, False, False, False, False]}]},
{'method': 'update', 'label': '2018', 'args': [{'visible': [False, False, False, False, False, False, False, False, True, False, False, False]}]},
{'method': 'update', 'label': '2019', 'args': [{'visible': [False, False, False, False, False, False, False, False, False, True, False, False]}]},
{'method': 'update', 'label': '2020', 'args': [{'visible': [False, False, False, False, False, False, False, False, False, False, True, False]}]},
{'method': 'update', 'label': '2021', 'args': [{'visible': [False, False, False, False, False, False, False, False, False, False, False, True]}]},
{'method': 'update', 'label': 'Altijd', 'args': [{'visible': [True, True, True, True, True, True, True, True, True, True, True, True]}]}]}]

# Update the figure to add sliders and show
fig.update_layout({'sliders': sliders}, xaxis_title_text='Teams', yaxis_title_text='Wins', title='Grand Prix Wins Per Team (2010-2021)',
        )

# Show the plot
fig.show()


# In[33]:


#Filter Unique Driver Names
results_drivers = results_df['Driver_Name'].unique()

#Create new lists driver_means
drivers_means = []

#Filter Driver_Names and Positions
results_position = results_df[['Driver_Name','Position']]

#Calculate the mean per driver
for driver in results_drivers:
    mean = results_position[results_position['Driver_Name'] == driver].mean()['Position']
    drivers_means.append((driver,mean))

#Create DataFrame driver_means_df
driver_means_df = pd.DataFrame(drivers_means, columns = ['Driver_Name', 'Mean Position'])

#Sort DataFrame by mean position
driver_means_df = driver_means_df.sort_values(by=['Mean Position'])

#Create the plot
fig = go.Figure(go.Bar(x = driver_means_df['Driver_Name'], y = driver_means_df['Mean Position']))

#Update the layout
fig.update_layout( xaxis_title_text='Driver', yaxis_title_text='Mean Position', title='Average Position Per Driver (2010-2021)')

#Show the plot
fig.show()



# In[35]:


df = results_df[results_df['Position'] == 1]
df1 = results_df[results_df['Grid'] == 1]
fig = go.Figure()
fig.add_trace(go.Box(y=df['Driver_Age_Race'], name='Age by win'))
fig.add_trace(go.Box(y=df1['Driver_Age_Race'], name='Age by poleposition'))
fig.update_layout(yaxis_title_text='Age', title='Age of drivers by wins and polepositions')
fig.show()


# In[ ]:




