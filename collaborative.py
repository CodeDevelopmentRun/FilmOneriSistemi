import pandas as pd
from surprise import SVD, Dataset, Reader

def get_collaborative_recommendations(user_id, num_recommendations=5):
    # Veriyi oku
    ratings = pd.read_csv("data/ratings.csv")
    movies = pd.read_csv("data/movies.csv")
    
    # Surprise formatı
    reader = Reader(rating_scale=(0.5, 5.0))
    data = Dataset.load_from_df(ratings[['userId', 'movieId', 'rating']], reader)
    trainset = data.build_full_trainset()
    
    # Modeli eğit
    model = SVD()
    model.fit(trainset)
    
    # İzlenmeyen filmleri bul
    all_movie_ids = movies['movieId'].unique()
    watched_movies = ratings[ratings['userId'] == user_id]['movieId'].tolist()
    not_watched = [m for m in all_movie_ids if m not in watched_movies]
    
    # Tahmin yap
    predictions = [model.predict(user_id, m_id) for m_id in not_watched]
    predictions.sort(key=lambda x: x.est, reverse=True)
    
    # En iyi 5 ID'yi al
    top_ids = [int(p.iid) for p in predictions[:num_recommendations]]
    
    # ID'lere göre başlıkları ve ID'leri çek
    top_movies = movies[movies['movieId'].isin(top_ids)]
    
    return top_movies['title'].tolist(), top_movies['movieId'].tolist()