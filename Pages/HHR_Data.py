#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 25 04:53:56 2020

@author: xuncui
"""

import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output
from utils import create_connection
from app import app

database_path = r'R:\03 Prime_Folders\Aaron\Reconciliation_database'
#connection = create_connection('./DATA/Reconciliation_databse.sl3')
connection = create_connection(database_path+'/Reconciliation_databse.sl3')
TOU_raw = pd.read_sql_query("select * from TOU_Consumption",connection)

layout= html.Div([
        html.Br(),
        dcc.Dropdown(
                id = 'target_ICP',
                options = [
                        {'label':i,'value':i} for i in TOU_raw.ICP.unique()        
                        ],
                value = '0000008117TE7CB'
                        ),

        dcc.Graph(id = 'TOU_graph')
            ])


@app.callback(
        Output('TOU_graph','figure'),
        [Input("target_ICP","value")])

def update_figure_HHR_Data(target_ICP):
    if target_ICP is None:
        temp_filtered_df = TOU_raw[TOU_raw['ICP']=='0000008117TE7CB']
    else:
        temp_filtered_df = TOU_raw[TOU_raw['ICP']==str(target_ICP)]
        
    return {
            'data':[
                            go.Bar(
                                    x= list(temp_filtered_df['DATE'].unique()), y= list(temp_filtered_df[temp_filtered_df['TOU']=='OP']['CONSUMPTION']),
                                    #offset = 0,
                                    #width = 1,
                                    #name="OP",
                                    marker={                                            
                                            "color": "#97151c",
                                            "line": {
                                                    "color": "#97151c",
                                                    "width": 1,
                                                        }},
                                                    name = 'OP'),
                            go.Bar(
                                    x=list(temp_filtered_df['DATE'].unique()), y= list(temp_filtered_df[temp_filtered_df['TOU']=='PEAK']['CONSUMPTION']),
                                    #offset = -0.5,
                                    #width = 1,
                                    marker={                                            
                                            "color": "#D5FF11",
                                            "line": {
                                                    "color": "#D5FF11",
                                                    "width": 1,
                                                        }},
                                    name="PEAK"),
                             go.Bar(
                                    x=list(temp_filtered_df['DATE'].unique()), y= list(temp_filtered_df[temp_filtered_df['TOU']=='SHOULDER']['CONSUMPTION']),
                                    #offset = 0.5,
                                    #width = 1,
                                    marker={                                            
                                            "color": "#5095c5",
                                            "line": {
                                                    "color": "#5095c5",
                                                    "width": 1,
                                                        }},
                                    name="SHOULDER")],
                            "layout": go.Layout(
                                                autosize=True,
                                                bargap=0.3,
                                                #barmode="group"
                                                ),
            
            }

