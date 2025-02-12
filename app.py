import streamlit as st
import pickle
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

# Retrieve the API key from Streamlit secrets
TMDB_API_KEY = st.secrets["tmdb"]["api_key"]

# Configure a requests session with retries
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
            poster_path = data.get("poster_path")
            if poster_path:
                return f"https://image.tmdb.org/t/p/w500{poster_path}"
    except Exception as e:
        print(e)
    return None

def fetch_trailer(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}/videos?api_key={TMDB_API_KEY}"
        response = requests_retry_session().get(url)
        if response.status_code == 200:
            for video in response.json().get("results", []):
                if video.get("type") == "Trailer" and video.get("site") == "YouTube":
                    return f"https://youtu.be/{video['key']}"
    except Exception as e:
        print(e)
    return None

# Get enriched movie details by appending credits and videos
def get_movie_details(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}&append_to_response=credits,videos"
        response = requests_retry_session().get(url)
        if response.status_code == 200:
            data = response.json()
            # Directors
            directors = [
                crew["name"]
                for crew in data.get("credits", {}).get("crew", [])
                if crew.get("job") == "Director"
            ]
            # Cast (top 5)
            cast = data.get("credits", {}).get("cast", [])[:5]
            cast_details = []
            for actor in cast:
                cast_details.append({
                    "name": actor.get("name"),
                    "character": actor.get("character"),
                    "profile": f"https://image.tmdb.org/t/p/w500{actor['profile_path']}" if actor.get("profile_path") else None
                })
            return {
                "rating": data.get("vote_average"),
                "vote_count": data.get("vote_count"),
                "release_date": data.get("release_date"),
                "runtime": data.get("runtime"),
                "tagline": data.get("tagline"),
                "overview": data.get("overview"),
                "director": ", ".join(directors) if directors else None,
                "cast": cast_details
            }
    except Exception as e:
        print(e)
    return None

# Recommendation based on similarity
def recommend(movie):
    index = movies[movies["title"] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    
    recommendations = []
    # Take next 5 most similar movies
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        poster = fetch_poster(movie_id)
        if poster:
            recommendations.append({
                "title": movies.iloc[i[0]].title,
                "poster": poster,
                "trailer": fetch_trailer(movie_id)
            })
    return recommendations

def get_random_movie():
    random_movie = movies.sample(1).iloc[0]
    return {
        "title": random_movie["title"],
        "poster": fetch_poster(random_movie["movie_id"]),
        "trailer": fetch_trailer(random_movie["movie_id"])
    }

# Load data
movies = pickle.load(open("model_files/movie_list.pkl", "rb"))
similarity = pickle.load(open("model_files/similarity.pkl", "rb"))

# UI Configuration
st.set_page_config(page_title="Movie Recommender", layout="wide")

# Header Section
st.markdown("""
    <h1 style='text-align: center; color: #FF4B4B; padding: 10px 0 0 0;'>
        🍿 Movie Magic Recommender
    </h1>
    <p style='text-align: center; color: #555; font-size: 1.2rem;'>
        Discover your next favorite movie! 🎬
    </p>
    <hr style="border:1px solid #eee">
""", unsafe_allow_html=True)

# --- Main Selection Section ---
# Two columns: left for search; right for surprise.
col_search, col_surprise = st.columns([3, 2])

with col_search:
    st.subheader("🔍 Search for a Movie")
    selected_movie = st.selectbox("Type to search...", movies["title"].values, key="select_movie", help="Start typing to find your movie")
    if st.button("Show Details & Recommendations", key="show_details"):
        st.session_state.mode = "search"
        st.session_state.selected_movie = selected_movie

with col_surprise:
    st.subheader("🎲 Feeling Adventurous?")
    if st.button("Surprise Me!", key="surprise_me"):
        st.session_state.mode = "surprise"
        st.session_state.random_movie = get_random_movie()

st.markdown("<br>", unsafe_allow_html=True)

# --- Content Section ---
if "mode" in st.session_state:
    if st.session_state.mode == "search":
        movie_title = st.session_state.selected_movie
        movie_id = movies[movies["title"] == movie_title].iloc[0].movie_id
        details = get_movie_details(movie_id)
        trailer_url = fetch_trailer(movie_id)

        st.markdown("<hr>", unsafe_allow_html=True)
        st.subheader(f"🎬 Details for: {movie_title}")

        # Display Movie Details
        detail_col_left, detail_col_right = st.columns([1, 2])
        with detail_col_left:
            poster = fetch_poster(movie_id)
            if poster:
                st.image(poster, use_column_width=True)
        with detail_col_right:
            st.markdown(f"**Release Date:** {details['release_date'] or 'N/A'}")
            st.markdown(f"**Rating:** {details['rating']} / 10 ({details['vote_count']} votes)" if details['rating'] else "**Rating:** N/A")
            st.markdown(f"**Runtime:** {details['runtime']} mins" if details['runtime'] else "**Runtime:** N/A")
            st.markdown(f"**Director:** {details['director'] or 'N/A'}")
            if details['tagline']:
                st.info(f"_{details['tagline']}_")
            st.markdown("**Overview:**")
            st.write(details['overview'] or "No overview available.")

            # Display top cast members
            if details['cast']:
                st.markdown("**Cast:**")
                cast_cols = st.columns(len(details['cast']))
                for idx, actor in enumerate(details['cast']):
                    with cast_cols[idx]:
                        if actor['profile']:
                            st.image(actor['profile'], use_column_width=True)
                        st.caption(f"{actor['name']} as {actor['character']}")
                        
            if trailer_url:
                with st.expander("Watch Trailer"):
                    st.video(trailer_url)

        # Display Recommendations
        with st.spinner("Fetching Recommendations..."):
            recommendations = recommend(movie_title)
        st.markdown("<hr>", unsafe_allow_html=True)
        st.subheader("🚀 Recommended Movies")
        rec_cols = st.columns(3)
        for idx, rec in enumerate(recommendations):
            with rec_cols[idx % 3]:
                st.image(rec['poster'], use_column_width=True)
                st.markdown(f"**{rec['title']}**")
                if rec['trailer']:
                    with st.expander("Trailer"):
                        st.video(rec['trailer'])
                        
    elif st.session_state.mode == "surprise":
        # Place the "Show Another Surprise Movie" button at the top
        if st.button("Show Another Surprise Movie", key="another_surprise"):
            st.session_state.random_movie = get_random_movie()
        
        random_data = st.session_state.random_movie
        movie_title = random_data["title"]
        movie_id = movies[movies["title"] == movie_title].iloc[0].movie_id
        details = get_movie_details(movie_id)
        trailer_url = fetch_trailer(movie_id)

        st.markdown("<hr>", unsafe_allow_html=True)
        st.subheader(f"🎉 Your Surprise Movie: {movie_title}")

        detail_col_left, detail_col_right = st.columns([1, 2])
        with detail_col_left:
            poster = fetch_poster(movie_id)
            if poster:
                st.image(poster, use_column_width=True)
        with detail_col_right:
            st.markdown(f"**Release Date:** {details['release_date'] or 'N/A'}")
            st.markdown(f"**Rating:** {details['rating']} / 10 ({details['vote_count']} votes)" if details['rating'] else "**Rating:** N/A")
            st.markdown(f"**Runtime:** {details['runtime']} mins" if details['runtime'] else "**Runtime:** N/A")
            st.markdown(f"**Director:** {details['director'] or 'N/A'}")
            if details['tagline']:
                st.info(f"_{details['tagline']}_")
            st.markdown("**Overview:**")
            st.write(details['overview'] or "No overview available.")

            if details['cast']:
                st.markdown("**Cast:**")
                cast_cols = st.columns(len(details['cast']))
                for idx, actor in enumerate(details['cast']):
                    with cast_cols[idx]:
                        if actor['profile']:
                            st.image(actor['profile'], use_column_width=True)
                        st.caption(f"{actor['name']} as {actor['character']}")
                        
            if trailer_url:
                with st.expander("Watch Trailer"):
                    st.video(trailer_url)

# --- Footer ---
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("""
    <div style='text-align: center; color: #888; padding: 10px; font-size: 0.9rem;'>
        Made with ❤️ by Harshal Kumawat
    </div>
""", unsafe_allow_html=True)
