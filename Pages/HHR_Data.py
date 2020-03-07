#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 25 04:53:56 2020

@author: xuncui
"""

import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from datetime import datetime
import plotly.graph_objs as go
from dash.dependencies import Input, Output
from utils import create_connection
from app import app

database_path = r'R:\03 Prime_Folders\Aaron\Reconciliation_database'
#connection = create_connection('./DATA/Reconciliation_databse.sl3')
connection = create_connection(database_path+'/Reconciliation_databse.sl3')

#========================TOU================================
TOU_raw = pd.read_sql_query("select * from TOU_Consumption",connection)
TOU_raw['REGISTER_NUMBER'] = TOU_raw['REGISTER_NUMBER'].astype(float).astype(int).astype(str)
tou_group = TOU_raw.groupby(by=['ICP','METER_SERIAL','REGISTER_NUMBER','REGISTER_CONTENT_CODE','DATE'],as_index=False)['CONSUMPTION'].sum()

tou_read_raw2 = pd.read_sql_query("select * from METER_READs where ICP in "+str(tuple(list(tou_group['ICP'].unique()))),connection)
tou_read_raw2['DATE_time'] = pd.to_datetime(tou_read_raw2.DATE,format="%Y%m%d")
tou_read_raw2.METER_SERIAL = tou_read_raw2.METER_SERIAL.str.strip()
tou_read_raw2.sort_values(by = ['ICP','METER_SERIAL','CHANNEL_NUMBER','DATE_time'],ascending=True,inplace = True)
tou_read_raw2.drop_duplicates(subset = ['ICP','METER_SERIAL','CHANNEL_NUMBER','DATE'],keep = 'last',inplace = True)
meter_validation = pd.read_sql_query("select * from METER_SERIAL_VALIDATION_TABLE",connection)
tou_read_raw3 = pd.merge(tou_read_raw2,meter_validation,how = 'left',left_on=['ICP','METER_SERIAL','CHANNEL_NUMBER'],\
                        right_on = ['ICP','FAULT_METER_SERIAL','FAULT_CHANNEL_NUMBER'])
tou_read_raw = tou_read_raw3[tou_read_raw3['DEL_FLAG']!='Y'].copy()
tou_read_raw.reset_index(drop = True,inplace = True)
ym = []
for i,row in enumerate(tou_read_raw.itertuples()):
    temp = row.DATE_time.strftime("%Y-%m")
    ym.append(temp)
tou_read_raw['Y_M']=ym
tou_read_raw['KEY'] = tou_read_raw['ICP']+tou_read_raw['METER_SERIAL']+tou_read_raw['CHANNEL_NUMBER']

consumption = list(tou_read_raw.READ.diff())
tou_read_raw['CONS'] = consumption
tou_read_raw['CONS'].fillna(0,inplace = True)
tou_read_raw['shift_DATE_time'] = tou_read_raw.DATE_time.shift(1)
tou_read_raw['shift_KEY'] = tou_read_raw.KEY.shift(1)
del_flag = []
for i,row in enumerate(tou_read_raw.itertuples()):
    if str(row.KEY)!=str(row.shift_KEY):
        del_flag.append("Y")
    else:
        del_flag.append("N")
tou_read_raw['DEL'] = del_flag
tou_read = tou_read_raw[tou_read_raw['DEL']=='N'].copy()
tou_read.reset_index(drop = True,inplace = True)

tou_read_group = tou_read.groupby(by=['ICP','METER_SERIAL','CHANNEL_NUMBER','Y_M'],as_index=False)['CONS'].sum()
tou_merge = pd.merge(tou_read_group,tou_group,how='inner',left_on = ['ICP','METER_SERIAL','CHANNEL_NUMBER','Y_M'],\
                    right_on = ['ICP','METER_SERIAL','REGISTER_NUMBER','DATE'])
date = []
for i,row in enumerate(tou_merge.itertuples()):
    temp = datetime.strptime(row.DATE,"%Y-%m").strftime("%Y-%m-%d")
    date.append(temp)
tou_merge['DATE'] = date
#==========================TOU END========================

#=====================METRIX HHR===============================
Metrix_hhr_raw = pd.read_sql_query("select * from METRIX_HHR",connection)
Metrix_hhr = Metrix_hhr_raw.groupby(by = ['ICP','YM'],as_index=False)['QUANTITY'].sum()
#====================END METRIX=================================

layout= html.Div([
        html.Br(),
        dcc.Dropdown(
                id = 'target_ICP',
                options = [
                        {'label':i,'value':i} for i in TOU_raw.ICP.unique()        
                        ],
                value = '0000008117TE7CB'
                        ),

        dcc.Graph(id = 'TOU_graph'),
        html.Br(),
        dcc.Dropdown(
                id = 'tou_ICP',
                options = [
                        {'label':i,'value':i} for i in tou_merge.ICP.unique()
                        ],
                value = '0000008117TE7CB'
                ),
        dcc.Graph(id = 'TOU_graph_2'),
        html.Br(),
        dcc.Graph(id = 'METRIX_HHR_graph',
                  figure = {
                          'data':[{
                                  'x':list(Metrix_hhr['YM']),
                                  'y':list(Metrix_hhr['QUANTITY']),
                                  'type': 'bar','name':'Consumption(kWh)'
                                  }],
                            "layout": go.Layout(
                                    autosize=True,
                                    title='METRIX_HHR_consumption(kWh)',
                                    xaxis=dict(
                                            title='PERIOD'),
                                    yaxis = dict(
                                            title = 'kWh'
                                            ),
                                    bargap=0.2,
                                    margin={'t': 40,'b':30},
                                    )
                          }
                  )
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

@app.callback(
        Output('TOU_graph_2','figure'),
        [Input("tou_ICP","value")])

def update_figure_HHR_Data2(tou_ICP):
    if tou_ICP is None:
        temp_filtered_df = tou_merge[tou_merge['ICP']=='0000008117TE7CB']
    else:
        temp_filtered_df = tou_merge[tou_merge['ICP']==str(tou_ICP)]
        
    return {
            'data':[
                            go.Bar(
                                    x= list(temp_filtered_df['DATE'].unique()), y= list(temp_filtered_df['CONS']),
                                    #offset = 0,
                                    #width = 1,
                                    #name="OP",
                                    marker={                                            
                                            "color": "#97151c",
                                            "line": {
                                                    "color": "#97151c",
                                                    "width": 1,
                                                        }},
                                                    name = 'TOTAL'),
                            go.Bar(
                                    x=list(temp_filtered_df['DATE'].unique()), y= list(temp_filtered_df['CONSUMPTION']),
                                    #offset = -0.5,
                                    #width = 1,
                                    marker={                                            
                                            "color": "#D5FF11",
                                            "line": {
                                                    "color": "#D5FF11",
                                                    "width": 1,
                                                        }},
                                    name="TOU")],       
                            "layout": go.Layout(
                                                autosize=True,
                                                bargap=0.3,
                                                #barmode="group"
                                                ),
            
            }
