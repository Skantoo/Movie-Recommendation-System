import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_title):
    api_key = "a68d6507"
    url = f"http://www.omdbapi.com/?t={movie_title}&apikey={api_key}"
    response = requests.get(url).json()
    if response['Response'] == "True":
        return response.get('Poster')
    else:
        return "https://via.placeholder.com/300x450?text=Poster+Not+Available"

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies = []
    recommended_posters = []
    for i in movies_list:
        movie_title = movies.iloc[i[0]]['title']
        recommended_movies.append(movie_title)
        recommended_posters.append(fetch_poster(movie_title))
    return recommended_movies, recommended_posters

movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('Movie Recommendation System')

selected_movie_name = st.selectbox("If you watched this:", movies['title'].values)

if st.button('Recommend'):
    recommendations, posters = recommend(selected_movie_name)
    st.write('### You might even like:')
    cols = st.columns(5) 
    for col, movie, poster in zip(cols, recommendations, posters):
        with col:
            st.image(poster, width=150, caption=movie)
