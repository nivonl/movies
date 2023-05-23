# -*- coding: utf-8 -*-
"""
Created on Sat Apr 29 10:56:23 2023

@author: User
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from datetime import datetime
import numpy as np
import re

# initialize an empty dataframe to store movie data
"""
movie_data = pd.DataFrame(columns=['title',
                                   'year',
                                   'genre', 
                                   'rating', 
                                   'votes',
                                   'rank',
                                   'country',
                                   'us_release_date',
                                   'date_of_scraping'])

"""
 # %%

# %%
    

# set the URL for the IMDb search results page for movies released in 2023
url = 'https://www.imdb.com/search/title/?release_date=2023&sort=num_votes,desc'
    
while True:
    print('starting')
    try:

        # send an HTTP request to the IMDb search results page
        response = requests.get(url)

        # parse the HTML response using Beautiful Soup
        soup = BeautifulSoup(response.content, 'html.parser')

        # find all the movie listings on the page
        movie_listings = soup.select('.lister-item')

        # loop through each movie listing and extract the desired data
        for movie in movie_listings:
            print('starrting movie')
            title = getattr( movie.select_one('.lister-item-header a'), 'text', np.nan)
            if title is not np.nan:
                title = title.strip()
                print(title)
            year = getattr(movie.select_one('.lister-item-year'), 'text', np.nan)
                
            if ('–' in year) | (title in movie_data["title"].unique().tolist()) :
                continue  # skip TV series
            
            if '2023' not in year:
                print('End of 2023 !')
                break #stops at the end of 2023 movies
            print(title)
            
            if year is not np.nan:
                year = year.strip('()')
                
            genre = getattr(movie.select_one('.genre'), 'text', np.nan)
            if genre is not np.nan:
                genre = genre.strip()
                
            rating = getattr(movie.select_one('.ratings-imdb-rating strong'), 'text', np.nan)
            
            votes = getattr(movie.select_one('.sort-num_votes-visible span:nth-of-type(2)'), 'text', np.nan)
            if votes is not np.nan:
                votes = votes.replace(',', '')
                
            rank = getattr(movie.select_one('.lister-item-index'), 'text', np.nan)
            if rank is not np.nan:
                rank = rank.strip('.')
                
            
  
            date_of_scraping = datetime.now().strftime('%Y-%m-%d')
            
            movie_data =  pd.concat([movie_data, pd.DataFrame({'title': title, 'year': year, 'genre': genre,
                                            'rating': rating, 'votes': votes, 'rank': rank,            
                                            'country': np.nan,
                                            'us_release_date': np.nan,   
                                            'date_of_scraping':date_of_scraping},
                                                              index=(range(len(movie_listings))))],
                                                              ignore_index=True).drop_duplicates()

        # check if there is a "Next" button on the page
        next_button = soup.select_one('.next-page')
        if next_button:
            # set the URL to the next page of search results
            url = 'https://www.imdb.com' + next_button['href']
            # wait for a few seconds before sending the next request to avoid overwhelming the server
            time.sleep(0.04)
        else:
            # break out of the loop if there is no "Next" button
            break
    except Exception as e:
        # print any errors that occur and continue with the next iteration of the loop
        print(e)
        continue

# print the scraped movie data
#print(movie_data)
   

  # %%


import requests


api_key = "c06e9873"


# Loop over each row in the dataframe and query OMDB API for US release date and country of origin
while len(movie_data.loc[(movie_data["country"].isna()) &
                         movie_data["us_release_date"].isna() ]) >0 :

    for index, row in movie_data.loc[(movie_data["country"].isna()) &
                                     movie_data["us_release_date"].isna() ].iterrows():
        
        title = row["title"]
        year = row["year"]
        print(title)
        
        # Send API request
        url = f"http://www.omdbapi.com/?apikey={api_key}&t={title}&y={year}"
        # wait for a few seconds before sending the next request to avoid overwhelming the server
        time.sleep(0.05)
        response = requests.get(url)
        data = response.json()
        if "reached" in  str(response.content):
            print("Request limit reached!")
            time.sleep(10)
            continue
     
        # Update dataframe with US release date and country of origin
        if "Released" in data:
            movie_data.at[index, "us_release_date"] = data["Released"]
        if "Country" in data:
            movie_data.at[index, "country"] = data["Country"]
            
print('FInish Fetching country and date ! ')
#%%#



print(type(movie_data["country_of_origin"][316]))
