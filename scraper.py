# -*- coding: utf-8 -*-
"""
Created on Tue Mar 28 11:50:26 2023

@author: User
"""

import pandas as pd
import requests
import time

OMDB_API_KEY = 'YOUR_API_KEY'
MOVIE_IDS = ['tt1375666', 'tt0816692', 'tt0468569'] # example movie IDs

def get_movie_data(movie_id):
    url = 'http://www.omdbapi.com/'
    params = {'i': movie_id, 'apikey': OMDB_API_KEY}
    response = requests.get(url, params=params)
    data = response.json()
    movie_data = {
        'title': data['Title'],
        'rating': float(data['imdbRating']),
        'genre': data['Genre'],
        'num_votes': int(data['imdbVotes'].replace(',', ''))
    }
    return movie_data

def get_all_movie_data(movie_ids):
    all_data = []
    for movie_id in movie_ids:
        movie_data = get_movie_data(movie_id)
        all_data.append(movie_data)
    return all_data

def create_dataframe(movie_data_list):
    df = pd.DataFrame(movie_data_list)
    df.set_index('title', inplace=True)
    return df

def main():
    while True:
        movie_data = get_all_movie_data(MOVIE_IDS)
        df = create_dataframe(movie_data)
        df.to_csv('movie_rankings.csv')
        time.sleep(86400) # pause for 1 day (86400 seconds)

if __name__ == '__main__':
    main()