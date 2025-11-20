<a id="readme-top"></a>

<div align="center">

# 🎬 Movie Recommender System

### AI-Powered Content-Based Movie Recommendation Engine

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=flat&logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

[Live Demo](https://findmynextflick.streamlit.app/#7c707207) • [Report Bug](https://github.com/hk-kumawat/Movie-Recommender-System/issues) • [Request Feature](https://github.com/hk-kumawat/Movie-Recommender-System/issues)

![Movie Recommender Banner](https://github.com/user-attachments/assets/c83f35ad-8079-4a51-831f-0b44714d9a75)

</div>

---

## 📖 Overview

A **content-based movie recommendation system** that suggests films based on similarity in genres, keywords, cast, crew, and plot. Built with Streamlit and powered by machine learning, it provides personalized recommendations with rich metadata from TMDB API.

### Key Highlights

- 🎯 **Content-Based Filtering** using NLP and cosine similarity
- 🔴 **Real-Time Data** from TMDB API (posters, trailers, cast, ratings)
- ⚡ **Fast Recommendations** with pre-computed similarity matrix
- 📊 **4,800+ Movies** in the catalog
- 🎨 **Interactive UI** with trending movies, random suggestions, and viewing history

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| **Movie Search** | Search from 4,800+ movies and get instant recommendations |
| **Surprise Me** | Random movie discovery with full details |
| **Trending Movies** | Weekly trending films from TMDB |
| **Rich Metadata** | Cast, crew, budget, revenue, ratings, runtime, trailers |
| **Viewing History** | Track and revisit recently viewed movies |
| **Responsive Design** | Mobile-friendly interface |

<div align="center">
  <img src="https://github.com/user-attachments/assets/542691f2-474d-46c3-a7ce-3ffebd697dbe" alt="App Demo" width="700">
</div>

---

## 🏗️ Architecture

### System Overview

```
┌─────────────────┐
│   User Input    │
│  (Movie Title)  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Streamlit App  │
│   (Frontend)    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Recommender    │
│    Engine       │
│ (Cosine Sim.)   │
└────────┬────────┘
         │
         ├───────────────┬───────────────┐
         ▼               ▼               ▼
┌──────────────┐  ┌──────────┐  ┌──────────────┐
│ Similarity   │  │ TMDB API │  │ Local Cache  │
│ Matrix (pkl) │  │ (Live)   │  │ (Session)    │
└──────────────┘  └──────────┘  └──────────────┘
```

### Recommendation Algorithm

1. **Text Vectorization**: Convert movie features (genres, keywords, cast, crew, overview) into vectors using CountVectorizer (5000 features)
2. **Similarity Computation**: Calculate cosine similarity between all movie pairs (4806 × 4806 matrix)
3. **Recommendation**: For a given movie, retrieve top 5 most similar movies based on cosine similarity scores

**Cosine Similarity Formula:**
```
similarity(A, B) = (A · B) / (||A|| × ||B||)
```

---

## 🔧 Tech Stack

<div align="center">

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)

</div>

### Core Dependencies

| Category | Technologies |
|----------|-------------|
| **Framework** | Streamlit |
| **ML/NLP** | scikit-learn, NLTK (PorterStemmer) |
| **Data Processing** | Pandas, NumPy, Pickle |
| **API** | TMDB API, Requests |
| **Deployment** | Streamlit Cloud |

---

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/hk-kumawat/Movie-Recommender-System.git
cd Movie-Recommender-System

# Install dependencies
pip install -r requirements.txt

# Set up TMDB API key (see below)
mkdir .streamlit
echo '[tmdb]\napi_key = "YOUR_API_KEY"' > .streamlit/secrets.toml

# Run the application
streamlit run app.py
```

**Access the app at:** `http://localhost:8501`

---

## ⚙️ Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager
- TMDB API key ([Get one here](https://www.themoviedb.org/settings/api))

### Step-by-Step Setup

**1. Clone the Repository**
```bash
git clone https://github.com/hk-kumawat/Movie-Recommender-System.git
cd Movie-Recommender-System
```

**2. Create Virtual Environment** (Recommended)
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

**3. Install Dependencies**
```bash
pip install -r requirements.txt
```

**4. Configure TMDB API Key**

Create `.streamlit/secrets.toml`:
```toml
[tmdb]
api_key = "your_tmdb_api_key_here"
```

**How to get TMDB API Key:**
1. Sign up at [themoviedb.org](https://www.themoviedb.org/)
2. Go to Settings → API
3. Request API Key (select "Developer")
4. Copy your API key

**5. Run the Application**
```bash
streamlit run app.py
```

### Troubleshooting

| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` |
| API Key Error | Check `.streamlit/secrets.toml` format |
| Port Already in Use | Use `streamlit run app.py --server.port 8502` |
| NLTK Data Missing | Run `python -m nltk.downloader punkt stopwords` |

---

## 📊 Dataset

**Source:** [TMDb 5000 Movie Dataset](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata) (Kaggle)

### Dataset Details

| File | Records | Description |
|------|---------|-------------|
| `tmdb_5000_movies.csv` | 4,803 | Movie metadata (title, overview, genres, keywords, budget, revenue) |
| `tmdb_5000_credits.csv` | 4,803 | Cast and crew information |

**Key Statistics:**
- **Movies:** 4,806 (after preprocessing)
- **Features:** 5,000 (CountVectorizer)
- **Genres:** 20 unique genres
- **Time Period:** 1916-2017

### Data Processing Pipeline

```
Raw Data
    ↓
Merge movies + credits
    ↓
Extract features (genres, keywords, cast, crew, overview)
    ↓
Text preprocessing (lowercase, remove spaces)
    ↓
Stemming (PorterStemmer)
    ↓
Combine into "tags" column
    ↓
Vectorize (CountVectorizer, max_features=5000)
    ↓
Compute cosine similarity matrix (4806 × 4806)
    ↓
Save model (movie_list.pkl, similarity.pkl)
```

---

## 📁 Project Structure

```
Movie-Recommender-System/
│
├── app.py                          # Main Streamlit application
├── Movie Recommender System.ipynb  # Data preprocessing & model training
├── requirements.txt                # Python dependencies
├── .gitignore                      # Git ignore rules
├── LICENSE                         # MIT License
│
├── Dataset/                        # Raw movie data
│   ├── tmdb_5000_movies.csv
│   └── tmdb_5000_credits.csv
│
├── model_files/                    # Trained models
│   ├── movie_list.pkl             # Movie data (4806 movies)
│   └── similarity.pkl             # Cosine similarity matrix (4806×4806)
│
└── .streamlit/                     # Configuration (not in repo)
    └── secrets.toml               # TMDB API key
```

---

## 📈 Performance

### Model Metrics

| Metric | Value |
|--------|-------|
| **Movies in Catalog** | 4,806 |
| **Feature Dimensions** | 5,000 |
| **Similarity Matrix Size** | 4,806 × 4,806 |
| **Average Recommendation Time** | <2 seconds |
| **Model Size** | 184 MB (similarity.pkl) |

### System Performance

- **API Response Time:** ~1.2s (TMDB)
- **Recommendation Generation:** ~0.8s
- **Memory Usage:** ~500MB
- **Concurrent Users:** 100+

---

## 🎯 How to Use

### Web Application

1. **Search Mode:** Select a movie from the dropdown and click "Show Details & Recommendations"
2. **Surprise Mode:** Click "Surprise Me!" for a random movie suggestion
3. **Trending:** View weekly trending movies at the top
4. **History:** Access recently viewed movies from the sidebar

### API Integration

```python
import pickle
import pandas as pd

# Load models
movies = pickle.load(open('model_files/movie_list.pkl', 'rb'))
similarity = pickle.load(open('model_files/similarity.pkl', 'rb'))

# Get recommendations
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommendations = []
    for i in distances[1:6]:
        recommendations.append(movies.iloc[i[0]].title)
    return recommendations

# Example
print(recommend('Avatar'))
# Output: ['Guardians of the Galaxy', 'Star Wars', 'Star Trek', ...]
```

---

## 🤝 Contributing

Contributions are welcome! Here's how:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/YourFeature`)
3. Commit changes (`git commit -m 'Add YourFeature'`)
4. Push to branch (`git push origin feature/YourFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## 📧 Contact

**Harshal Kumawat**

[![GitHub](https://img.shields.io/badge/GitHub-181717?style=flat&logo=github)](https://github.com/hk-kumawat)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=flat&logo=linkedin)](https://www.linkedin.com/in/harshal-kumawat/)
[![Email](https://img.shields.io/badge/Email-D14836?style=flat&logo=gmail&logoColor=white)](mailto:harshalkumawat100@gmail.com)

**Project Link:** [github.com/hk-kumawat/Movie-Recommender-System](https://github.com/hk-kumawat/Movie-Recommender-System)

---

<div align="center">

### ⭐ Star this repository if you found it helpful!

**Made with ❤️ by Harshal Kumawat**


<p align="right">
  <a href="#readme-top">⬆️ Back to top</a>
</p>


</div>

