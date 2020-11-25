import requests
import re
import json
from bs4 import BeautifulSoup

#Helper Functions
base_url = 'https://www.rottentomatoes.com/m/'

#Helper function -1 for getting url of user review site
def get_user_url(movie_name):
    return base_url + '_'.join(movie_name.lower().split()) + '/reviews?type=user'

#Helper function -2 for fetching reviews from next page
def fetch_user_reviews(endCursor,url):
    params = {'directions':'next',
         'endCursor':endCursor,
         'startCursor':''}

    rev_json = requests.get(url,params = params).json()
    return rev_json

#Helper function -1 for getting url of critic review site
def get_critic_url(movie_name):
    return base_url+ '_'.join(movie_name.lower().split())+'/reviews'




#User Review function - start
def get_user_reviews(movie_name):
    '''
    returns list of 60 user reviews
    
    '''
    try:
        url = get_user_url(movie_name)
        #print(url)
        resp = requests.get(url)
        #print(resp.status_code)
        data = json.loads(re.search(r'movieReview\s=\s(.*);', resp.text).group(1))
        movieID = data['movieId']

        review_url = 'https://www.rottentomatoes.com/napi/movie/'+movieID+'/reviews/user'
        reviews = []
        result = {}

        
        for i in range(6):
            #print('page {}'.format(i))
            result = fetch_user_reviews(endCursor = result['pageInfo']['endCursor'] if i!=0 else '',url = review_url)
            reviews.extend(t['review'] for t in result['reviews'])
        
        if (len(reviews)) < 50:
            #print(len(reviews))
            print('Not enough reviews')
        else:
            return reviews

    except:
        print('Please Enter correct name of movie')
#User Review function  - end



#Critic Review function -start
def get_critic_reviews(movie_name):
    ''' 
    returns list of 60 critic reviews

    '''
    try:
        url = get_critic_url(movie_name)
        lst = []
        for i in range(3):
            params = {
                'type':'',
                'sort':'',
                'page':str(i+1)
            }
            resp = requests.get(url,params)
            #print(i,resp.status_code)
            bs = BeautifulSoup(resp.text,'lxml')
            for i in bs.find_all('div',{'class':'the_review'}):
                lst.append(i.get_text().strip())
            
        if (len(lst)) < 50:
            #print(len(lst))
            print('Not enough reviews')
        else:
            return lst

    except Exception as e:
        print(e)
        print('Please Enter correct name of movie')
#Critic Review function - end



#Image-url function -start
def get_image_url(movie_name):
    '''
    returns url of image of the input movie from RT site

    '''
    if movie_name:
        url = base_url+'_'.join(movie_name.lower().split())
        resp = requests.get(url)
        bs = BeautifulSoup(resp.text,'lxml')
        return bs.find('img',{'class':'posterImage js-lazyLoad'})['data-src']
#Image-url function -end


#Getting release date and runtime function -start
def get_rel_date_runtime(movie_name):
    if movie_name:
        url = base_url+'_'.join(movie_name.lower().split())
        resp = requests.get(url)
        bs = BeautifulSoup(resp.text,'lxml')
        rel_date = bs.find_all('time')[0].get_text().strip()

        try:

            runtime = bs.find_all('time')[2].get_text().strip()
        except:

            runtime = bs.find_all('time')[1].get_text().strip()
        
        return {'release_date':rel_date,'runtime':runtime}
#Getting release date and runtime function -end


#Getting movie description function -start
def get_description(movie_name):
    if movie_name:
        url = base_url+'_'.join(movie_name.lower().split())
        resp = requests.get(url)
        bs = BeautifulSoup(resp.text,'lxml')
    
        return bs.find('div',{'class':'movie_synopsis clamp clamp-6 js-clamp'}).get_text().strip()
#Getting moovie description fucntion -end
