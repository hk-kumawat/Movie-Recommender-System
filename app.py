import streamlit as st
import pickle
import requests
from dotenv import load_dotenv
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

# Retrieve the API key from Streamlit secrets
TMDB_API_KEY = st.secrets["tmdb"]["api_key"]

# Configure requests session
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

# Helper functions
def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}"
        response = requests_retry_session().get(url)
        if response.status_code == 200:
            data = response.json()
            return f"https://image.tmdb.org/t/p/w500/{data.get('poster_path', '')}"
    except Exception:
        return None

def fetch_trailer(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}/videos?api_key={TMDB_API_KEY}"
        response = requests_retry_session().get(url)
        if response.status_code == 200:
            for video in response.json().get('results', []):
                if video['type'] == 'Trailer' and video['site'] == 'YouTube':
                    return f"https://youtu.be/{video['key']}"
        return None
    except Exception:
        return None

def get_movie_details(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}"
        response = requests_retry_session().get(url)
        if response.status_code == 200:
            data = response.json()
            return {
                'rating': data.get('vote_average'),
                'release_date': data.get('release_date'),
                'runtime': data.get('runtime'),
                'tagline': data.get('tagline'),
                'director': ', '.join([crew['name'] for crew in data.get('credits', {}).get('crew', []) 
                          if crew['job'] == 'Director'])
            }
    except Exception:
        return None

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    
    recommendations = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        poster = fetch_poster(movie_id)
        if poster:
            recommendations.append({
                'title': movies.iloc[i[0]].title,
                'poster': poster,
                'trailer': fetch_trailer(movie_id)
            })
    return recommendations

def get_random_movie():
    random_movie = movies.sample(1).iloc[0]
    return {
        'title': random_movie['title'],
        'poster': fetch_poster(random_movie['movie_id']),
        'trailer': fetch_trailer(random_movie['movie_id'])
    }

# Load data
movies = pickle.load(open("model_files/movie_list.pkl", 'rb'))
similarity = pickle.load(open("model_files/similarity.pkl", 'rb'))

# UI Configuration
st.set_page_config(page_title="Movie Recommender", layout="wide")

# Header Section
st.markdown("""
    <h1 style='text-align: center; color: #FF4B4B; padding: 20px;'>
        🍿 Movie Magic Recommender
    </h1>
    <p style='text-align: center; color: #666; font-size: 1.1rem;'>
        Discover your next favorite movie! 🎬
    </p>
""", unsafe_allow_html=True)

# Main Layout
col1, col2 = st.columns([3, 1])

with col1:
    selected_movie = st.selectbox("Search for a movie:", movies['title'].values, 
                                help="Start typing to find movies")

with col2:
    if st.button("Surprise Me! 🎲", use_container_width=True):
        st.session_state.random_movie = get_random_movie()

# Selected Movie Details
if selected_movie:
    movie_id = movies[movies['title'] == selected_movie].iloc[0].movie_id
    details = get_movie_details(movie_id)
    trailer_url = fetch_trailer(movie_id)
    
    st.markdown("---")
    st.subheader(f"About {selected_movie}")
    
    if details:
        cols = st.columns([2, 3])
        with cols[0]:
            if poster := fetch_poster(movie_id):
                st.image(poster, use_container_width=True)
        
        with cols[1]:
            st.markdown(f"**📅 Release Year:** {details['release_date'][:4] if details['release_date'] else 'N/A'}") 
            st.markdown(f"**⭐ Rating:** {details['rating']}/10" if details['rating'] else '**⭐ Rating:** N/A')
            st.markdown(f"**⏱ Runtime:** {details['runtime']} mins" if details['runtime'] else '**⏱ Runtime:** N/A')
            st.markdown(f"**🎬 Director:** {details['director']}" if details['director'] else '**🎬 Director:** N/A')
            
            if details['tagline']:
                st.markdown(f"*\"{details['tagline']}\"*")
            
            if trailer_url:
                st.video(trailer_url)

# Random Movie Section
if 'random_movie' in st.session_state:
    st.markdown("---")
    st.subheader("🎉 Your Random Pick!")
    
    cols = st.columns([2, 3])
    with cols[0]:
        if st.session_state.random_movie['poster']:
            st.image(st.session_state.random_movie['poster'], use_container_width=True)
    
    with cols[1]:
        st.markdown(f"## {st.session_state.random_movie['title']}")
        if st.button("Try Another Random Movie"):
            st.session_state.random_movie = get_random_movie()
            st.experimental_rerun()
        
        if st.session_state.random_movie['trailer']:
            st.video(st.session_state.random_movie['trailer'])

# Recommendations Section
if st.button("Get Recommendations 🚀", type="primary"):
    with st.spinner("Finding perfect matches..."):
        recommendations = recommend(selected_movie)
    
    st.markdown("---")
    st.subheader("Recommended Movies")
    
    cols = st.columns(5)
    for idx, movie in enumerate(recommendations):
        with cols[idx % 5]:
            st.image(movie['poster'], caption=movie['title'], use_container_width=True)
            if movie['trailer']:
                st.video(movie['trailer'])

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #666; padding: 20px;'>
        Made with ❤️ by Harshal Kumawat | 
        <a href="https://www.themoviedb.org/" target="_blank">Powered by TMDB</a>
    </div>
""", unsafe_allow_html=True)