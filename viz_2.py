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
filename='D:\jazz_docs\gapminder\data3.txt'
dataset=pd.read_csv(filename)
#base_dict={'Asia':'Core', 'Americas':'Rot','Europe':'New','Africa':'drop','Oceania':'drop'}
#dataset['base']=dataset['base'].apply(lambda x: base_dict[x])
#dataset=dataset.loc[(dataset['base']!='drop')]
#dataset=dataset.reset_index(drop=True)
# %%
#dataset=pd.DataFrame()
#col=['base','seg','week','pop','rev','rech_amt']
#
#weeks=range(1,15)
#bases=['Core','Rot','New']
#segs=['bundle takers',
#'vas',
#'high_data',
#'high_voice',
#'low_data',
#'low_voice',
#'qos_good',
#'qos_bad'
#]
#
#dataset=pd.DataFrame(columns=col)
#for b in bases:
#    for s in segs:
#        for w in weeks:
#            dataset=dataset.append({'base':b,'seg':s,'week':w,'pop':int(np.random.uniform(1000000,10000000,1)),'rev':float(np.random.uniform(0,100,1)),'rech_amt':float(np.random.uniform(0,2000,1))},ignore_index=True)
# %%
weeks_from_col = set(dataset['week'])
weeks_ints = sorted(list(weeks_from_col))
weeks = [str(week) for week in weeks_ints]
# %%make list of continents
bases = []
for base in dataset['base']:
    if base not in bases: 
        bases.append(base)
# %%make grid
df = pd.DataFrame()
for week in weeks:
    for base in bases:
        dataset_by_week = dataset[dataset['week'] == int(week)]
        dataset_by_week_and_base = dataset_by_week[dataset_by_week['base'] == base]
        for col_name in dataset_by_week_and_base:
            # each column name is unique
            temp = '{week}+{base}+{header}_grid'.format(
                week=week, base=base, header=col_name
            )
            #if dataset_by_year_and_cont[col_name].size != 0:
            df = df.append({'value': list(dataset_by_week_and_base[col_name]), 'key': temp}, ignore_index=True)
# %%
figure = {
    'data': [],
    'layout': {},
    'frames': []
}
figure['layout']['xaxis'] = {'title': 'Recharge Amount', 'type': 'log', 'autorange': True} #was not set properly
figure['layout']['yaxis'] = {'title': 'Revenue', 'autorange': True} #was not set properly
figure['layout']['hovermode'] = 'closest'
figure['layout']['showlegend'] = True
figure['layout']['sliders'] = {
    'args': [
        'slider.value', {
            'duration': 400,
            'ease': 'cubic-in-out'
        }
    ],
    'initialValue': '12',
    'plotlycommand': 'animate',
    'values': weeks,
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
        'prefix': 'Week:',
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
    'Core': 'rgb(171, 99, 250)',
    'Rot': 'rgb(230, 99, 250)',
    #'Africa': 'rgb(99, 110, 250)',
    'New': 'rgb(25, 211, 243)',
    #'Oceania': 'rgb(9, 255, 255)' 
    #'Oceania': 'rgb(50, 170, 255)'
}
# %%
col_name_template = '{week}+{base}+{header}_grid'
week = 7
for base in bases:
    data_dict = {
        'x': df.loc[df['key']==col_name_template.format(
            week=week, base=base, header='rech_amt'
        ), 'value'].values[0],
        'y': df.loc[df['key']==col_name_template.format(
            week=week, base=base, header='rev'
        ), 'value'].values[0],
        'mode': 'markers',
        'text': df.loc[df['key']==col_name_template.format(
            week=week, base=base, header='seg'
        ), 'value'].values[0],
        'marker': {
            'sizemode': 'area',
            'sizeref': 200000,
            'size': df.loc[df['key']==col_name_template.format(
                week=week, base=base, header='pop'
            ), 'value'].values[0],
            'color': custom_colors[base]
        },
        'name': base
    }
    figure['data'].append(data_dict)
# %%
for week in weeks:
    frame = {'data': [], 'name': str(week)}
    for base in bases:
        data_dict = {
            'x': df.loc[df['key']==col_name_template.format(
                week=week, base=base, header='rech_amt'
            ), 'value'].values[0],
            'y': df.loc[df['key']==col_name_template.format(
                week=week, base=base, header='rev'
            ), 'value'].values[0],
            'mode': 'markers',
            'text': df.loc[df['key']==col_name_template.format(
                week=week, base=base, header='seg'
            ), 'value'].values[0],
            'marker': {
                'sizemode': 'area',
                'sizeref': 200000,
                'size': df.loc[df['key']==col_name_template.format(
                    week=week, base=base, header='pop'
                ), 'value'].values[0],
                'color': custom_colors[base]
            },
            'name': base
        }
        frame['data'].append(data_dict)

    figure['frames'].append(frame) #this block was indented and should not have been.
    slider_step = {'args': [
        [week],
        {'frame': {'duration': 300, 'redraw': False},
         'mode': 'immediate',
       'transition': {'duration': 300}}
     ],
     'label': week,
     'method': 'animate'}
    sliders_dict['steps'].append(slider_step)

# %%
figure['layout']['sliders'] = [sliders_dict]
iplot(figure, config={'scrollzoom': True})
