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
from datetime import datetime
import numpy as np
from app import app
import sys
import YM_subtract
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
database_path = r'R:\03 Prime_Folders\Aaron\Reconciliation_database'
connection = create_connection(database_path+'/Reconciliation_databse.sl3')
#connection = create_connection('./DATA/Reconciliation_databse.sl3')
AV080_raw = pd.read_sql_query("select * from AV080",connection)
AV080 = AV080_raw.groupby(by=['Revision_type','RECONPERIOD'],as_index=False)['TOTAL','ACTUALS'].sum()
AV080['Ratio'] = 100*(AV080['ACTUALS']/AV080['TOTAL'])

M1_ratio = list(AV080[(AV080['Revision_type']=='M1')&(AV080['RECONPERIOD'].isin(list(AV080[AV080['Revision_type']=='M0']['RECONPERIOD'])))]['Ratio'])
M1_ratio.extend([np.nan]*(len(AV080[AV080['Revision_type']=='M0'])-len(M1_ratio)))
M3_ratio = list(AV080[(AV080['Revision_type']=='M3')&(AV080['RECONPERIOD'].isin(list(AV080[AV080['Revision_type']=='M0']['RECONPERIOD'])))]['Ratio'])
M3_ratio.extend([np.nan]*(len(AV080[AV080['Revision_type']=='M0'])-len(M3_ratio)))
M7_ratio = list(AV080[(AV080['Revision_type']=='M7')&(AV080['RECONPERIOD'].isin(list(AV080[AV080['Revision_type']=='M0']['RECONPERIOD'])))]['Ratio'])
M7_ratio.extend([np.nan]*(len(AV080[AV080['Revision_type']=='M0'])-len(M7_ratio)))
M14_ratio = list(AV080[(AV080['Revision_type']=='M14')&(AV080['RECONPERIOD'].isin(list(AV080[AV080['Revision_type']=='M0']['RECONPERIOD'])))]['Ratio'])
M14_ratio.extend([np.nan]*(len(AV080[AV080['Revision_type']=='M0'])-len(M14_ratio)))


M1_TOT = list(AV080[(AV080['Revision_type']=='M1')&(AV080['RECONPERIOD'].isin(list(AV080[AV080['Revision_type']=='M0']['RECONPERIOD'])))]['TOTAL'])
M1_TOT.extend([np.nan]*(len(AV080[AV080['Revision_type']=='M0'])-len(M1_TOT)))
M3_TOT = list(AV080[(AV080['Revision_type']=='M3')&(AV080['RECONPERIOD'].isin(list(AV080[AV080['Revision_type']=='M0']['RECONPERIOD'])))]['TOTAL'])
M3_TOT.extend([np.nan]*(len(AV080[AV080['Revision_type']=='M0'])-len(M3_TOT)))
M7_TOT = list(AV080[(AV080['Revision_type']=='M7')&(AV080['RECONPERIOD'].isin(list(AV080[AV080['Revision_type']=='M0']['RECONPERIOD'])))]['TOTAL'])
M7_TOT.extend([np.nan]*(len(AV080[AV080['Revision_type']=='M0'])-len(M7_TOT)))
M14_TOT = list(AV080[(AV080['Revision_type']=='M14')&(AV080['RECONPERIOD'].isin(list(AV080[AV080['Revision_type']=='M0']['RECONPERIOD'])))]['TOTAL'])
M14_TOT.extend([np.nan]*(len(AV080[AV080['Revision_type']=='M0'])-len(M14_TOT)))

AV080_df = pd.DataFrame({'RECONPERIOD':list(AV080[AV080['Revision_type']=='M0']['RECONPERIOD']),\
                        'M0_TOTAL':list(AV080[AV080['Revision_type']=='M0']['TOTAL']),\
                        'M1_TOTAL':M1_TOT,'M3_TOTAL':M3_TOT,'M7_TOTAL':M7_TOT,'M14_TOTAL':M14_TOT,\
                        'M0_ratio':list(AV080[AV080['Revision_type']=='M0']['Ratio']),'M1_ratio':M1_ratio,'M3_ratio':M3_ratio,\
                        'M7_ratio':M7_ratio,'M14_ratio':M14_ratio})
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


#========================GR_150=================================================
gr_150_raw = pd.read_sql_query("select * from GR_150",connection)
gr_150 = gr_150_raw[(gr_150_raw['PARTICIPANT']=='PRME')&(gr_150_raw['Metering_Type']=='NHH')].copy()
gr_150.sort_values(by = ['PARTICIPANT','Metering_Type','RECONPERIOD','Revision_Cycle','RUN_DATE'],inplace = True)
gr_150.reset_index(drop = True,inplace = True)
gr_150.drop_duplicates(subset = ['PARTICIPANT','Metering_Type','RECONPERIOD'],keep = 'last',inplace = True)
gr_150.reset_index(drop =True,inplace = True)
if len(gr_150['RECONPERIOD'].unique())!=len(gr_150):
    print('Something is wrong, check GR_150 table')
    sys.exit()
#======================GR_150 END=====================================================

#=========================AV080 VS AV120=============================
global av080_av120_merge_V2
AV080_groupby = AV080.groupby(by=['RECONPERIOD','Revision_type'],as_index=False)['TOTAL','ACTUALS'].sum()

AV120 = pd.read_sql_query("select * from AV120",connection)
AV120_groupby = AV120.groupby(by=['RECONPERIOD','Revision_type'],as_index=False)['TOTAL'].sum()

asbilled_period = []
for i,row in enumerate(AV120_groupby.itertuples()):
    temp_ym = datetime.strptime(row.RECONPERIOD,"%Y-%m-%d").strftime("%Y%m")
    temp_date = YM_subtract.year_month_subtract_month(temp_ym,1)
    asbilled_period.append(datetime.strptime(temp_date,"%Y%m").strftime("%Y-%m-%d"))
AV120_groupby['AsBilled_period'] = asbilled_period
AV120_groupby.rename(columns={'TOTAL':'Asbilled_vol','RECONPERIOD':'AsBilled_Reconperiod'},inplace = True)

av080_av120_merge = pd.merge(AV080_groupby,AV120_groupby,how='left',left_on = ['RECONPERIOD','Revision_type'],\
                            right_on = ['AsBilled_period','Revision_type'])

av080_av120_merge_V2 = av080_av120_merge[av080_av120_merge['Asbilled_vol'].notnull()].copy()
av080_av120_merge_V2.sort_values(by = ['RECONPERIOD','Revision_type'],inplace = True)
av080_av120_merge_V2.reset_index(drop = True,inplace = True)
#av080_av120_merge_V2['HE_percent'] = av080_av120_merge_V2['ACTUALS']/av080_av120_merge_V2['TOTAL']
#============================AV080 VS AV120 END======================


#====================================AV080 VS GR_010========================
GR010_raw = pd.read_sql_query("select * from GR_010 where CONTRACT_NUMBER = 'PRME1'",connection)
#AV080_raw2 = pd.read_sql_query("select * from AV080",connection)
ym= pd.to_datetime(AV080_raw.RECONPERIOD,format="%Y-%m-%d")
AV080_raw['YM'] = ym.apply(lambda x: x.strftime('%Y%m'))
ym= pd.to_datetime(GR010_raw.TRADING_DATE,format="%d/%m/%Y")
GR010_raw['YM'] = ym.apply(lambda x: x.strftime('%Y%m'))
GR010 = GR010_raw.groupby(by = ['YM','RUN_DATE'],as_index=False)['CHECKSUM'].sum()
AV080_b = AV080_raw.groupby(by = ['Revision_type','RUNDATE','YM'],as_index=False)['TOTAL'].sum()
temp_merge = pd.merge(AV080_b,GR010,how='left',on='YM')
temp_merge['RUNDATE_datetime'] = pd.to_datetime(temp_merge.RUNDATE,format="%Y-%m-%d")
temp_merge['RUN_DATE_datetime'] = pd.to_datetime(temp_merge.RUN_DATE,format="%Y-%m-%d")
temp_merge['diff'] = (temp_merge['RUN_DATE_datetime']-temp_merge['RUNDATE_datetime']).dt.days
temp_merge.sort_values(by = ['Revision_type','YM','diff'],inplace = True)
temp_merge2 = temp_merge[temp_merge['diff']>=0].copy()
temp_merge2.reset_index(drop = True,inplace = True)
temp_merge2.drop_duplicates(subset = ['Revision_type','YM'],keep = 'first',inplace = True)
temp_merge2.reset_index(drop =True,inplace = True)
temp_merge2['Ratio'] = temp_merge2['CHECKSUM']/temp_merge2['TOTAL']
ym= pd.to_datetime(temp_merge2.YM,format="%Y%m")
temp_merge2['RECONPERIOD'] = ym.apply(lambda x: x.strftime('%Y-%m-%d'))
#=====================================AV080_VS GR_010 END=========================




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
                            ],
                    value = 'Variance_M0_percent',
                    #multi = True,
                    ),
                    dcc.Graph(id = 'Variance_PRE_period_Graph',)
                    ],className='six columns'),
            html.Div([
                    dcc.Dropdown(id = 'Variance_CUR_PRE_dropdown',
                    options=[
                            {'label':'Variance_M1','value':'Variance_M1_CUR_PRE'},
                            {'label':'Variance_M3','value':'Variance_M3_CUR_PRE'},
                            {'label':'Variance_M7','value':'Variance_M7_CUR_PRE'},
                            {'label':'Variance_M14','value':'Variance_M14_CUR_PRE'},
                            ],
                    value = 'Variance_M1_CUR_PRE',
                                 
                                 
                                 ),
                    
                    dcc.Graph(id = 'Variance_CUR_PRE_Graph',)
                    ],className='six columns')
            ],className="row"),
    html.Br(),
    html.Div([
            html.Div([
                    dcc.Dropdown(id = 'HE_Ratio_dropdown',
                    options = [
                            {'label':'M0_RATIO','value':'M0_ratio'},
                            {'label':'M1_RATIO','value':'M1_ratio'},
                            {'label':'M3_RATIO','value':'M3_ratio'},
                            {'label':'M7_RATIO','value':'M7_ratio'},
                            {'label':'M14_RATIO','value':'M14_ratio'},
                            ],
                    value = 'M0_ratio',
                                 ),
                    dcc.Graph(id = 'AV080_HE_ratio_graph')
                    ],className='six columns'),
            html.Div([
                    dcc.Graph(id = 'GR-150-graph',
                              figure={
                                      'data':[
                                              {'x' : list(gr_150['RECONPERIOD']),
                                               'y' : list(gr_150['Difference']),
                                               'type': 'bar','name':'RM_PRME_ICPDays_Diff'},
                                              ],
                                        'layout': go.Layout(
                                                title='RM ICPDays VS PRME ICPDays',
                                                )
                                            })
                              ],className="six columns",)
                    
                    ], className = 'row'),
    html.Br(),
    html.Div([
            dcc.Dropdown(
                    id = 'AV080_120_comparison',
                    options=[
                            {'label':'M0','value':'M0'},
                            {'label':'M1','value':'M1'},
                            {'label':'M3','value':'M3'},
                            {'label':'M7','value':'M7'},
                            {'label':'M14','value':'M14'}
                            ],
                    value = 'M0',
                    ),
            dcc.Graph(id = 'AV080_120_comparison_Graph')
            ]),
    html.Br(),
    html.Div([
            dcc.Dropdown(
                    id = "AV080_GR010_comparison",
                    options = [
                            {'label':'M0','value':'M0'},
                            {'label':'M1','value':'M1'},
                            {'label':'M3','value':'M3'},
                            {'label':'M7','value':'M7'},
                            {'label':'M14','value':'M14'},
                            ],
                    value = 'M0'
                    ),
            dcc.Graph(id = "AV080_GR010_comparison_Graph")
            ])
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
    
@app.callback(
        Output('AV080_HE_ratio_graph','figure'),
        [Input("HE_Ratio_dropdown","value")])
def update_figure2(he_ratio_dropdown_menu):
    temp_filtered_x_val = list(AV080[AV080['Revision_type']=='M0']['RECONPERIOD'])
    if he_ratio_dropdown_menu is None:       
        temp_filtered_y_val = list(AV080_df['M0_ratio'])
    else:
        temp_filtered_y_val = list(AV080_df[str(he_ratio_dropdown_menu)])
        return {
                'data':[
                                {
                                        'x': temp_filtered_x_val,
                                        'y': temp_filtered_y_val,
                                        'type':'lines','name':'Historical_Est_ratio',"color": "#F22604"
                                },                                  
                        ],
                "layout": go.Layout(
                        autosize=True,
                        title='Historical Estimate Ratio',
                        xaxis=dict(
                                title='RECONPERIOD',
                            ),
                        yaxis=dict(
                                    title='%'),
                        bargap=0.2,
                        margin={'t': 40,'b':30},
                            #barmode="group"
                            ), 
            }
    

@app.callback(
        Output('AV080_120_comparison_Graph','figure'),
        [Input("AV080_120_comparison","value")])

def update_figure3(av080_120_comparison):
    if av080_120_comparison is None:
        temp_filtered_df_av080_120_comp = av080_av120_merge_V2[av080_av120_merge_V2['Revision_type']=='M0'].copy()
        #temp_filtered_df = av080_av120_merge_V2.copy()
    else:
        temp_filtered_df_av080_120_comp = av080_av120_merge_V2[av080_av120_merge_V2['Revision_type']==str(av080_120_comparison)].copy()
        #temp_filtered_df_av080_120_comp = av080_av120_merge_V2[av080_av120_merge_V2['Revision_type']=='M1'].copy()
    return {
            'data':[
                            go.Scatter(
                                    x= list(temp_filtered_df_av080_120_comp['RECONPERIOD']), y= list(temp_filtered_df_av080_120_comp['TOTAL']),
                                    #offset = 0,
                                    #width = 1,
                                    #name="OP",
                                    line = {"color":"#FF1A11"},
                                    mode = "lines",
                                    name = 'AV080'),
                            go.Scatter(
                                    x=list(temp_filtered_df_av080_120_comp['RECONPERIOD']), y= list(temp_filtered_df_av080_120_comp['Asbilled_vol']),
                                    #offset = -0.5,
                                    #width = 1,
                                    line = {"color":"#119DFF"},
                                    mode = "lines",
                                    name="AV120")],
                            "layout": go.Layout(
                                                title = 'AV080 VS AV120',
                                                autosize=False,
                                                bargap=0.5,
                                                xaxis = dict(
                                                        title = 'RECONPERIOD',
                                                        ),
                                                yaxis = dict(
                                                        title = 'kWh',
                                                        ),
                                                barmode="group"
                                                ),
            }
                            
@app.callback(
        Output('AV080_GR010_comparison_Graph','figure'),
        [Input("AV080_GR010_comparison","value")])

def update_figure4(drop_down_gr010_av080):
    if drop_down_gr010_av080 is None:
        temp_gr010_av080_df = temp_merge2[temp_merge2['Revision_type']=='M0']
        temp_gr010_av080_df.sort_values(by = ['YM'],inplace = True)
    else:
        temp_gr010_av080_df = temp_merge2[temp_merge2['Revision_type']==str(drop_down_gr010_av080)]
        temp_gr010_av080_df.sort_values(by = ['YM'],inplace = True)
        
    return {
            'data':[
                    {
                            'x':list(temp_gr010_av080_df['RECONPERIOD']),
                            'y':list(temp_gr010_av080_df['Ratio']),
                            'type':'lines','name':'HIST_Loss',"color": "#F22604"
                            }
                    ],
            "layout": go.Layout(
                        autosize=True,
                        title='Historical ratio of UFE_Loss_factor',
                        xaxis=dict(
                                title='RECONPERIOD',
                            ),
                        yaxis=dict(
                                    title=''),
                        #bargap=0.2,
                        margin={'t': 40,'b':30},
                            #barmode="group"
                            ), 
            }
        