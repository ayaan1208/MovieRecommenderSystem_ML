import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    api_key = "3dab35ccb173856c815ac2ee46adaa01"
    base_url = "https://api.themoviedb.org/3/movie/{}?api_key={}&language=en-US".format(movie_id, api_key)
    
    try:
        response = requests.get(url=base_url)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        data = response.json()
        poster_path = data.get('poster_path')
        if poster_path:
            full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
            return full_path
        else:
            st.warning("No poster available for this movie.")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching movie details: {e}")
        return None

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        poster = fetch_poster(movie_id)
        if poster:
            recommended_movies_posters.append(poster)

    return recommended_movies, recommended_movies_posters

# Load data and similarity matrix
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Streamlit app
st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
    'Select a movie:',
    movies['title'].values)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)
    
    # Create columns for display
    col1, col2, col3, col4, col5 = st.columns(5)
    
    # Display recommended movies and posters
    with col1:
        st.text(names[0])
        st.image(posters[0], caption=names[0], use_column_width=True)
    
    with col2:
        st.text(names[1])
        st.image(posters[1], caption=names[1], use_column_width=True)

    with col3:
        st.text(names[2])
        st.image(posters[2], caption=names[2], use_column_width=True)

    with col4:
        st.text(names[3])
        st.image(posters[3], caption=names[3], use_column_width=True)

    with col5:
        st.text(names[4])
        st.image(posters[4], caption=names[4], use_column_width=True)
