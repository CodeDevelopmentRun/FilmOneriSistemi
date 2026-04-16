import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def get_content_recommendations(movie_title):
    # Veriyi oku
    movies = pd.read_csv("data/movies.csv")
    
    # Türleri temizle
    movies['genres'] = movies['genres'].fillna('')
    movies['genres_cleaned'] = movies['genres'].str.replace('|', ' ', regex=False)
    
    # TF-IDF Vektörleştirici
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(movies['genres_cleaned'])
    
    # Benzerlik matrisi
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
    
    try:
        # Seçilen filmin index'ini bul
        idx = movies[movies['title'] == movie_title].index[0]
        
        # Benzerlik skorlarını al ve sırala
        sim_scores = list(enumerate(cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        
        # En benzer 5 filmi al
        movie_indices = [i[0] for i in sim_scores[1:6]]
        
        # İsimleri ve ID'leri listele
        titles = movies['title'].iloc[movie_indices].tolist()
        ids = movies['movieId'].iloc[movie_indices].tolist()
        
        return titles, ids
    except:
        return [], []