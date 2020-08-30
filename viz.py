# -*- coding: utf-8 -*-
"""
Created on Sat Nov 17 11:08:43 2018

@author: harres.tariq
"""
import pandas as pd
import numpy as np
from __future__ import division
import plotly.plotly as py
from plotly.offline import download_plotlyjs, init_notebook_mode, iplot
from plotly.graph_objs import *
init_notebook_mode()
from plotly.grid_objs import Grid, Column
from plotly.tools import FigureFactory as FF 
# %%
#url=url = 'https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv'
filename='D:\jazz_docs\gapminder\data'
dataset=pd.read_csv(filename)
#dataset.to_csv(filename,index=False)
# %%
years_from_col = set(dataset['year'])
years_ints = sorted(list(years_from_col))
years = [str(year) for year in years_ints]
# %%make list of continents
continents = []
for continent in dataset['continent']:
    if continent not in continents: 
        continents.append(continent)
# %%make grid
df = pd.DataFrame()
for year in years:
    for continent in continents:
        dataset_by_year = dataset[dataset['year'] == int(year)]
        dataset_by_year_and_cont = dataset_by_year[dataset_by_year['continent'] == continent]
        for col_name in dataset_by_year_and_cont:
            # each column name is unique
            temp = '{year}+{continent}+{header}_grid'.format(
                year=year, continent=continent, header=col_name
            )
            #if dataset_by_year_and_cont[col_name].size != 0:
            df = df.append({'value': list(dataset_by_year_and_cont[col_name]), 'key': temp}, ignore_index=True)
figure = {
    'data': [],
    'layout': {},
    'frames': []
}
figure['layout']['xaxis'] = {'title': 'GDP per Capita', 'type': 'log', 'autorange': True} #was not set properly
figure['layout']['yaxis'] = {'title': 'Life Expectancy', 'autorange': True} #was not set properly
figure['layout']['hovermode'] = 'closest'
figure['layout']['showlegend'] = True
figure['layout']['sliders'] = {
    'args': [
        'slider.value', {
            'duration': 400,
            'ease': 'cubic-in-out'
        }
    ],
    'initialValue': '2007',
    'plotlycommand': 'animate',
    'values': years,
    'visible': True
}
    
figure['layout']['updatemenus'] = [
    {
        'buttons': [
            {
                'args': [None, {'frame': {'duration': 1000, 'redraw': False},
                         'fromcurrent': True, 'transition': {'duration': 300, 'easing': 'quadratic-in-out'}}],
                'label': 'Play',
                'method': 'animate'
            },
            {
                'args': [[None], {'frame': {'duration': 0, 'redraw': False}, 'mode': 'immediate',
                'transition': {'duration': 0}}],
                'label': 'Pause',
                'method': 'animate'
            }
        ],
        'direction': 'left',
        'pad': {'r': 10, 't': 87},
        'showactive': False,
        'type': 'buttons',
        'x': 0.1,
        'xanchor': 'right',
        'y': 0,
        'yanchor': 'top'
    }
]

sliders_dict = {
    'active': 0,
    'yanchor': 'top',
    'xanchor': 'left',
    'currentvalue': {
        'font': {'size': 20},
        'prefix': 'Year:',
        'visible': True,
        'xanchor': 'right'
    },
    'transition': {'duration': 300, 'easing': 'cubic-in-out'},
    'pad': {'b': 10, 't': 50},
    'len': 0.9,
    'x': 0.1,
    'y': 0,
    'steps': []
}
    
custom_colors = {
    'Asia': 'rgb(171, 99, 250)',
    'Europe': 'rgb(230, 99, 250)',
    'Africa': 'rgb(99, 110, 250)',
    'Americas': 'rgb(25, 211, 243)',
    #'Oceania': 'rgb(9, 255, 255)' 
    'Oceania': 'rgb(50, 170, 255)'
}
# %%
col_name_template = '{year}+{continent}+{header}_grid'
year = 2007
for continent in continents:
    data_dict = {
        'x': df.loc[df['key']==col_name_template.format(
            year=year, continent=continent, header='gdpPercap'
        ), 'value'].values[0],
        'y': df.loc[df['key']==col_name_template.format(
            year=year, continent=continent, header='lifeExp'
        ), 'value'].values[0],
        'mode': 'markers',
        'text': df.loc[df['key']==col_name_template.format(
            year=year, continent=continent, header='country'
        ), 'value'].values[0],
        'marker': {
            'sizemode': 'area',
            'sizeref': 200000,
            'size': df.loc[df['key']==col_name_template.format(
                year=year, continent=continent, header='pop'
            ), 'value'].values[0],
            'color': custom_colors[continent]
        },
        'name': continent
    }
    figure['data'].append(data_dict)

for year in years:
    frame = {'data': [], 'name': str(year)}
    for continent in continents:
        data_dict = {
            'x': df.loc[df['key']==col_name_template.format(
                year=year, continent=continent, header='gdpPercap'
            ), 'value'].values[0],
            'y': df.loc[df['key']==col_name_template.format(
                year=year, continent=continent, header='lifeExp'
            ), 'value'].values[0],
            'mode': 'markers',
            'text': df.loc[df['key']==col_name_template.format(
                year=year, continent=continent, header='country'
            ), 'value'].values[0],
            'marker': {
                'sizemode': 'area',
                'sizeref': 200000,
                'size': df.loc[df['key']==col_name_template.format(
                    year=year, continent=continent, header='pop'
                ), 'value'].values[0],
                'color': custom_colors[continent]
            },
            'name': continent
        }
        frame['data'].append(data_dict)

    figure['frames'].append(frame) #this block was indented and should not have been.
    slider_step = {'args': [
        [year],
        {'frame': {'duration': 300, 'redraw': False},
         'mode': 'immediate',
       'transition': {'duration': 300}}
     ],
     'label': year,
     'method': 'animate'}
    sliders_dict['steps'].append(slider_step)


figure['layout']['sliders'] = [sliders_dict]
iplot(figure, config={'scrollzoom': True})
