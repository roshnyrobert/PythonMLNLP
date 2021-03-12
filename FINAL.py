
import pandas as pd
import webbrowser
import sqlite3 as sql
import pickle
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from  dash.dependencies import Input, Output, State
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer

app=dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
Project_name="SENTIMENT ANALYSIS WITH INSIGHTS"

def open_browser():
    return webbrowser.open_new("https://127.0.0.1/:8050/")

def load_model():
    global pickle_model
    global vocab
    global df
    global assign 
    
    df=pd.read_csv("balanced_reviews.csv")
    assign=pd.read_csv("FINAL REVIEWSAll.csv")

    with open("pickle_model.pkl",'rb') as file:
        pickle_model=pickle.load(file)
        
    with open("features.pkl",'rb') as voc:
        vocab=pickle.load(voc)
        
def check_reviews(reviewText): 
    global Project_name
    conn=sql.connect('FINAL REVIEWSAll.db')
    assignNew=conn.execute('SELECT reviews FROM FINAL REVIEWSAllTable').fetchall()     
    res=[''.join(i) for i in assignNew]
    main_layout=dbc.Container(
        dbc.Jumbotron(
                [
                    html.H1(id='heading',children=Project_name, className='display-3 mb-4')
                    dbc.Textarea(id='textarea',className="mb-3",placeholder="ENTER THE REVIEW", value='MY DAUGHTER LOVES THESE SHOES',style={'height': '150px'}),
                    dbc.Div([
                        dcc.Dropdown(
                    id='dropdown',
                    placeholder='Select a Review',
                    options=[{'label':i[:100]+"...",'value':i} for i in res],
                    value=df.reviewtext[0],
                    style={'margin-bottom':'40px'}
                )
                        ],
                        style={'padding-right':'50px','padding-left':'50px'}
                        ),
                    dbc.Button("Submit",color="dark",className="mt-2 mb-3", id='button',style={'width':'110px'}),
                    html.Div(id='result'),
                    html.Div(id='result')
                    ],
                className='text-center'
                ),
        classNaame='mt-4'
        )
    return main_layout

@app.callback(
    Output('result','children'),
    [
    Input('button','n_clicks')
    ],
    [
    State('textarea','value')
    ]
    )

def update_app_ui(n_clicks,textarea):
    final_list= check_review(textarea)
    
    if (result_list[0]==0):
        return dbc.Alert("NEGATIVE",color="FAIL")
    elif (result_list[0]==1):
        return dbc.Alert("POSITIVE",color="SUCESS")
    else:
        return dbc.Alert("UNKNOWN",color="DARK")


@app.callback(
    Output('result','children'),
    [
    Input('button','n_clicks')
    ],
    [
    State('textarea','value')
    ]
    )
    
def update_dropdown(n_clicks,value):
    final_list=check_review(value)
    
    if (result_list[0]==0):
        return dbc.Alert("NEGATIVE",color="FAIL")
    elif (result_list[0]==1):
        return dbc.Alert("POSITIVE",color="SUCESS")
    else:
        return dbc.Alert("UNKNOWN",color="DARK")
    
def main():
    global app
    global Project_name
    load_model()
    open_browser()
    app.layout=create_app_ui()
    app.title=Project_name
    app.run_server()
    app=None
    Project_name=None
if __name__=='__main__':
    main()

































































































