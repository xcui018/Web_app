#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 25 05:34:11 2020

@author: xuncui
"""

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
import sqlite3
import numpy as np
from app import app
#from utils import create_connection,create_table
#import utils


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(e)
 
    return conn

#==================AV080===========================
connection = create_connection('./DATA/Reconciliation_databse.sl3')
AV080_raw = pd.read_sql_query("select * from AV080",connection)
AV080 = AV080_raw.groupby(by=['Revision_type','RECONPERIOD'],as_index=False)['TOTAL','ACTUALS'].sum()
M1_TOT = list(AV080[(AV080['Revision_type']=='M1')&(AV080['RECONPERIOD'].isin(list(AV080[AV080['Revision_type']=='M0']['RECONPERIOD'])))]['TOTAL'])
M1_TOT.extend([np.nan]*(len(AV080[AV080['Revision_type']=='M0'])-len(AV080[AV080['Revision_type']=='M1']['TOTAL'])))
M3_TOT = list(AV080[(AV080['Revision_type']=='M3')&(AV080['RECONPERIOD'].isin(list(AV080[AV080['Revision_type']=='M0']['RECONPERIOD'])))]['TOTAL'])
M3_TOT.extend([np.nan]*(len(AV080[AV080['Revision_type']=='M0'])-len(M3_TOT)))
M7_TOT = list(AV080[(AV080['Revision_type']=='M7')&(AV080['RECONPERIOD'].isin(list(AV080[AV080['Revision_type']=='M0']['RECONPERIOD'])))]['TOTAL'])
M7_TOT.extend([np.nan]*(len(AV080[AV080['Revision_type']=='M0'])-len(M7_TOT)))
M14_TOT = list(AV080[(AV080['Revision_type']=='M14')&(AV080['RECONPERIOD'].isin(list(AV080[AV080['Revision_type']=='M0']['RECONPERIOD'])))]['TOTAL'])
M14_TOT.extend([np.nan]*(len(AV080[AV080['Revision_type']=='M0'])-len(M14_TOT)))

AV080_df = pd.DataFrame({'RECONPERIOD':list(AV080[AV080['Revision_type']=='M0']['RECONPERIOD']),\
                        'M0_TOTAL':list(AV080[AV080['Revision_type']=='M0']['TOTAL']),\
                        'M1_TOTAL':M1_TOT,'M3_TOTAL':M3_TOT,'M7_TOTAL':M7_TOT,'M14_TOTAL':M14_TOT})
AV080_df['Variance_M0_percent'] = 100*((AV080_df['M0_TOTAL']-AV080_df.M0_TOTAL.shift(1))/AV080_df.M0_TOTAL.shift(1))
AV080_df['Variance_M1_percent'] = 100*((AV080_df['M1_TOTAL']-AV080_df.M1_TOTAL.shift(1))/AV080_df.M1_TOTAL.shift(1))
AV080_df['Variance_M3_percent'] = 100*((AV080_df['M3_TOTAL']-AV080_df.M3_TOTAL.shift(1))/AV080_df.M3_TOTAL.shift(1))
AV080_df['Variance_M7_percent'] = 100*((AV080_df['M7_TOTAL']-AV080_df.M7_TOTAL.shift(1))/AV080_df.M7_TOTAL.shift(1))
AV080_df['Variance_M14_percent'] = 100*((AV080_df['M14_TOTAL']-AV080_df.M14_TOTAL.shift(1))/AV080_df.M14_TOTAL.shift(1))


AV080_df['Variance_M1_CUR_PRE'] = 100*(AV080_df['M1_TOTAL']-AV080_df['M0_TOTAL'])/AV080_df['M0_TOTAL']
AV080_df['Variance_M3_CUR_PRE'] = 100*(AV080_df['M3_TOTAL']-AV080_df['M1_TOTAL'])/AV080_df['M1_TOTAL']
AV080_df['Variance_M7_CUR_PRE'] = 100*(AV080_df['M7_TOTAL']-AV080_df['M3_TOTAL'])/AV080_df['M3_TOTAL']
AV080_df['Variance_M14_CUR_PRE'] = 100*(AV080_df['M14_TOTAL']-AV080_df['M7_TOTAL'])/AV080_df['M7_TOTAL']
#========================AV080 END================

#========================AV110======================
AV110_raw = pd.read_sql_query("select * from AV110",connection)
AV110 =AV110_raw.groupby(by=['Revision_type','RECONPERIOD'],as_index=False)['DAYs'].sum()
M1_ICP = list(AV110[(AV110['Revision_type']=='M1')&(AV110['RECONPERIOD'].isin(list(AV110[AV110['Revision_type']=='M0']['RECONPERIOD'])))]['DAYs'])
M1_ICP.extend([np.nan]*(len(AV110[AV110['Revision_type']=='M0'])-len(M1_ICP)))
M3_ICP = list(AV110[(AV110['Revision_type']=='M3')&(AV110['RECONPERIOD'].isin(list(AV110[AV110['Revision_type']=='M0']['RECONPERIOD'])))]['DAYs'])
M3_ICP.extend([np.nan]*(len(AV110[AV110['Revision_type']=='M0'])-len(M3_ICP)))
M7_ICP = list(AV110[(AV110['Revision_type']=='M7')&(AV110['RECONPERIOD'].isin(list(AV110[AV110['Revision_type']=='M0']['RECONPERIOD'])))]['DAYs'])
M7_ICP.extend([np.nan]*(len(AV110[AV110['Revision_type']=='M0'])-len(M7_ICP)))
M14_ICP = list(AV110[(AV110['Revision_type']=='M14')&(AV110['RECONPERIOD'].isin(list(AV110[AV110['Revision_type']=='M0']['RECONPERIOD'])))]['DAYs'])
M14_ICP.extend([np.nan]*(len(AV110[AV110['Revision_type']=='M0'])-len(M14_ICP)))

AV110_df = pd.DataFrame({'RECONPERIOD':list(AV110[AV110['Revision_type']=='M0']['RECONPERIOD']),\
                        'M0_DAYs':list(AV110[AV110['Revision_type']=='M0']['DAYs']),\
                        'M1_DAYs':M1_ICP,'M3_DAYs':M3_ICP,'M7_DAYs':M7_ICP,'M14_DAYs':M14_ICP})
    
AV110_df['Variance_M0_percent'] = 100*((AV110_df['M0_DAYs']-AV110_df.M0_DAYs.shift(1))/AV110_df.M0_DAYs.shift(1))
AV110_df['Variance_M1_percent'] = 100*((AV110_df['M1_DAYs']-AV110_df.M1_DAYs.shift(1))/AV110_df.M1_DAYs.shift(1))
AV110_df['Variance_M3_percent'] = 100*((AV110_df['M3_DAYs']-AV110_df.M3_DAYs.shift(1))/AV110_df.M3_DAYs.shift(1))
AV110_df['Variance_M7_percent'] = 100*((AV110_df['M7_DAYs']-AV110_df.M7_DAYs.shift(1))/AV110_df.M7_DAYs.shift(1))
AV110_df['Variance_M14_percent'] = 100*((AV110_df['M14_DAYs']-AV110_df.M14_DAYs.shift(1))/AV110_df.M14_DAYs.shift(1))

AV110_df['Variance_M1_CUR_PRE'] = 100*(AV110_df['M1_DAYs']-AV110_df['M0_DAYs'])/AV110_df['M0_DAYs']
AV110_df['Variance_M3_CUR_PRE'] = 100*(AV110_df['M3_DAYs']-AV110_df['M1_DAYs'])/AV110_df['M1_DAYs']
AV110_df['Variance_M7_CUR_PRE'] = 100*(AV110_df['M7_DAYs']-AV110_df['M3_DAYs'])/AV110_df['M3_DAYs']
AV110_df['Variance_M14_CUR_PRE'] = 100*(AV110_df['M14_DAYs']-AV110_df['M7_DAYs'])/AV110_df['M7_DAYs']
#================AV110 END============



layout = html.Div([
        #html.H6('HIST NZX VOL'),
        html.Br(),
        dcc.Graph(
                id='hist_nzx_vol_graph',
                figure={
                        'data': [{
                                'x':list(AV080[AV080['Revision_type']=='M0']['RECONPERIOD']),
                                'y':list(AV080[AV080['Revision_type']=='M0']['TOTAL']),
                                'type': 'bar','name':'TOTAL_M0'
                                },
                                {'x':list(AV080[AV080['Revision_type']=='M0']['RECONPERIOD']),
                                 'y':M1_TOT,
                                 'type':'bar','name':'TOTAL_M1',"color": "#D5FF11"
                                },
                                 {'x':list(AV080[AV080['Revision_type']=='M0']['RECONPERIOD']),
                                  'y':M3_TOT,
                                  'type':'bar','name':'TOTAL_M3',"color": "#C5741D"},
                                  {'x':list(AV080[AV080['Revision_type']=='M0']['RECONPERIOD']),
                                   'y':M7_TOT,
                                   'type':'bar','name':'TOTAL_M7',"color": "#B44C3A"},
                                   {'x':list(AV080[AV080['Revision_type']=='M0']['RECONPERIOD']),
                                    'y':M14_TOT,
                                    'type':'bar','name':'TOTAL_M14',"color": "#EE2D0D"},
                                 ],
                        "layout": go.Layout(
                                
                                autosize=True,
                                title='HIST NZX VOL(kWh)',
                                xaxis=dict(
                                        title='RECONPERIOD',
                                        #ticklen=5,
                                        zeroline=False,
                                        #gridwidth=2,
                                        ),
                                yaxis=dict(
                                        title='kWh'),
                                bargap=0.2,
                                margin={'t': 40,'b':30},
                                barmode="group"),
                        },
                
                ),
    html.Br(),
    html.Div([
            html.Div([
                    dcc.Dropdown(id = 'Variance_PRE_period_dropdown',
                    options=[
                            {'label':'Variance_M0_percent','value':'Variance_M0_percent'},
                            {'label':'Variance_M1_percent','value':'Variance_M1_percent'},
                            {'label':'Variance_M3_percent','value':'Variance_M3_percent'},
                            {'label':'Variance_M7_percent','value':'Variance_M7_percent'},
                            {'label':'Variance_M14_percent','value':'Variance_M14_percent'},
                            ]),
                    dcc.Graph(id = 'Variance_PRE_period_Graph',)
                    ],className='six columns'),
            html.Div([
                    dcc.Dropdown(id = 'Variance_CUR_PRE_dropdown',
                    options=[
                            {'label':'Variance_M1','value':'Variance_M1_CUR_PRE'},
                            {'label':'Variance_M3','value':'Variance_M3_CUR_PRE'},
                            {'label':'Variance_M7','value':'Variance_M7_CUR_PRE'},
                            {'label':'Variance_M14','value':'Variance_M14_CUR_PRE'},
                            ]
                                 
                                 
                                 ),
                    
                    dcc.Graph(id = 'Variance_CUR_PRE_Graph',)
                    ],className='six columns')
            ],className="row "),
])

    
@app.callback(
        Output('Variance_PRE_period_Graph','figure'),
        [Input("Variance_PRE_period_dropdown","value")])

def update_figure(drop_down_ele):
    if drop_down_ele is None:
        temp_filtered_av080_df = list(AV080_df['Variance_M0_percent'])
        temp_filtered_av110_df = list(AV110_df['Variance_M0_percent'])
    else:
        temp_filtered_av080_df = list(AV080_df[str(drop_down_ele)])
        temp_filtered_av110_df = list(AV110_df[str(drop_down_ele)])
           
    return {
                    'data':[
                            {
                                    'x': list(AV080[AV080['Revision_type']=='M0']['RECONPERIOD']),
                                    'y': temp_filtered_av080_df,
                                    'type':'bar','name':'TOTAL_Var%',"color": "#F22604"
                            },
                            {
                                   'x': list(AV080[AV080['Revision_type']=='M0']['RECONPERIOD']),
                                   'y':temp_filtered_av110_df,
                                   'type':'bar','name':'ICP_Var%',"color": "#1334DB"
                            },                                  
                            ],
                    "layout": go.Layout(
                            autosize=True,
                            title='HIST Variance between CUR period VS PRE period (%)',
                            xaxis=dict(
                                    title='RECONPERIOD',
                            ),
                            yaxis=dict(
                                    title='%'),
                            bargap=0.2,
                            margin={'t': 40,'b':30},
                            barmode="group"),
                                    
                    }
                    
@app.callback(
        Output('Variance_CUR_PRE_Graph','figure'),
        [Input("Variance_CUR_PRE_dropdown","value")])

def update_figure1(drop_down_ele1):
    if drop_down_ele1 is None:
        temp_filtered_av080_df2 = list(AV080_df['Variance_M1_CUR_PRE'])
        temp_filtered_av110_df2 = list(AV110_df['Variance_M1_CUR_PRE'])
    else:
        temp_filtered_av080_df2 = list(AV080_df[str(drop_down_ele1)])
        temp_filtered_av110_df2 = list(AV110_df[str(drop_down_ele1)])
           
    return {
                    'data':[
                            {
                                    'x': list(AV080[AV080['Revision_type']=='M0']['RECONPERIOD']),
                                    'y': temp_filtered_av080_df2,
                                    'type':'bar','name':'TOTAL_Var%',"color": "#F22604"
                            },
                            {
                                   'x': list(AV080[AV080['Revision_type']=='M0']['RECONPERIOD']),
                                   'y':temp_filtered_av110_df2,
                                   'type':'bar','name':'ICP_Var%',"color": "#1334DB"
                            },                                  
                            ],
                    "layout": go.Layout(
                            autosize=True,
                            title='HIST Variance between CUR VS PRE (%)',
                            xaxis=dict(
                                    title='RECONPERIOD',
                            ),
                            yaxis=dict(
                                    title='%'),
                            bargap=0.2,
                            margin={'t': 40,'b':30},
                            barmode="group"),
                    }
#def create_layout():
#    return html.Div([
#            html.Br(),
#            html.H6(["Historical NZX Submission Vol"],className="subtitle padded"),
#        
#                    ])
