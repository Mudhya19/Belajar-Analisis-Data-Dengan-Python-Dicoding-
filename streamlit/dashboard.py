# Import Library
import streamlit as st
import pandas as pd
import seaborn as sns
import plotly.express as px

sns.set(style='dark')

@st.cache_resource
def load_data():
    df_hour = pd.read_csv("../streamlit/hour.csv")
    df_day = pd.read_csv("../streamlit/day.csv")
    return df_hour, df_day


df_hour, df_day = load_data()

# ==============================
# TITLE DASHBOARD
# ==============================
# Set page title
st.title("Bike Share Dashboard")
with st.sidebar:
    st.image("bike.jpg")

if st.sidebar.checkbox("Show Dataset"):
    st.subheader("Raw Data")
    st.write(df_hour)

# Display summary statistics
# Display summary statistics
# Display summary statistics
# Display summary statistics
if st.sidebar.checkbox("Show Summary Statistics"):
    st.subheader("Summary Statistics")
    st.write(df_hour.describe())



# ==============================
# SIDEBAR
# ==============================
st.sidebar.title("Dataset Bike Share")
st.sidebar.markdown("[Download Dataset](https://link-to-your-dataset)")
st.sidebar.markdown('**Weather:**')
st.sidebar.markdown('1: Clear, Few clouds, Partly cloudy, Partly cloudy')
st.sidebar.markdown('2: Mist + Cloudy, Mist + Broken clouds, Mist + Few clouds, Mist')
st.sidebar.markdown('3: Light Snow, Light Rain + Thunderstorm + Scattered clouds, Light Rain + Scattered clouds')
st.sidebar.markdown('4: Heavy Rain + Ice Pallets + Thunderstorm + Mist, Snow + Fog')

# ==============================
# VISUALIZATION
# ==============================
col1, col2 = st.columns(2)


with col1:
    # Season-wise bike share count
    # st.subheader("Season-wise Bike Share Count")

    # Filter data untuk musim gugur (season 3) pada tahun 2011 dan 2012
    filtered_data_2011_autumn = df_day[(df_day["yr"] == 0) & (df_day["season"] == 3)]
    filtered_data_2012_autumn = df_day[(df_day["yr"] == 1) & (df_day["season"] == 3)]

    # Hitung total sewa sepeda untuk musim gugur tahun 2011 dan 2012
    total_sewa_2011_autumn = filtered_data_2011_autumn["cnt"].sum()
    total_sewa_2012_autumn = filtered_data_2012_autumn["cnt"].sum()

    # Visualisasikan dengan bar chart
    fig = px.bar(x=["2011", "2012"], y=[total_sewa_2011_autumn, total_sewa_2012_autumn],
                labels={"x": "Tahun", "y": "Total Sewa Sepeda"})

    # Tampilkan chart menggunakan Streamlit
    st.plotly_chart(fig, use_container_width=True)
    st.subheader("Total Sewa Sepeda Musim Gugur (Musim 3) Tahun 2011 dan 2012")
    st.write(f"Jumlah total sepeda yang disewakan pada tahun 2011: {total_sewa_2011_autumn}")
    st.write(f"\nJumlah total sepeda yang disewakan pada tahun 2012: {total_sewa_2012_autumn}")

with col2:
    # Weather situation-wise bike share count
    # st.subheader("Weather Situation-wise Bike Share Count")


    # Filter data untuk tahun 2012, musim panas (season 3), dan hari libur (holiday = 1)
    filtered_data_2012_summer_holiday = df_day[(df_day["yr"] == 1) & (df_day["season"] == 3) & (df_day["holiday"] == 1)]

    # Hitung jumlah total sepeda yang disewakan
    total_sepeda_disewakan_2012_summer_holiday = filtered_data_2012_summer_holiday["cnt"].sum()

    # Visualisasi Bar Chart
    fig = px.bar(filtered_data_2012_summer_holiday, x="weekday", y="cnt", 
                labels={"weekday": "Hari", "cnt": "Jumlah Sepeda Disewakan"},
                color="weekday",  # Menambahkan warna berbeda untuk setiap hari
                color_discrete_sequence=px.colors.qualitative.Set3)  # Menggunakan warna dari set warna qualitative Set3

    # Tampilkan plot dalam Streamlit app
    st.plotly_chart(fig, use_container_width=True)
    # Tampilkan hasil total sepeda yang disewakan
    st.subheader("Total Sepeda Disewakan pada Hari Libur Selama Musim Panas (Tahun 2012)")
    st.write(f"Jumlah total sepeda yang disewakan pada hari libur selama musim panas tahun 2012: {total_sepeda_disewakan_2012_summer_holiday}")


# Hourly bike share count
# st.subheader("Hourly Bike Share Count")
# Filter data untuk tahun 2012, Hari Libur (holiday = 1), dan Hari Kerja (workingday = 1)
filtered_data_2012_holiday = df_hour[(df_hour["yr"] == 1) & (df_hour["holiday"] == 1)]
filtered_data_2012_workingday = df_hour[(df_hour["yr"] == 1) & (df_hour["workingday"] == 1)]

# Hitung distribusi per jam sewa sepeda (cnt) untuk Hari Libur dan Hari Kerja
distribusi_per_jam_holiday = filtered_data_2012_holiday.groupby("hr")["cnt"].sum()
distribusi_per_jam_workingday = filtered_data_2012_workingday.groupby("hr")["cnt"].sum()

# Visualisasikan distribusi per jam
fig = px.line(x=distribusi_per_jam_holiday.index, y=distribusi_per_jam_holiday.values,
            labels={"x": "Jam", "y": "Jumlah Sewa Sepeda"},
            title="Distribusi Per Jam Sewa Sepeda pada Hari Libur (2012)",
            line_shape="linear")
fig.update_xaxes(tickmode="linear")
st.plotly_chart(fig, use_container_width=True)

fig = px.line(x=distribusi_per_jam_workingday.index, y=distribusi_per_jam_workingday.values,
        labels={"x": "Jam", "y": "Jumlah Sewa Sepeda"},
        title="Distribusi Per Jam Sewa Sepeda pada Hari Kerja (2012)",
        line_shape="linear")
fig.update_xaxes(tickmode="linear")
st.plotly_chart(fig, use_container_width=True)
# Humidity vs. Bike Share Count

# Scatter plot dengan garis tren
fig_humidity_chart = px.scatter(
    df_day, 
    x="temp", 
    y="registered", 
    color="season",
    size="cnt",
    hover_name="dteday",
    title="Hubungan Suhu dengan Jumlah Pengguna Terdaftar",
    )
st.plotly_chart(fig_humidity_chart, use_container_width=True)


filtered_data_casual_workingday = df_day[(df_day["workingday"] == 1) & (df_day["casual"] > 0)]

# Visualisasikan jumlah sewa sepeda casual pada hari kerja
fig = px.bar(filtered_data_casual_workingday, x="weekday", y="casual", 
            title="Jumlah Sewa Sepeda (Casual) pada Hari Kerja",
            labels={"weekday": "Hari Kerja", "casual": "Jumlah Sewa Sepeda Casual"},
            color="weekday", 
            color_discrete_sequence=px.colors.qualitative.Set3)
st.plotly_chart(fig, use_container_width=True, width=800)


# Filter musim gugur (season 3)
filtered_data_autumn = df_day[df_day["season"] == 3]

# Buat plot untuk menganalisis pengaruh cuaca terhadap jumlah sewa sepeda
fig = px.bar(filtered_data_autumn, x="weathersit", y="cnt", color="weathersit",
            title="Pengaruh Cuaca terhadap Jumlah Sewa Sepeda (Musim Gugur)",
            labels={"weathersit": "Cuaca", "cnt": "Jumlah Sewa Sepeda"},
            category_orders={"weathersit": ["Clear", "Mist", "Light Rain", "Heavy Rain"]},
            opacity=0.8)
st.plotly_chart(fig, use_container_width=True,
                height=400, width=800)

# Show data source and description
st.sidebar.title("About")
st.sidebar.info("Dashboard ini menampilkan visualisasi untuk sekumpulan data Bike Share. "
                "Dataset ini mengandung informasi mengenai penyewaan sepeda berdasarkan berbagai variabel seperti musim, suhu, kelembaban, dan faktor lainnya.")
