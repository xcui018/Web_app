# -*- coding: utf-8 -*-
"""
Created on Thu Jan 30 09:19:22 2020

@author: Aaron
"""
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
import sqlite3
#from datetime import datetime
#import numpy as np
from app import app
#import sys

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

database_location = r'R:\03 Prime_Folders\Aaron\Reconciliation_database'
connection = create_connection(database_location+'/Reconciliation_databse.sl3')

EIEP_raw = pd.read_sql_query("select * from EIEP1",connection)

new_charge = []
for i,row in enumerate(EIEP_raw.itertuples()):
    try:
        temp = float(row.Network_Charge)
        new_charge.append(float(row.Network_Charge))
    except:
        new_charge.append(0)
EIEP_raw['Network_Charge'] = new_charge
EIEP = EIEP_raw.groupby(by=['Report_type','Revision_type','REPORTMONTH','F_V'],as_index = False)['UNITs','Network_Charge'].sum()
EIEP_a = EIEP[EIEP['F_V']=='V'].copy()
EIEP_a.reset_index(drop = True,inplace = True)



EIEP1_Revision_type_list_ = ['M0','M1','M3','M7','M14']
layout = html.Div([
        #html.H6('HIST NZX VOL'),
        html.Br(),
        
        html.Div([
                dcc.Dropdown(
                        id = "EIEP1_report_type_dropdown",
                        options = [
                                {'label':'AsBilled','value':'AB'},
                                {'label':'Normalized','value':'NM'},
                                ],
                        value = "AB",
                        ),
                dcc.Dropdown(
                        id = "EIEP1_Revision_type_dropdown",
                        ),
                dcc.Graph(
                        id = "EIEP1_hist_network_charge_graph"
                        )
                ])
        
    ])
                
@app.callback(
    Output("EIEP1_Revision_type_dropdown", "options"),
    [ Input("EIEP1_report_type_dropdown", "value") ],
    )
def Update_EIEP(report_type):
    
    temp_revision_type= []
    EIEP1_Revision_type_list_ = [str(report_type)+'_M0',str(report_type)+'_M1',\
                                 str(report_type)+'_M3',str(report_type)+'_M7',str(report_type)+'_M14']
    
    temp_revision_type += [ dict(label = ele, value = ele) for ele in EIEP1_Revision_type_list_ ]
    
    return temp_revision_type

@app.callback(
    Output("EIEP1_Revision_type_dropdown", "value"),
    [ Input("EIEP1_Revision_type_dropdown", "options") ],
    )
def Update_EIEP1(eiep_revision_type_):
    if len(eiep_revision_type_)==0:
        return 'NM_M0'
    else:
        eiep_revision_type_

@app.callback(
     Output("EIEP1_hist_network_charge_graph", "figure"),
    [ Input("EIEP1_Revision_type_dropdown", "value") ],   
        )
def Update_EIEP2(eiep_revision_type):
    
    if len(eiep_revision_type)==0:
        eiep_temp_filtered_df = EIEP_a[(EIEP_a['Revision_type']=='M0')&(EIEP_a['Report_type']=='NM')]
    else:
        eiep_temp_filtered_df = EIEP_a[(EIEP_a['Revision_type']==str(eiep_revision_type).split('_')[1])&\
                                       (EIEP_a['Report_type']==str(eiep_revision_type).split('_')[0])]
    return {
            'data':[
                    {
                            'x':list(eiep_temp_filtered_df['REPORTMONTH']),
                            'y':list(eiep_temp_filtered_df['Network_Charge']),
                            'type':'bar','name':'HIST_Network_Charge',"color": "#F22604"
                            }
                    ],
            "layout": go.Layout(
                        autosize=True,
                        title='Historical Network Charge',
                        xaxis=dict(
                                title='RECONPERIOD',
                            ),
                        yaxis=dict(
                                    title='$NZD'),
                        #bargap=0.2,
                        margin={'t': 40,'b':30},
                            #barmode="group"
                            ), 
            }
   
