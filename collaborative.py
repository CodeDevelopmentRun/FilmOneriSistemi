import pandas as pd
from surprise import SVD, Dataset, Reader

def get_collaborative_recommendations(user_id, num_recommendations=5):
    # Veriyi oku
    ratings = pd.read_csv("data/ratings.csv")
    movies = pd.read_csv("data/movies.csv")
    
    # Surprise kütüphanesi için format belirle
    reader = Reader(rating_scale=(0.5, 5.0))
    data = Dataset.load_from_df(ratings[['userId', 'movieId', 'rating']], reader)
    trainset = data.build_full_trainset()
    
    # SVD Modelini eğit
    model = SVD()
    model.fit(trainset)
    
    # Kullanıcının henüz izlemediği filmleri belirle
    all_movie_ids = movies['movieId'].unique()
    watched_movies = ratings[ratings['userId'] == user_id]['movieId'].tolist()
    not_watched = [m for m in all_movie_ids if m not in watched_movies]
    
    # İzlenmeyen filmler için puan tahmini yap
    predictions = [model.predict(user_id, m_id) for m_id in not_watched]
    predictions.sort(key=lambda x: x.est, reverse=True)
    
    # En yüksek puan tahmini alan 5 filmin adını getir
    top_ids = [int(p.iid) for p in predictions[:num_recommendations]]
    return movies[movies['movieId'].isin(top_ids)]['title'].tolist()