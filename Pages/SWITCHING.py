# -*- coding: utf-8 -*-
"""
Created on Fri Mar  6 14:52:50 2020

@author: Aaron
"""

import dash_core_components as dcc
import dash_table
import dash_daq as daq
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
import sqlite3
from datetime import datetime
import numpy as np
from app import app
#import sys
import YM_subtract
import Active_Lis

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

current = datetime.now()
current_date = current.strftime("%Y%m")
path = r'R:\03 Prime_Folders\Aaron\RM_raw_input_data\Lis_File/LIS20200303103906.txt'
active_lis_date_input = YM_subtract.year_month_subtract_month(current_date,1)
Lis_out2,b,c = Active_Lis.active_lis(path,active_lis_date_input,'AV')
new_conn_df = Lis_out2[Lis_out2['Status_Reason_Description']=='New_Connection_in_progress'].copy()
PR255_icp = pd.read_sql_query("select distinct ICP from PR255",connection)
target_new_conn = new_conn_df[new_conn_df['ICP'].isin(list(PR255_icp['ICP']))].copy()
target_new_conn2 = target_new_conn[['ICP','Network','GXP','ICP_Status_Code','Status_Reason_Description']].copy()

layout = html.Div([
        dash_table.DataTable(id = 'new_conn_table',
                             columns = [{"name": i, "id": i} for i in target_new_conn2.columns],
                             data=target_new_conn2.to_dict('records')
                             )
        ])

    