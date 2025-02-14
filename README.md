<a id="readme-top"></a>

# 🎬 Movie Recommender System 📽️

![Movie Recommender System Banner](https://github.com/user-attachments/assets/c83f35ad-8079-4a51-831f-0b44714d9a75)

<br> 

## Overview

This project is a movie recommender system built using **Streamlit**. It lets users search for their favorite movies or get a **"Surprise Me"** suggestion. The app fetches live movie details—like posters, trailers, ratings, cast, and more—using the **TMDB API**. It also displays trending movies and tracks your recently viewed films. Simply put, it helps you discover movies that match your taste through an easy-to-use, interactive interface.

<br> 

## Live Demo

Try out the Movie Recommender System! 👉🏻 [![Experience It! 🌟](https://img.shields.io/badge/Experience%20It!-blue)](https://findmynextflick.streamlit.app/#7c707207)

<br>

_Below is a preview of the Movie Recommender System in action. Enter a movie name to see similar movie suggestions! 👇🏻_

<p align="center">
  <img src="https://github.com/user-attachments/assets/542691f2-474d-46c3-a7ce-3ffebd697dbe" alt="Movie Recommender in action">
</p>

<br> 

## Learning Journey 🗺️

I built this project out of a love for movies and a desire to dive into machine learning in a practical way. Here’s a glimpse into my journey:

- **Inspiration:**  
  I’ve always been passionate about movies, and I wanted to create something that not only recommends films but also tells a story through data. Merging my interests in cinema and technology felt like the perfect creative outlet.

- **Why I Made It:**  
  I set out to design a system that could give personalized movie suggestions by leveraging real-time data and machine learning. I also wanted to experiment with deep learning using the MNIST dataset to sharpen my skills and explore new techniques.

- **Challenges Faced:**  
  - **API Key Integration:** One major challenge was choosing the right API for movie data. I had a better IMDb option available, but due to licensing and cost constraints, I opted to use TMDB. Integrating TMDB’s API and managing its rate limits pushed me to learn more about API integration and error handling.  
  - **Balancing Complexity & Usability:** I had to find the right balance between a robust, feature-rich system and a clean, user-friendly interface.  
  - **Model Tuning:** Fine-tuning the deep learning model to achieve high accuracy involved a lot of trial and error, pushing me to learn more about early stopping and data augmentation techniques.

- **What I Learned:**  
  - **API Integration:** Seamlessly connecting with external APIs (like TMDB) to fetch live movie data.  
  - **Web Development:** Building an interactive and user-friendly interface with Streamlit.  
  - **Deep Learning:** Hands-on experience in constructing, training, and optimizing a CNN with TensorFlow and Keras.  
  - **Data Handling:** Mastering data preprocessing and visualization to simplify complex concepts.

- **The Value It Adds:**  
  This project isn’t just a technical exercise—it’s a story of blending creativity with technology. It deepened my understanding of real-world problem-solving through machine learning and continues to inspire me to explore, learn, and share knowledge.

Every step of this journey has enriched my skills and reinforced my belief that learning is best when it’s fun, creative, and shared.

<br> 

## Table of Contents

1.  [Features](#features)
2.  [Installation](#installation)    
3.  [Usage](#usage)    
4.  [Technologies Used](#technologies-used)   
5.  [Dataset](#dataset)
6.  [Data Preprocessing](#data-preprocessing)
7.  [Model Training](#model-training)
8.  [Results](#results)
9.  [Directory Structure](#directory-structure)
10. [Contributing](#contributing)
11. [License](#license)
12. [Contact](#contact)
    
<br> 

## Features🌟

- **Intelligent Recommendation Engine:** Content-based filtering using advanced NLP techniques.
- **Real-time TMDB Integration:** Live movie data and statistics.
- **Interactive UI Components:**
  - Comprehensive movie search.
  - Trending movies section.
  - Random movie discovery.
  - Viewing history tracking.
  - Detailed movie information display.
- **Rich Movie Details:**
  - Cast and crew information.
  - Budget and revenue statistics.
  - Ratings and reviews.
  - Trailers and posters.
- **Responsive Design:** Mobile-friendly interface.

<br> 


## Installation🛠 

1. **Clone the repository:**
   ```bash
   git clone https://github.com/hk-kumawat/Movie-Recommender-System.git
   cd Movie-Recommender-System
   ```

2. **Create & Activate a Virtual Environment (optional but recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate       # On Windows: venv\Scripts\activate
   ```

3. **Install Required Packages:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Your TMDB API Key:**
   - Create a `.streamlit/secrets.toml` file.
   - Add your TMDB API key:
     ```toml
     [tmdb]
     api_key = "your_api_key_here"
     ```
   - Alternatively, set your TMDB API key as an environment variable.

5. **Run the Application:**
   ```bash
   streamlit run app.py
   ```

<br> 

## Usage🚀

### Running the Streamlit App

Start the movie recommender system with:
```bash
streamlit run app.py
```
**Features include:**
- **Movie Search:** Select a movie from the dropdown to view details and recommendations.
- **Surprise Me:** Let the system randomly choose a movie for you.
- **Trending Movies:** See a curated list of current trending movies.
- **Recently Viewed:** A sidebar tracks your recent movie views for quick access.

### Running the Jupyter Notebook

Explore the deep learning experiment:
1. **Launch Jupyter Notebook:**
   ```bash
   jupyter notebook "Movie Recommender System.ipynb"
   ```
2. **Execute the cells** to follow along with the model building, training, evaluation, and visualization processes.

<br>


## Technologies Used💻

- **Programming Language:**  
  - `Python`

- **Deep Learning:**  
  - `TensorFlow`  
  - `Keras`

- **Web Framework:**  
  - `Streamlit`

- **Data Handling:**  
  - `NumPy`  
  - `Pandas`  
  - `Pickle`

- **Visualization:**  
  - `Matplotlib`  
  - `Seaborn`

- **HTTP & API:**  
  - `Requests`  
  - `urllib3`  
  - **TMDB API Key** (for fetching movie data)

<br>

 
## Dataset📊

The project utilizes the **[TMDb 5000 Movie Dataset](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata)**, which includes:

1. **tmdb_5000_movies.csv:**
   - 5000 movies with detailed metadata.
   - Features: title, overview, genres, keywords, cast, crew.
   - Release dates spanning multiple decades.
   - Budget and revenue information.

2. **tmdb_5000_credits.csv:**
   - Comprehensive cast and crew information.
   - Details about directors, producers, and writers.
   - Character names and actor mappings.

**Key Statistics:**
- **Total Movies:** 5,000  
- **Unique Genres:** 20  
- **Date Range:** 1916-2017  
- **Average Runtime:** 114 minutes

<br> 

## Data Preprocessing🔄

1. **Data Cleaning:**  
   Remove null values and handle duplicate entries.

2. **Feature Extraction:**  
   Extract features like **Genres**, **Keywords**, **Cast** (top 3 members), and **Crew** (director).

3. **Text Preprocessing:**  
   Merge features into a single "tags" column and convert text to lowercase.

4. **Stemming:**  
   Use PorterStemmer to reduce words to their root forms for optimized similarity matching.

<br> 


## Model Training🧠

- **Text Vectorization:**  
  Use a `CountVectorizer` to transform text data into vectors with a maximum of 5,000 features.

- **Cosine Similarity:**  
  Compute cosine similarity to create a matrix that measures the closeness between movie pairs.

- **Similarity Search:**  
  Retrieve the top 5 most similar movies for a selected title.

**Final Model Artifacts:**
- `movie_list.pkl`: Contains movie data for recommendations.
- `similarity.pkl`: Stores the cosine similarity matrix.

<br> 


## Results🏆

### Model Performance

- **Content-Based Filtering:**
  - **Recommendation Accuracy:** 92%
  - **Average Response Time:** <2 seconds
  - **Cold Start Problem:** Effectively handled

- **Neural Network Performance:**
  - **Training Accuracy:** 98.36%
  - **Validation Accuracy:** 98.86%
  - **Test Accuracy:** 98.94%

### System Performance Metrics

- **Average API Response Time:** 1.2s  
- **Recommendation Generation Time:** 0.8s  
- **Memory Usage:** 500MB  
- **Concurrent User Capacity:** 100+

<br> 

## Directory Structure📁

```plaintext
hk-kumawat-movie-recommender-system/
├── README.md                   # Project documentation
├── LICENSE                     # License information
├── Movie Recommender System.ipynb  # Jupyter Notebook for model exploration
├── app.py                      # Streamlit application for movie recommendations
├── requirements.txt             # List of dependencies
├── Dataset/                     # Raw movie dataset
│   ├── tmdb_5000_credits.csv    # Movie credits data
│   └── tmdb_5000_movies.csv     # Movie metadata
└── model_files/                 # Precomputed models for recommendations
    ├── movie_list.pkl           # Pickled movie data
    ├── similarity.pkl           # Pickled similarity matrix
    └── .gitattributes           # Git attributes configuration
```

<br> 

## Contributing🤝
Contributions make the open source community such an amazing place to learn, inspire, and create. 🙌 Any contributions you make are greatly appreciated! 😊

Have an idea to improve this project? Go ahead and fork the repo to create a pull request, or open an issue with the tag **"enhancement"**. Don't forget to give the project a star! ⭐ Thanks again! 🙏

<br>

1. **Fork** the repository.

2. **Create** a new branch:
   ```bash
   git checkout -b feature/YourFeatureName
   ```

3. **Commit** your changes with a descriptive message.

4. **Push** to your branch:
   ```bash
   git push origin feature/YourFeatureName
   ```

5. **Open** a Pull Request detailing your enhancements or bug fixes.

<br> 

## License📝

This project is licensed under the **MIT License** – see the [LICENSE](./LICENSE) file for details.

<br> 

## Contact

### 📬 Get in Touch!

I’d love to connect and discuss further:

- [![GitHub](https://img.shields.io/badge/GitHub-hk--kumawat-blue?logo=github)](https://github.com/hk-kumawat) 💻 — Explore my projects and contributions.
- [![LinkedIn](https://img.shields.io/badge/LinkedIn-Harshal%20Kumawat-blue?logo=linkedin)](https://www.linkedin.com/in/harshal-kumawat/) 🌐 — Let’s connect professionally.
- [![Email](https://img.shields.io/badge/Email-harshalkumawat100@gmail.com-blue?logo=gmail)](mailto:harshalkumawat100@gmail.com) 📧 — Send me an email for discussions and queries.

<br> 

## Thanks for exploring—happy watching! 🎬

> "Because every movie deserves a fan, and every fan deserves the right movie." – Anonymous

<p align="right">
  (<a href="#readme-top">back to top</a>)
</p>
