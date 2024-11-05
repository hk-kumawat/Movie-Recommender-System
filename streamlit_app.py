import pandas as pd
import numpy as np
import streamlit as st
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
import requests
import zipfile
from io import BytesIO
import time


# Load the data files
movies = pd.read_csv('Dataset/ml-1m/movies.dat', sep='::', names=['movie_id', 'title', 'genres'], engine='python', encoding='latin-1')
ratings = pd.read_csv('Dataset/ml-1m/ratings.dat', sep='::', names=['user_id', 'movie_id', 'rating', 'timestamp'], engine='python', encoding='latin-1')

# Merge movies and ratings
movie_ratings = pd.merge(ratings, movies, on='movie_id')

# User-item matrix for collaborative filtering
user_movie_matrix = movie_ratings.pivot_table(index='user_id', columns='title', values='rating').fillna(0)

# Genre-based matrix
count_vectorizer = CountVectorizer(tokenizer=lambda x: x.split('|'), token_pattern=None)
genre_matrix = count_vectorizer.fit_transform(movies['genres'])
genre_sim_matrix = cosine_similarity(genre_matrix)
genre_sim_df = pd.DataFrame(genre_sim_matrix, index=movies['title'], columns=movies['title'])

# User-based collaborative filtering similarity
user_sim_matrix = cosine_similarity(user_movie_matrix)
user_sim_df = pd.DataFrame(user_sim_matrix, index=user_movie_matrix.index, columns=user_movie_matrix.index)

# Weighted combination of user-based, item-based, and genre-based similarities
combined_sim_df = 0.4 * user_sim_df.add(0.6 * genre_sim_df, fill_value=0)

# Helper function for case-insensitive, partial matching of movie titles
def find_closest_title(input_title):
    lower_titles = movies['title'].str.lower()
    matches = movies[lower_titles.str.contains(input_title.lower(), na=False)]
    if not matches.empty:
        return matches.iloc[0]['title']  # Return the closest match found
    else:
        return None

# Helper function to filter movies by genre
def get_genres(movie_title):
    genres = movies[movies['title'] == movie_title]['genres']
    if not genres.empty:
        return genres.values[0].split('|')
    return []

# Recommendation function
def recommend_movies(movie_title, num_recommendations=5):
    exact_title = find_closest_title(movie_title)
    if not exact_title:
        return f"Movie '{movie_title}' not found in dataset. Please try another title."

    input_genres = get_genres(exact_title)
    num_recommendations = min(num_recommendations, 10)

    similar_movies = combined_sim_df[exact_title].sort_values(ascending=False)

    genre_filtered = similar_movies.index[similar_movies.index.isin(movies[movies['genres'].apply(lambda g: any(genre in g for genre in input_genres))]['title'])]
    recommended_movies = similar_movies.loc[genre_filtered].drop(exact_title).head(num_recommendations)

    recommendations = pd.DataFrame({
        'Rank': range(1, len(recommended_movies) + 1),
        'Recommended Movie': recommended_movies.index    })

    return recommendations

# Streamlit UI with Splash Screen
st.set_page_config(page_title="Movie Recommendation System", page_icon="🎬", layout="centered")

# Display splash screen at the start
if "splash_shown" not in st.session_state:
    st.session_state.splash_shown = True
    st.markdown("<h1 style='text-align: center; color: #FF5733;'>Welcome to the Movie Recommendation System 🎬</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #2ECC71;'>Loading recommendations just for you... sit tight! 🍿</p>", unsafe_allow_html=True)
    time.sleep(2)  # Pause for 2 seconds to simulate a splash screen

# Main UI
st.title('Movie Recommendation System')
movie_title = st.text_input("Enter a movie title:")
num_recommendations = st.number_input("Enter the number of recommendations (max 10):", min_value=1, max_value=10, value=5)

if st.button('Recommend'):
    with st.spinner('Fetching your recommendations... please wait a moment! 🎬🍿'):
        time.sleep(1)  # Optional: Simulate loading time
        recommendations = recommend_movies(movie_title, num_recommendations)
        
        if isinstance(recommendations, pd.DataFrame):
            st.write(f"Recommendations for '{movie_title}':")
            st.dataframe(recommendations.style.set_properties(**{'text-align': 'center'}))
        else:
            st.write(recommendations)
