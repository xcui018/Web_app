#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 25 05:52:42 2020

@author: xuncui
"""

import dash_html_components as html
import dash_core_components as dcc
import sqlite3

tabs_styles = {
    'height': '44px'
}
tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold'
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#119DFF',
    'color': 'white',
    'padding': '6px'
}
def web_tab():
    return html.Div([
            dcc.Tabs(id="tabs-styled-with-inline", value='tab-1', children=[
            dcc.Tab(label='NZX', value='tab-1', style=tab_style, selected_style=tab_selected_style),
            dcc.Tab(label='EIEP', value='tab-2', style=tab_style, selected_style=tab_selected_style),
            dcc.Tab(label='HHR_Data', value='tab-3', style=tab_style, selected_style=tab_selected_style),
            dcc.Tab(label='Spot Market', value='tab-4', style=tab_style, selected_style=tab_selected_style),
            ], style=tabs_styles),
            html.Div(id='page-content')
    ])
    
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
 

    
def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except sqlite3.Error as e:
        print(e)
        
def get_menu():
    menu = html.Div(
        [
            dcc.Link(
                "NZX",
                href="/",
                className="tab first",
            ),
            dcc.Link(
                "EIEP",
                href="/report/eiep",
                className="tab",
            ),
        ],
        className="row all-tabs",
    )
    return menu