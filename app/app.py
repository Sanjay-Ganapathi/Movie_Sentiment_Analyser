from scraper import get_user_reviews,get_critic_reviews,get_image_url,get_rel_date_runtime,get_description
from utils import preprocess,predict,labels_list,scores_list
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output,Input,State
from dash.exceptions import PreventUpdate
import pandas as pd
import plotly.graph_objects as go
from concurrent.futures import ThreadPoolExecutor
import flask



colors = {
    'background':'#070807',
    'font':'white',
    'first div':'#242323',
    'second div':'#4a4945',
    'hist_bg':'#312c8a',
    'hist_bin':'#c71585',
    'pie_bg':'#1a9ef0'

}

def plot_hist(arr,title,bin_color = colors['hist_bin'],bg_color = colors['hist_bg']):
    data = go.Histogram(x = arr,marker = {'color':bin_color})
    layout = go.Layout(title=title,title_x=0.5,plot_bgcolor=bg_color,paper_bgcolor = bg_color,title_font_color = colors['font'],xaxis = {'color':'white'},yaxis = {'color':'white'})
    
    fig = {'data':[data],'layout':layout}
    return fig

def plot_pie(arr,title,bg_color = colors['pie_bg']):
    
    labels = ['Positive','Negative','Neutral']
    values = [arr.count('Positive'),arr.count('Negative'), arr.count('Neutral')]

    data = go.Pie(labels=labels, values=values,marker = {'line' : dict(color='#000000', width=2)})

    layout = go.Layout(title=title,title_x=0.5,paper_bgcolor = bg_color,title_font_color = colors['font'])

    fig = {'data':[data],'layout':layout}
    return fig

server = flask.Flask(__name__)
app = dash.Dash(__name__,server = server)


app.layout = html.Div([
    
                        html.Div([
                                    html.H1('Movie Sentiment Analyser',style = {'color':colors['font'],'text-align':'center','padding-top':'5px'}),
                                    html.H3('Analyses Critic and User Reviews of searched movie by scraping Rotten Tomatoes',style =  {'color':colors['font'],'text-align':'center'}),
                                 ]),
                        
                        

                        html.Div([  
                                    html.H3('Enter the movie name here : ',style = {'display':'inline-block','color':colors['font'],'padding-left':'400px'}),
                                    dcc.Input(id = 'search_term',value='the dark knight',type = 'text',style = {'display':'inline-block','width':'50%','height':'20px','padding-top':'22px','padding-left':'5px','background-color':colors['background'],'border':'hidden','color':colors['font'],'fontSize':18}),
                                    html.Button('Submit',id = 'submit_button',style = {'display':'inline-block','width':'100px','fontSize':18,'background-color':'red'})
                                 ],style = {'display':'flex','justifyContent':'center',}),

                        html.Div([
                                    html.Div([
                                                html.P(id = 'description')
                                             ]),
                                    
                                    html.Div([
                                                html.Img(id = 'image')
                                             ],style = {"text-align":"center"}),

                                    html.Div([
                                                html.P(id = 'release_date'),
                                                html.P(id = 'runtime')
                                             ],style = {"text-align":"center"})
                                    
                                ],style = {'background-color':colors['first div'],'color':colors['font']}),

                        dcc.Loading(
                             id='loading',
                             type='default',
                            children=html.Div([  
                            #To do 1.first hist count  of sentiment of critic and user review --done
                                    #2.Pie chart of same --done
                                    #3.AVerage score of critic and user review --done
                                    #4.Weighted Average of both --done

                                    html.H2('Analysis of Latest 60 Critic and User Reviews'),
                                    
                                    html.Div([                                                      
                                                dcc.Graph(id = 'critic_hist',style = {'display':'inline-block'}),
                                                
                                                dcc.Graph(id = 'user_hist',style = {'display':'inline-block','padding-left':'20px'})
                                             ],style = {'text-align':'center'}),
                                    
                                    html.Div([
                                                dcc.Graph(id = 'critic_pie',style = {'display':'inline-block'}),
                                                dcc.Graph(id = 'user_pie',style = {'display':'inline-block','padding-left':'20px'})
                                             ],style = {'text-align':'center','padding-top':'20px'}),

                                    html.Div([
                                                html.H3(id = 'avg_critic_score',style={'background-color':colors['second div'],'color':colors['font'],'fontSize':22,'font-family':'Trebuchet MS'}),
                                                html.H3(id = 'avg_user_score',style={'background-color':colors['second div'],'color':colors['font'],'fontSize':22,'font-family':'Trebuchet MS'}),
                                                html.H3(id = 'avg_score',style={'background-color':colors['second div'],'color':colors['font'],'fontSize':22,'font-family':'Trebuchet MS'})
                                    ],style = {'text-align':'center','padding-top':'20px'})
                            


                                    
                                 ],style = {'background-color':colors['second div'],'color':colors['font'],'text-align':'center'})),
                        

                        html.Div([
                                    dcc.Markdown('''
                                                    #### *Model Used: Bidirectional LSTM*
                                                    #### *Embeddings : Pretrained Word2Vec Google News Corpus(Dim:300)*
                                                    #### *Model trained on: Twitter Data*
                                                    #### [*Kaggle Link*](https://www.kaggle.com/ethanhunt1080/sentiment-analyzer)
                                                    ''')
                                ],style = {'color':colors['font'],'fontSize':18})
                                
                

                       ],style = {
                                    'background-color': colors['background'],
                                    'margin-left':'-8px',
                                    'margin-right':'-8px',
                                    'margin-top':'-22px',
                                    'margin-bottom':'-hidden'
                                    
                                    })


executor = ThreadPoolExecutor()


@app.callback([Output('description','children'),
                Output('image','src'),
                Output('release_date','children'),
                Output('runtime','children')],
                [Input('submit_button','n_clicks')],
                [State('search_term','value')])
def update_img_desc_reldate_runtime(n,val):
    try:
        if val:
            description = executor.submit(get_description,val)
            img = executor.submit(get_image_url,val)
            rel_runtime = executor.submit(get_rel_date_runtime,val)
            rel_date = 'Release Date : {}'.format(rel_runtime.result()['release_date'])
            runtime = 'Runtime : {}'.format(rel_runtime.result()['runtime'])

            return description.result(),img.result(),rel_date,runtime
    except Exception as e:
        return 'Please Enter the Correct Name of the Movie','',str(e),''

@app.callback([Output('critic_hist','figure'),
                Output('user_hist','figure'),
                Output('critic_pie','figure'),
                Output('user_pie','figure'),
                Output('avg_critic_score','children'),
                Output('avg_user_score','children'),
                Output('avg_score','children')],
                [Input('submit_button','n_clicks')],
                [State('search_term','value')])
def update_hist_pie(n,val):
    try:
        if val:
            critic = executor.submit(get_critic_reviews,val)
            user = executor.submit(get_user_reviews,val)

            critic_reviews = critic.result()
            user_reviews = user.result()
            #critic_reviews = get_critic_reviews(val)
            #user_reviews = get_user_reviews(val)

            critic_sentiment = labels_list(critic_reviews)
            user_sentiment = labels_list(user_reviews)
            
            critic_hist = plot_hist(critic_sentiment,'Critic Reviews')
            user_hist = plot_hist(user_sentiment,'User Reviews')
            critic_pie =plot_pie(critic_sentiment,'Critic Reviews')
            user_pie = plot_pie(user_sentiment,'User Reviews')

            critic_scores = scores_list(critic_reviews)
            user_scores = scores_list(user_reviews)

            critic_avg = round(sum(critic_scores)/len(critic_scores),2)
            user_avg = round(sum(user_scores)/len(user_scores),2)
            avg = round(critic_avg/2+user_avg/2,2)
            
            critic_avg = f'Average Score of Critics : {critic_avg}'
            user_avg = f'Average Score of Users : {user_avg}'
            avg = f'Weighted Average : {avg}'

            return critic_hist,user_hist,critic_pie,user_pie,critic_avg,user_avg,avg
    except:
        raise PreventUpdate
        


    
    
    

if __name__ == '__main__':
    
    app.run_server(debug = True)
