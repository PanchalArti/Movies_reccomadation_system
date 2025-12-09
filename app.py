
import streamlit as st
import pickle
import pandas as pd
import gzip

import requests
def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=5d7716e1565284d08a615a391d481e5f'.format(movie_id))
    data = response.json()
    return "http://image.tmdb.org/t/p/w500" +data['poster_path']
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distance = similarity[movie_index]
    movies_list = sorted(list(enumerate(distance)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
      movie_id = movies.iloc[i[0]].movie_id
      #fetch poster from API
      recommended_movies.append(movies.iloc[i[0]].title)
      recommended_movies_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_movies_posters

movie_dict = pickle.load(open('movie_dict.pkl','rb'))
movies = pd.DataFrame(movie_dict)

with gzip.open('similarity.pkl.gz','rb') as f:
    similarity = pickle.load(f)

st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
    'How woul d you like to be contacted?',
    movies['title'].values
)
if st.button('Recommend'):
    name,posters = recommend(selected_movie_name)

    col1,col2,col3,col4,col5 = st.columns(5)
    with col1:
        st.text(name[0])
        st.image(posters[0])
    with col2:
        st.text(name[1])
        st.image(posters[1])
    with col3:
        st.text(name[2])
        st.image(posters[2])

    with col4:
        st.text(name[3])
        st.image(posters[3])

    with col5:
        st.text(name[4])
        st.image(posters[4])


