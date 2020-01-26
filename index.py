#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 25 04:59:01 2020

@author: xuncui
"""

import dash_core_components as dcc
import dash_html_components as html
import base64
from dash.dependencies import Input, Output
from app import app
from Pages import HHR_Data,NZX
from utils import web_tab,get_menu



prime_logo_path = './Pictures/PRME_logo.png'
encoded_image = base64.b64encode(open(prime_logo_path, 'rb').read())
app.layout = html.Div([
        html.Div([
                html.Img(
                src='data:image/png;base64,{}'.format(encoded_image.decode()),
                style={
                        'height': '20%',
                        'width': '20%'
                        })
        ], style={'textAlign': 'left'}),
        html.Br(),
        #get_menu(),
        #dcc.Location(id="url",refresh=False),
        #html.Div(id = "page-content")
        web_tab(),
    #dcc.Location(id='url', refresh=False),
    #utils.web_tab(),
    #html.Br(),
    #html.Div([
    #        dcc.Tabs(id="tabs-styled-with-inline", value='tab-1', children=[
    #        dcc.Tab(label='NZX', value='tab-1', style=tab_style, selected_style=tab_selected_style),
    #        dcc.Tab(label='HHR Data', value='tab-2', style=tab_style, selected_style=tab_selected_style),
    #        dcc.Tab(label='EIEP', value='tab-3', style=tab_style, selected_style=tab_selected_style),
    #        dcc.Tab(label='Spot Market', value='tab-4', style=tab_style, selected_style=tab_selected_style),
    #        ], style=tabs_styles),
     #       html.Div(id='page-content')

    #        ]),
])


@app.callback(Output('page-content', 'children'),
              [Input('tabs-styled-with-inline', 'value')])
              #[#Input('url', 'pathname')])
def display_page(tab):
    if tab == 'tab-1':
        return NZX.layout
    else:
        return HHR_Data.layout

if __name__ == '__main__':
    app.run_server(debug=True,port=8030)