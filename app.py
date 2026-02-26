import streamlit as st
import pandas as pd
from content_based import get_content_recommendations
from collaborative import get_collaborative_recommendations

# Sayfa Yapılandırması
st.set_page_config(page_title="Film Tavsiye Sistemi", layout="wide")

st.title("🎬 Film ve Dizi Öneri Sistemi")
st.markdown("---")

# Veri setlerini yükle (İstatistikler için)
movies_df = pd.read_csv("data/movies.csv")

# Sol Menü (Sidebar)
st.sidebar.header("📌 Proje Bilgisi")
st.sidebar.info("Bu sistem Content-Based ve Collaborative Filtering algoritmalarını kullanır.")

# Sekmeli Görünüm
tab1, tab2 = st.tabs(["🎥 Benzer Filmler", "👤 Size Özel Öneriler"])

with tab1:
    st.subheader("İzlediğiniz Bir Filme Göre Öneri Alın")
    movie_list = movies_df['title'].values
    selected_movie = st.selectbox("Film Seçiniz:", movie_list)
    
    if st.button("Benzerlerini Bul"):
        with st.spinner('Hesaplanıyor...'):
            results = get_content_recommendations(selected_movie)
            st.write(f"### '{selected_movie}' Sevenler Bunları da İzledi:")
            for m in results:
                st.write(f"✅ {m}")

with tab2:
    st.subheader("Kullanıcı Profilinize Göre Tahminler")
    u_id = st.number_input("Kullanıcı ID Giriniz (1-610):", min_value=1, max_value=610, value=1)
    
    if st.button("Tahminleri Getir"):
        with st.spinner('Yapay zeka analiz ediyor...'):
            collab_results = get_collaborative_recommendations(u_id)
            st.write(f"### Kullanıcı {u_id} İçin En Yüksek Puanlı Tahminler:")
            for m in collab_results:
                st.write(f"🌟 {m}")