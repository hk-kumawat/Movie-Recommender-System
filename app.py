import streamlit as st
import pickle
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

# ------------------------------
# Session State Initialization
# ------------------------------
if "history" not in st.session_state:
    st.session_state.history = []    # Stores movie_id of recently viewed movies
if "mode" not in st.session_state:
    st.session_state.mode = None
if "selected_movie" not in st.session_state:
    st.session_state.selected_movie = None
if "random_movie" not in st.session_state:
    st.session_state.random_movie = None

# ------------------------------
# TMDB API and Helper Functions
# ------------------------------
TMDB_API_KEY = st.secrets["tmdb"]["api_key"]

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
            genres = ", ".join([g["name"] for g in data.get("genres", [])]) if data.get("genres") else "N/A"
            budget = f"${data.get('budget', 0):,}" if data.get("budget", 0) > 0 else "N/A"
            revenue = f"${data.get('revenue', 0):,}" if data.get("revenue", 0) > 0 else "N/A"
            available_in = ", ".join([lang["english_name"] for lang in data.get("spoken_languages", [])]) if data.get("spoken_languages") else "N/A"
            return {
                "rating": data.get("vote_average"),
                "vote_count": data.get("vote_count"),
                "release_date": data.get("release_date"),
                "runtime": data.get("runtime"),
                "tagline": data.get("tagline"),
                "overview": data.get("overview"),
                "director": ", ".join(directors) if directors else "N/A",
                "cast": cast_details,
                "genres": genres,
                "budget": budget,
                "revenue": revenue,
                "available_in": available_in,
            }
    except Exception as e:
        print(e)
    return None

def recommend(movie):
    index = movies[movies["title"] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommendations = []
    # Take the next 5 most similar movies
    for i in distances[1:6]:
        rec_movie_id = movies.iloc[i[0]].movie_id
        poster = fetch_poster(rec_movie_id)
        if poster:
            recommendations.append({
                "title": movies.iloc[i[0]].title,
                "poster": poster,
                "trailer": fetch_trailer(rec_movie_id)
            })
    return recommendations

def get_random_movie():
    random_movie = movies.sample(1).iloc[0]
    return {
        "title": random_movie["title"],
        "poster": fetch_poster(random_movie["movie_id"]),
        "trailer": fetch_trailer(random_movie["movie_id"]),
        "movie_id": random_movie["movie_id"]
    }

def update_history(movie_id):
    # Add the movie to recently viewed if it's not the same as the last viewed
    if not st.session_state.history or st.session_state.history[-1] != movie_id:
        st.session_state.history.append(movie_id)
        if len(st.session_state.history) > 5:
            st.session_state.history.pop(0)

# ------------------------------
# Load Data
# ------------------------------
movies = pickle.load(open("model_files/movie_list.pkl", "rb"))
similarity = pickle.load(open("model_files/similarity.pkl", "rb"))

# ------------------------------
# UI Configuration and Header
# ------------------------------
st.set_page_config(page_title="Movie Recommender", layout="wide")
st.markdown("""
    <h1 style='text-align: center; color: #FF4B4B; margin-bottom: 0.5em;'>
        🍿 Movie Magic Recommender
    </h1>
    <p style='text-align: center; color: #555; font-size: 1.2rem; margin-top: 0;'>
        Discover your next favorite movie! 🎬
    </p>
    <hr style="border:1px solid #eee">
""", unsafe_allow_html=True)

# ------------------------------
# Main Selection Section
# ------------------------------
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

# ------------------------------
# Content Section: Movie Details & Recommendations
# ------------------------------
if "mode" in st.session_state and st.session_state.mode:
    if st.session_state.mode == "search":
        movie_title = st.session_state.selected_movie
        movie_row = movies[movies["title"] == movie_title].iloc[0]
        movie_id = movie_row.movie_id
        update_history(movie_id)
        details = get_movie_details(movie_id)
        trailer_url = fetch_trailer(movie_id)

        st.markdown("<hr>", unsafe_allow_html=True)
        st.subheader(f"🎬 Details for: {movie_title}")

        # Display poster and details side-by-side
        detail_col_left, detail_col_right = st.columns([1, 2])
        with detail_col_left:
            poster = fetch_poster(movie_id)
            if poster:
                st.image(poster, use_container_width=True)
        with detail_col_right:
            st.markdown("### Movie Details")
            # Organize details into two columns: Main details and Additional details
            col_details_1, col_details_2 = st.columns(2)
            with col_details_1:
                st.markdown(f"**Release Date:** {details['release_date'] or 'N/A'}")
                st.markdown(f"**Directed by:** {details['director']}")
                st.markdown(f"**Genres:** {details['genres']}")
            with col_details_2:
                st.markdown(f"Budget: {details['budget']}")
                st.markdown(f"Revenue: {details['revenue']}")
                st.markdown(f"Available in: {details['available_in']}")
            if details["tagline"]:
                st.info(details["tagline"])
            st.markdown("**Overview:**")
            st.write(details["overview"])

            # Display rating and runtime in columns
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Rating:** {details['rating']} / 10 ({details['vote_count']} votes)" if details["rating"] else "**Rating:** N/A")
            with col2:
                st.markdown(f"**Runtime:** {details['runtime']} mins" if details["runtime"] else "**Runtime:** N/A")

            # Display top cast members
            if details["cast"]:
                st.markdown("**Cast:**")
                cast_cols = st.columns(len(details["cast"]))
                for idx, actor in enumerate(details["cast"]):
                    with cast_cols[idx]:
                        if actor["profile"]:
                            st.image(actor["profile"], use_container_width=True)
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
                st.image(rec["poster"], use_container_width=True)
                st.markdown(f"**{rec['title']}**")
                if rec["trailer"]:
                    with st.expander("Trailer"):
                        st.video(rec["trailer"])
                        
    elif st.session_state.mode == "surprise":
        random_data = st.session_state.random_movie
        movie_title = random_data["title"]
        movie_id = random_data.get("movie_id")
        if not movie_id:
            movie_row = movies[movies["title"] == movie_title].iloc[0]
            movie_id = movie_row.movie_id
        update_history(movie_id)
        details = get_movie_details(movie_id)
        trailer_url = fetch_trailer(movie_id)

        st.markdown("<hr>", unsafe_allow_html=True)
        st.subheader(f"🎉 Your Surprise Movie: {movie_title}")

        detail_col_left, detail_col_right = st.columns([1, 2])
        with detail_col_left:
            poster = fetch_poster(movie_id)
            if poster:
                st.image(poster, use_container_width=True)
        with detail_col_right:
            st.markdown("### Movie Details")
            col_details_1, col_details_2 = st.columns(2)
            with col_details_1:
                st.markdown(f"**Release Date:** {details['release_date'] or 'N/A'}")
                st.markdown(f"**Directed by:** {details['director']}")
                st.markdown(f"**Genres:** {details['genres']}")
            with col_details_2:
                st.markdown(f"Budget: {details['budget']}")
                st.markdown(f"Revenue: {details['revenue']}")
                st.markdown(f"Available in: {details['available_in']}")
            if details["tagline"]:
                st.info(details["tagline"])
            st.markdown("**Overview:**")
            st.write(details["overview"])

            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Rating:** {details['rating']} / 10 ({details['vote_count']} votes)" if details["rating"] else "**Rating:** N/A")
            with col2:
                st.markdown(f"**Runtime:** {details['runtime']} mins" if details["runtime"] else "**Runtime:** N/A")

            if details["cast"]:
                st.markdown("**Cast:**")
                cast_cols = st.columns(len(details["cast"]))
                for idx, actor in enumerate(details["cast"]):
                    with cast_cols[idx]:
                        if actor["profile"]:
                            st.image(actor["profile"], use_container_width=True)
                        st.caption(f"{actor['name']} as {actor['character']}")
                        
            if trailer_url:
                with st.expander("Watch Trailer"):
                    st.video(trailer_url)

# ------------------------------
# Sidebar: Recently Viewed (rendered at the end so it reflects the updated history)
# ------------------------------
with st.sidebar:
    st.header("🕒 Recently Viewed")
    if st.session_state.history:
        # Show most recent first
        for hist_id in reversed(st.session_state.history):
            movie_row = movies[movies["movie_id"] == hist_id].iloc[0]
            hist_title = movie_row["title"]
            hist_poster = fetch_poster(hist_id)
            if hist_poster:
                st.image(hist_poster, width=100)
            if st.button(hist_title, key=f"hist_button_{hist_id}"):
                st.session_state.mode = "search"
                st.session_state.selected_movie = hist_title
    else:
        st.write("No history yet.")

# ------------------------------
# Footer
# ------------------------------
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("""
    <div style='text-align: center; color: #888; padding: 10px; font-size: 0.9rem;'>
        Made with ❤️ by Harshal Kumawat
    </div>
""", unsafe_allow_html=True)
