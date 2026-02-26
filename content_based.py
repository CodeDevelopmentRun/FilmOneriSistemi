import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def get_content_recommendations(movie_title):
    # Veriyi oku
    movies = pd.read_csv("data/movies.csv")
    
    # Türleri temizle (boşlukları doldur ve ayraçları kaldır)
    movies['genres'] = movies['genres'].fillna('')
    movies['genres_cleaned'] = movies['genres'].str.replace('|', ' ')
    
    # TF-IDF Vektörleştirici (Kelimeleri sayıya çevirir)
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(movies['genres_cleaned'])
    
    # Cosine Similarity (Benzerlik matrisi hesapla)
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
    
    try:
        # Seçilen filmin index'ini bul
        idx = movies[movies['title'] == movie_title].index[0]
        
        # Benzerlik skorlarını al ve sırala
        sim_scores = list(enumerate(cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        
        # En benzer 5 filmi al (0. index filmin kendisidir, o yüzden 1'den başlarız)
        movie_indices = [i[0] for i in sim_scores[1:6]]
        return movies['title'].iloc[movie_indices].tolist()
    except:
        return ["Hata: Film adı tam eşleşmedi."]