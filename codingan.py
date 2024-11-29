import streamlit as st
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Membaca data dari file Excel
try:
    df = pd.read_excel('df_cleaned (1).xlsx')
except FileNotFoundError:
    st.error("File 'df_cleaned.xlsx' tidak ditemukan. Pastikan file ada di direktori yang benar.")
    st.stop()

# Pastikan kolom yang diperlukan ada di dataset
required_columns = ['TreatmentPlace', 'GroupProvider', 'Nama Item Garda Medika', 'Qty', 'Amount Bill']
if not all(col in df.columns for col in required_columns):
    st.error("Dataset tidak memiliki kolom yang diperlukan. Pastikan kolom berikut ada: " + ", ".join(required_columns))
    st.stop()

# Streamlit App Title
st.title("Dashboard Sebaran Obat di Tiap Rumah Sakit 💊")

# Filter Utama
st.header("Pilih Filter untuk Membandingkan Data")

# Filter untuk Treatment Place
selected_treatment_places = st.multiselect(
    "Pilih Treatment Place:",
    options=df['TreatmentPlace'].dropna().unique(),
    default=df['TreatmentPlace'].dropna().unique()[:1]
)

# Filter untuk Group Provider
selected_group_providers = st.multiselect(
    "Pilih Group Provider:",
    options=df['GroupProvider'].dropna().unique(),
    default=df['GroupProvider'].dropna().unique()[:1]
)

# Tombol untuk Menampilkan Hasil
if st.button("Tampilkan Perbandingan"):
    if not selected_treatment_places and not selected_group_providers:
        st.warning("Pilih setidaknya satu filter untuk Treatment Place atau Group Provider.")
    else:
        # Kombinasi filter untuk dibandingkan
        comparison_filters = [
            (treatment, provider)
            for treatment in selected_treatment_places
            for provider in selected_group_providers
        ]
        
        # Menampilkan Tabs
        st.header("Perbandingan Data")
        if comparison_filters:
            tabs = st.tabs([f"{treatment} - {provider}" for treatment, provider in comparison_filters])
            for i, (treatment, provider) in enumerate(comparison_filters):
                with tabs[i]:
                    # Filter Data
                    filtered_df = df.copy()
                    if treatment:
                        filtered_df = filtered_df[filtered_df['TreatmentPlace'] == treatment]
                    if provider:
                        filtered_df = filtered_df[filtered_df['GroupProvider'] == provider]
                    
                    if filtered_df.empty:
                        st.warning("Tidak ada data untuk filter ini.")
                        continue
                    
                    # Tabel Data
                    st.subheader(f"Tabel Data ({treatment} - {provider})")
                    st.write(filtered_df[['TreatmentPlace', 'GroupProvider', 'Nama Item Garda Medika', 'Qty', 'Amount Bill']])
                    
                    # Total Records
                    st.text(f"Total Records: {len(filtered_df)}")
                    
                    # Total Amount Bill
                    total_amount_bill = filtered_df['Amount Bill'].sum()
                    formatted_total_amount_bill = f"Rp {total_amount_bill:,.0f}".replace(",", ".")
                    st.subheader(f"Total Amount Bill: {formatted_total_amount_bill}")
                    
                    # WordCloud
                    st.subheader(f"WordCloud ({treatment} - {provider})")
                    wordcloud_text = " ".join(filtered_df['Nama Item Garda Medika'].dropna().astype(str))
                    wordcloud = WordCloud(width=800, height=400, background_color="white").generate(wordcloud_text)
                    
                    # Display WordCloud
                    fig, ax = plt.subplots(figsize=(10, 5))
                    ax.imshow(wordcloud, interpolation="bilinear")
                    ax.axis("off")
                    st.pyplot(fig)
        else:
            st.warning("Tidak ada kombinasi filter yang valid untuk ditampilkan.")
else:
    st.info("Gunakan filter di atas, lalu tekan tombol 'Tampilkan Perbandingan' untuk melihat hasil.")
