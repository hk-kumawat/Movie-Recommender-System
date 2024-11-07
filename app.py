import streamlit as st
import pickle
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

# Function to create a session with a retry strategy
def requests_retry_session(
    retries=5,
    backoff_factor=1,
    status_forcelist=(500, 502, 504),
    session=None,
):
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session

# Function to fetch trending movies with error handling
def fetch_trending():
    url = "https://api.themoviedb.org/3/trending/movie/week?api_key=2f5f23da3b0b5b9f71c7a0c83a95cd1b"
    try:
        response = requests_retry_session().get(url)
        response.raise_for_status()
        data = response.json()
        trending = [{"title": item["title"], "poster": "https://image.tmdb.org/t/p/w500/" + item["poster_path"]} for item in data["results"][:5]]
        return trending
    except requests.exceptions.RequestException:
        st.error("Unable to fetch trending movies at the moment. Please try again later.")
        return []

# Function to fetch posters for recommendations with retry and error handling
def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=2f5f23da3b0b5b9f71c7a0c83a95cd1b&language=en-US"
        response = requests_retry_session().get(url)
        if response.status_code == 200:
            data = response.json()
            poster_path = data.get('poster_path')
            if poster_path:
                return f"https://image.tmdb.org/t/p/w500/{poster_path}"
    except requests.exceptions.RequestException:
        return None

# Recommendation function
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    movie_names = []
    movie_posters = []
    
    for i in distances[1:]:
        movie_id = movies.iloc[i[0]].movie_id
        poster = fetch_poster(movie_id)
        if poster:
            movie_posters.append(poster)
            movie_names.append(movies.iloc[i[0]].title)
        if len(movie_posters) == 5:
            break
    
    return movie_names, movie_posters

# Load the movie data and similarity matrix
movies = pickle.load(open("model_files/movie_list.pkl", 'rb'))
similarity = pickle.load(open("model_files/similarity.pkl", 'rb'))
movie_list = movies['title'].values

# Adding a title section
st.markdown("<h1 style='text-align: center; color: #d35400;'>Let’s Find the Perfect Movie that Matches Your Vibe!🎬</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #7f8c8d;'>Just pick a title and let us do the magic ✨</p>", unsafe_allow_html=True)

# Trending movies section
trending_movies = fetch_trending()
st.markdown("<h3 style='color: #d35400; text-align: center;'>🔥 Now Trending</h3>", unsafe_allow_html=True)
cols = st.columns(5)
for i, movie in enumerate(trending_movies):
    with cols[i]:
        st.image(movie["poster"], width=100, caption=movie["title"], use_column_width=True)

# Movie selection box with a custom placeholder
selected_movie = st.selectbox("Enter a movie name 🎥", movie_list)

# Button styling
st.markdown("""
    <style>
    .recommend-btn {
        background-color: #3498db;
        color: white;
        padding: 10px 20px;
        font-size: 18px;
        border-radius: 10px;
        font-weight: bold;
        text-align: center;
        display: inline-block;
        cursor: pointer;
    }
    .recommend-btn:hover {
        background-color: #2980b9;
    }
    </style>
""", unsafe_allow_html=True)

# Recommendation button with spinner and loading message
if st.button("Give Me the Best Movies!🎬"):
    with st.spinner("Please wait a moment as we discover your next favorite movies! 🍿"):
        movie_names, movie_posters = recommend(selected_movie)
    
    # Display recommended movies in columns with titles below posters
    st.markdown("<h3 style='text-align: center; color: #d35400;'>Recommended Movies</h3>", unsafe_allow_html=True)
    cols = st.columns(5)
    for i, col in enumerate(cols):
        with col:
            st.image(movie_posters[i], use_column_width=True)
            st.markdown(f"<p style='text-align: center;'>{movie_names[i]}</p>", unsafe_allow_html=True)

# Footer section
st.markdown("---")  # Horizontal divider
st.markdown(
    "<div style='text-align: center; color: #7f8c8d; font-size: 16px;'>"
    "🍿 | Brought to Life By - Harshal Kumawat | 🎬"
    "</div>",
    unsafe_allow_html=True
)
