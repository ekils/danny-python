import plotly.graph_objects as go
import dateutil.parser as dparser
import matplotlib.pyplot as plt 
import plotly.express as px
import numpy as np
import datetime as dt
from scipy import stats
import pandas as pd
import math
import os

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS

app = Flask(__name__)
CORS(app)




def plot_interval_slope(fig, index,y0,y1,eps_date_group_with_add_next,std):
    for std_count in range(4):
        if std_count == 0:
            fillcolor='rgba(150,26,65,0.4)' # r
        elif std_count == 1 :
            fillcolor='rgba(30,90,250,0.4)' # b
        elif std_count == 2:
            fillcolor='rgba(255,255,51,0.2)' # y
        elif std_count == 3:
            fillcolor='rgba(26,190,65,0.2)' # g
        
        fig.add_trace(go.Scatter(
            x=[str(eps_date_group_with_add_next[index+1]), str(eps_date_group_with_add_next[index])],
            y=[y0 - ((std/2)*std_count), y1 - ((std/2)*std_count)],
            fill=None,
            mode='lines',
        ))
        fig.add_trace(go.Scatter(
            x=[str(eps_date_group_with_add_next[index+1]), str(eps_date_group_with_add_next[index])],
            y=[y0 - ((std/2)*(std_count+1)), y1 - ((std/2)*(std_count+1))],
            fill='tonexty',
            fillcolor=fillcolor,
            mode='lines',
        ))

@app.route('/')
def index():
    return 'hello!!'


@app.route('/plot', methods=['POST'])
def postInput():

    data = request.json
    # 將數據轉換為Pandas DataFrame
    df = pd.DataFrame({
        'x_timestring_list': data['x_timestring_list'],
        'y_data_list': data['y_data_list'],
    })
    company = data['company']
    eps_date_group_with_add_next = data['eps_date_group_with_add_next']
    yminValue =  data['yminValue']
    ymaxValue=  data['ymaxValue']
    interval_data_y0 = data['interval_data_y0']
    interval_data_y1=data['interval_data_y1']
    slope = data['slope']
    stdev = data['stdev']

    # print(df)

    # 畫圖：
    fig = go.Figure()
    fig.add_trace(go.Scatter(mode='markers', 
                            x=data["x_timestring_list"],
                            y=data["y_data_list"],
                            marker=dict(
                                color='LightSkyBlue',
                                size=4,
                                line=dict(
                                    color='MediumPurple',
                                    width=1
                                ))))
    
    for x_date in eps_date_group_with_add_next: 
        fig.add_vline(x=x_date, line_width=2, line_dash="dash", line_color="green")

    for index in range(len(data['eps_date_group_with_add_next'])-1):
        y0 = interval_data_y0[index]
        y1 = interval_data_y1[index]
        plot_interval_slope(fig, index,y0,y1,eps_date_group_with_add_next, stdev)  
        


    # new feature add :
    fig.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(step="all")
                ])
            ),
            rangeslider=dict(
                visible=True
            ),
            type="date"
        )
    )

    fig.update_layout(title="PE_Trend_{}".format(company),showlegend=False, yaxis={'side': 'right'})     

    html_file_path = "./html/PE_Trend_{}.html".format(company)
    fig.write_html(html_file_path)
    return send_file(html_file_path, mimetype='text/html')



#if __name__ == '__main__':
   # app.run(host='0.0.0.0', port=3000, debug=True)
 #  app.run()
