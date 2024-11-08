# 🎬 Movie Recommender System 📽️  

![132905471-3ef27af4-ecc6-44bf-a47c-5ccf2250410c](https://github.com/user-attachments/assets/c83f35ad-8079-4a51-831f-0b44714d9a75)


## Overview

The Movie Recommender System leverages machine learning and natural language processing to suggest movies similar to a user’s selected movie. Using metadata from movies such as genres, keywords, cast, and crew, it provides recommendations based on similarity. This project is ideal for applications like personalized streaming services and movie discovery platforms.


## Live Demo

Try out the Handwritten Digit Recognizer! 👉🏻 [![Experience It! 🌟](https://img.shields.io/badge/Experience%20It!-blue)](https://findmynextflick.streamlit.app/#7c707207)

<br>

_Below is a preview of the Movie Recommender System in action. Enter a movie name to see similar movie suggestions! 👇🏻_


<p align="center">
  <img src="https://github.com/user-attachments/assets/71eb852d-f796-47d8-9837-e4e76e17a526" alt="movie">
</p>

<br>


## Table of Contents

1. [Features](#features)
2. [Dataset](#dataset)
3. [Data Preprocessing](#data-preprocessing)
4. [Model Training](#model-training)
5. [Installation](#installation)
6. [Usage](#usage)
7. [Technologies Used](#technologies-used)
8. [Results](#results)
9. [Conclusion](#conclusion)
10. [Contact](#contact)

<br>

## Features🌟

- Real-time movie recommendations based on a user-selected movie.
- Integrates with The Movie Database (TMDb) API to fetch trending movies and posters.
- Provides an intuitive interface built with Streamlit for an engaging user experience.
- Optimized for fast processing and real-time recommendations, even with large datasets.


<br>

## Dataset📊

- **[TMDb 5000 Movie Dataset](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata)**: This dataset contains detailed metadata for 5,000 movies, including information like genres, cast, crew, and keywords. It serves as the primary data source for generating movie recommendations based on content similarity.
- **Data Processing**: The dataset is transformed into a similarity matrix that compares movies based on their metadata, enabling the system to find and suggest movies similar to the one selected by the user.


<br>

## Data Preprocessing🛠

1. **Data Cleaning**: Null values are removed, and duplicate entries are handled.
2. **Feature Extraction**: The following features are extracted for each movie:
   - **Genres**
   - **Keywords**
   - **Cast** (top 3 cast members)
   - **Crew** (director only)
3. **Text Preprocessing**: Features are merged into a single "tags" column, with all text converted to lowercase for uniformity.
4. **Stemming**: PorterStemmer is used to reduce words to their root forms, optimizing similarity matching.

<br>

## Model Training🧠

- **Text Vectorization**: A `CountVectorizer` is used to transform text data into vectors, with a maximum of 5,000 features.
- **Cosine Similarity**: Cosine similarity is computed to create a similarity matrix, measuring the closeness of each movie pair.
- **Similarity Search**: The model retrieves the top 5 most similar movies for the selected title.

### Final Model Artifacts:
- `movie_list.pkl`: Contains movie data for the recommendation.
- `similarity.pkl`: Stores the cosine similarity matrix for recommendations.

<br>

## Installation🛠

1. **Clone the repository**:
   ```bash
   https://github.com/hk-kumawat/Movie-Recommender-System.git
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

<br>

## Usage🚀

1. **Run the Streamlit App**:
   ```bash
   streamlit run app.py
   ```

2. **Selecting a Movie**: Choose a movie from the dropdown menu to view recommendations.
3. **Trending Section**: The app also displays the top 5 trending movies based on TMDb’s API.

<br>

## Technologies Used💻

- **Programming Language**: Python
- **Libraries**:
  - `pandas`
  - `numpy`
  - `scikit-learn`
  - `streamlit`
  - `requests`
  - `nltk` (for stemming)
- **API**: TMDb API for fetching trending movies and movie posters

<br>

## Results🏆

The Movie Recommender System effectively recommends movies with similar features, with quick response times and a user-friendly interface. The project showcases how machine learning and NLP can be applied to content-based recommendation systems.

<br>


## Conclusion📚

The **Movie Recommender System** showcases how **machine learning** can enhance user experiences through **intelligent recommendations**. By utilizing metadata like **genres, keywords, cast, and crew**, combined with **cosine similarity**, the system effectively suggests movies similar to a user’s choice. This project exemplifies the potential of **recommendation engines** in various applications, particularly in **content discovery for entertainment platforms**.

With room for further enhancements, such as refining the recommendation logic or expanding the dataset, this system provides a solid foundation for **personalized, data-driven movie suggestions**. It serves as a practical application of **machine learning concepts** and highlights the role of **content-based filtering** in building engaging and user-centric platforms.


<br>

## Contact

### 📬 Get in Touch!
I’d love to connect and discuss further:

- [![GitHub](https://img.shields.io/badge/GitHub-hk--kumawat-blue?logo=github)](https://github.com/hk-kumawat) 💻 — Explore my projects and contributions.
- [![LinkedIn](https://img.shields.io/badge/LinkedIn-Harshal%20Kumawat-blue?logo=linkedin)](https://www.linkedin.com/in/harshal-kumawat/) 🌐 — Let’s connect professionally.
- [![Email](https://img.shields.io/badge/Email-harshalkumawat100@gmail.com-blue?logo=gmail)](mailto:harshalkumawat100@gmail.com) 📧 — Send me an email for discussions and queries.

<br>

---

## Thanks for checking out this movie magic! Enjoy discovering your next favorite film!🎬🔍

> "Because every movie deserves a fan, and every fan deserves the right movie." - Anonymous


