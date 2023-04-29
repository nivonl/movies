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
# initialize an empty dataframe to store movie data
movie_data = pd.DataFrame(columns=['title',
                                   'year',
                                   'genre', 
                                   'rating', 
                                   'votes',
                                   'rank', 
                                   'date_of_scraping',
                                   'release_type'])

# set the URL for the IMDb search results page for movies released in 2023
url = 'https://www.imdb.com/search/title/?release_date=2023&sort=num_votes,desc'
    # %%
while True:
    try:

        # send an HTTP request to the IMDb search results page
        response = requests.get(url)

        # parse the HTML response using Beautiful Soup
        soup = BeautifulSoup(response.content, 'html.parser')

        # find all the movie listings on the page
        movie_listings = soup.select('.lister-item')

        # loop through each movie listing and extract the desired data
        for movie in movie_listings:
            # check if the movie is a movie or a TV series
            release_type = movie.select_one('.lister-item-header .lister-item-year+ span')
            if release_type and release_type.text == '(TV Series)':
                continue  # skip TV series
            title = movie.select_one('.lister-item-header a').text.strip()
            
            year = movie.select_one('.lister-item-year').text.strip('()')
            if ('-' in year) | (title in movie_data["title"].unique().tolist()) :
                continue  # skip TV series
            print(title)
            try:
                genre = movie.select_one('.genre').text.strip()
            except:
                genre = np.nan     
    
            print(genre)
            rating = movie.select_one('.ratings-imdb-rating strong').text
            votes = movie.select_one('.sort-num_votes-visible span:nth-of-type(2)').text.replace(',', '')
            rank = movie.select_one('.lister-item-index').text.strip('.')
            date_of_scraping = datetime.now().strftime('%Y-%m-%d')
            release_type = 'TV Series' if release_type else 'Movie'
            movie_data =  pd.concat([movie_data, pd.DataFrame({'title': title, 'year': year, 'genre': genre,
                                            'rating': rating, 'votes': votes, 'rank': rank,
                                            'date_of_scraping':date_of_scraping},
                                                              index=(range(len(movie_listings))))],
                                                              ignore_index=True).drop_duplicates()

        # check if there is a "Next" button on the page
        next_button = soup.select_one('.next-page')
        if next_button:
            # set the URL to the next page of search results
            url = 'https://www.imdb.com' + next_button['href']
            # wait for a few seconds before sending the next request to avoid overwhelming the server
            time.sleep(3)
        else:
            # break out of the loop if there is no "Next" button
            break
    except Exception as e:
        # print any errors that occur and continue with the next iteration of the loop
        print(e)
        continue
#%%
# print the scraped movie data
print(movie_data)
   


