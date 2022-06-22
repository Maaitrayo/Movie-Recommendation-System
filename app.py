import streamlit as st
import pickle
import pandas as pd
import requests

similarity = pickle.load(open('similarity.pkl', 'rb'))
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies =pd.DataFrame(movies_dict)

st.title('Movie Recommender System' )

selected_movie_name = st.selectbox(
    'How would you like to be contacted?',
    movies['title'].values)

def fetch_poster(movie_id):
    responce =  requests.get('https://api.themoviedb.org/3/movie/{}?api_key=02d7209ba2a475c09a28c826603f3432&language=en-US'.format(movie_id))
    data = responce.json()
    # st.text(data)
    return 'https://image.tmdb.org/t/p/w500/'+data['poster_path']

def recommend(movie):
    movie_index = movies[movies.title == movie].index[0]
    distance = similarity[movie_index]
    movies_list = sorted(list(enumerate(distance)), reverse = True, key=lambda x:x[1])[1:7]
    
    recommended_movies = []
    recommended_movies_poster = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_poster.append(fetch_poster(movie_id))
    
    return recommended_movies, recommended_movies_poster


if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)

    col1, col2, col3, col4, col5, col6 = st.columns(6)
    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])
    with col6:
        st.text(names[5])
        st.image(posters[5])
    

