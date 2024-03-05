import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import io

sns.set(style='dark')

def get_total_count_by_hours_df(hours_df):
    hours_count_df = hours_df.groupby(by="hours").agg({"count_cr": ["sum"]})
    hours_count_df.columns = ['total_count']
    return hours_count_df

def count_by_day_df(day_df):
    day_df_count_2011 = day_df.query('dteday >= "2011-01-01" and dteday < "2012-12-31"')
    return day_df_count_2011

def total_registered_df(day_df):
    reg_df = day_df.groupby(by="dteday").agg({
        "registered": "sum"
    })
    reg_df = reg_df.reset_index()
    reg_df.rename(columns={"registered": "register_sum"}, inplace=True)
    return reg_df

def total_casual_df(day_df):
    cas_df = day_df.groupby(by="dteday").agg({
        "casual": ["sum"]
    })
    cas_df = cas_df.reset_index()
    cas_df.rename(columns={"casual": "casual_sum"}, inplace=True)
    return cas_df

def sum_order(hours_df):
    sum_order_items_df = hours_df.groupby("hours").count_cr.sum().sort_values(ascending=False).reset_index()
    return sum_order_items_df

def macem_season(day_df):
    season_df = day_df.groupby(by="season").count_cr.sum().reset_index()
    return season_df

# Membaca data
days_df = pd.read_csv("day.csv")
hours_df = pd.read_csv("hour.csv")

days_df.rename(columns={'yr':'year','mnth':'month','weekday':'one_of_week', 'weathersit':'weather_situation', 'windspeed':'wind_speed','cnt':'count_cr','hum':'humidity'},inplace=True)
hours_df.rename(columns={'yr':'year','hr':'hours','mnth':'month','weekday':'one_of_week', 'weathersit':'weather_situation','windspeed':'wind_speed','cnt':'count_cr','hum':'humidity'},inplace=True)

# Mengatur tampilan DataFrame
datetime_columns = ["dteday"]
for column in datetime_columns:
    days_df[column] = pd.to_datetime(days_df[column])
    hours_df[column] = pd.to_datetime(hours_df[column])

min_date_days = days_df["dteday"].min()
max_date_days = days_df["dteday"].max()

min_date_hours = hours_df["dteday"].min()
max_date_hours = hours_df["dteday"].max()

# Inisialisasi aplikasi Streamlit
with st.sidebar:
    st.image("https://storage.googleapis.com/gweb-uniblog-publish-prod/original_images/image1_hH9B4gs.jpg")
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date_days,
        max_value=max_date_days,
        value=[min_date_days, max_date_days]
    )

main_df_days = days_df[(days_df["dteday"] >= str(start_date)) & (days_df["dteday"] <= str(end_date))]
main_df_hours = hours_df[(hours_df["dteday"] >= str(start_date)) & (hours_df["dteday"] <= str(end_date))]

hours_count_df = get_total_count_by_hours_df(main_df_hours)
days_df_count_2011 = count_by_day_df(main_df_days)
reg_df = total_registered_df(main_df_days)
cas_df = total_casual_df(main_df_days)
sum_order_items_df = sum_order(main_df_hours)
season_df = macem_season(main_df_hours)

# Melengkapi Dashboard dengan Berbagai Visualisasi Data
st.header('Dashboard visualisasi data pinjaman sepeda :sparkles:')
st.subheader('Information')

col1, col2, col3 = st.columns(3)
with col1:
    total_orders = days_df_count_2011.count_cr.sum()
    st.metric("Total Sharing Bike", value=total_orders)

with col2:
    total_sum = reg_df.register_sum.sum()
    st.metric("Total Registered", value=total_sum)

with col3:
    total_sum = cas_df.casual_sum.sum()
    st.metric("Total Casual", value=total_sum)

st.subheader("1. Apakah efek musim mempengaruhi jumlah total penyewaan sepeda ? ")

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    days_df["dteday"],
    days_df["count_cr"],
    marker='o', 
    linewidth=2,
    color="#124076"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
st.pyplot(fig)

st.subheader("2. Bagaimana perbandingan antara casual dan registered?")

labels = 'casual', 'registered'
sizes = [18.8, 81.2]
explode = (0, 0.1) 

fig1, ax1 = plt.subplots()
ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',colors=["#D3D3D3", "#90CAF9"],
        shadow=True, startangle=90)
ax1.axis('equal')  

st.pyplot(fig1)

st.subheader("3. Apakah efek musim mempengaruhi jumlah total penyewaan sepeda ? ")

season_order = ["spring", "summer", "fall", "winter"]
season_labels = ["Spring", "Summer", "Fall", "Winter"]

# Use a different color palette or specify colors for each season
colors = ["#D3D3D3", "#D3D3D3", "#EE4266", "#D3D3D3"]

# membuat subplot dengan 1 baris dan 1 kolom, dengan ukuran (20, 10)
fig, ax = plt.subplots(figsize=(20, 10))

# Buat barplot untuk y="count_cr" dan x="season", menggunakan data=day_df
sns.barplot(
        y="count_cr", 
        x="season",
        data=days_df.sort_values(by="season", ascending=False),
        palette=colors,
        ax=ax
    )
# mengatur judul, label y dan x, serta tick params untuk subplot tersebut
ax.set_title("Penyewaan Sepeda Sepanjang Musim", loc="center", fontsize=30)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='x', labelsize=30)
ax.tick_params(axis='y', labelsize=30)

# Set x-axis labels
ax.set_xticklabels(season_labels, fontsize=20)

st.pyplot(fig)
