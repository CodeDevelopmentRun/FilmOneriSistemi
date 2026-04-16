import streamlit as st
import pandas as pd
import requests
from content_based import get_content_recommendations
from collaborative import get_collaborative_recommendations

def get_poster(movie_title):
    api_key = "97c2888f7de49bd7935163f35f5f6621"
    
    # İlk deneme: Yıl ve "The" gibi ekleri temizle
    clean_title = movie_title.split(' (')[0].replace(', The', '').replace(', A', '').strip()
    
    search_url = f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={clean_title}&language=tr-TR"
    
    try:
        response = requests.get(search_url)
        data = response.json()
        
        # Eğer sonuç varsa ilkini döndür
        if data['results'] and data['results'][0].get('poster_path'):
            return "https://image.tmdb.org/t/p/w500/" + data['results'][0]['poster_path']
        
        # İkinci deneme (Hala bulamadıysa): Sadece ilk iki kelimeyle ara (Daha esnek arama)
        words = clean_title.split()
        if len(words) > 2:
            short_title = " ".join(words[:2])
            short_url = f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={short_title}&language=tr-TR"
            res2 = requests.get(short_url).json()
            if res2['results'] and res2['results'][0].get('poster_path'):
                return "https://image.tmdb.org/t/p/w500/" + res2['results'][0]['poster_path']

        return "https://via.placeholder.com/500x750?text=Afiş+Bulunamadı"
    except:
        return "https://via.placeholder.com/500x750?text=Hata"# Sayfa Ayarları
st.set_page_config(page_title="Film Tavsiye Sistemi", layout="wide")
st.title("🎬 Film ve Dizi Öneri Sistemi")
st.markdown("---")

# Veriyi Önbelleğe Alarak Yükle
@st.cache_data
def load_data():
    return pd.read_csv("data/movies.csv")

movies_df = load_data()

# Sol Menü (Sidebar)
st.sidebar.header("📌 Proje Bilgisi")
st.sidebar.info("Bu sistem Content-Based ve Collaborative Filtering algoritmalarını kullanır.")

# Sekmeler
tab1, tab2 = st.tabs(["🎥 Benzer Filmler", "👤 Size Özel Öneriler"])

with tab1:
    st.subheader("İzlediğiniz Bir Filme Göre Öneri Alın")
    movie_list = movies_df['title'].values
    selected_movie = st.selectbox("Film Seçiniz:", movie_list)

    if st.button('Benzerlerini Bul'):
        # Fonksiyon hem isimleri hem idleri döndürüyor
        names, ids = get_content_recommendations(selected_movie)
        
        if names:
            cols = st.columns(5)
            for i in range(len(names)):
                with cols[i]:
                    # Yeni get_poster fonksiyonuna ID yerine İSİM gönderiyoruz
                    poster_url = get_poster(names[i])
                    st.image(poster_url)
                    st.caption(names[i])
        else:
            st.warning("Eşleşen film bulunamadı.")

with tab2:
    st.subheader("İzleme Geçmişinize Göre Öneriler")
    user_id = st.number_input("Kullanıcı ID Giriniz:", min_value=1, step=1)
    
    if st.button('Önerilerimi Getir'):
        names, ids = get_collaborative_recommendations(user_id)
        
        if names:
            cols = st.columns(5)
            for i in range(len(names)):
                with cols[i]:
                    # Burada da isimle arama yapıyoruz
                    poster_url = get_poster(names[i])
                    st.image(poster_url)
                    st.caption(names[i])
        else:
            st.info("Bu kullanıcı için henüz öneri oluşturulamadı.")