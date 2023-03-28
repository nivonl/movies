# -*- coding: utf-8 -*-
"""
Created on Fri Mar 24 23:39:53 2023

@author: User
"""

"""
This script will iinclude scraping data from imbd or other api in order to track ratings,
In Order to get time series data. 
"""




import requests
import pandas as pd

api_key = "c06e9873"
movie_ids = ["tt0111161", "tt0468569", "tt1375666"] # example movie IDs

# Empty DataFrame to store movie data
df_movies_list = []

# Loop over movie titles and query OMDB API for each movie's data
for movie_id in movie_ids:
    # Send API request
    url = f"http://www.omdbapi.com/?apikey={api_key}&i={movie_id}"
    response = requests.get(url)
    data = response.json()
    
    # Convert data to Pandas DataFrame and append to df_movies
   
    df_movie =  pd.DataFrame.from_dict(data)
    df_movies_list.append(df_movie)
    
df_movies = pd.concat( df_movies_list)
    


