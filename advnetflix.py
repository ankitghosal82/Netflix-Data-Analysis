# netflix_dashboard.py

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

# Page config
st.set_page_config(page_title="Netflix Analysis Dashboard", layout="wide")

# Load and preprocess data
def load_data():
    df = pd.read_csv("netflix_titles.csv")
    df.dropna(subset=['director', 'country', 'rating', 'date_added'], inplace=True)
    df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')
    df.dropna(subset=['date_added'], inplace=True)
    df['year_added'] = df['date_added'].dt.year
    df['month_added'] = df['date_added'].dt.month
    df['month_name_added'] = df['date_added'].dt.month_name()
    df['cast'] = df['cast'].fillna("Not specified")
    df['duration'] = df['duration'].fillna("Unknown")
    return df

df = load_data()

# Sidebar filters
st.sidebar.title("Filters")
year_range = st.sidebar.slider("Select Year Range", int(df['year_added'].min()), int(df['year_added'].max()), (2015, 2021))
selected_type = st.sidebar.multiselect("Select Type", df['type'].unique(), default=df['type'].unique())

df_filtered = df[(df['year_added'].between(*year_range)) & (df['type'].isin(selected_type))]

# Dashboard title
st.title("📺 Netflix Data Analysis Dashboard")

# 1. Type distribution
st.subheader("Content Type Distribution")
st.bar_chart(df_filtered['type'].value_counts())

# 2. Yearly additions
st.subheader("Yearly Additions")
fig1 = px.bar(df_filtered['year_added'].value_counts().sort_index(), labels={'value':'Count', 'index':'Year'})
st.plotly_chart(fig1, use_container_width=True)

# 3. Month-wise additions
st.subheader("Monthly Additions")
month_order = ['January','February','March','April','May','June','July','August','September','October','November','December']
fig2 = px.bar(df_filtered['month_name_added'].value_counts().reindex(month_order), labels={'value':'Count', 'index':'Month'})
st.plotly_chart(fig2, use_container_width=True)

# 4. Heatmap: Content Type vs Rating
st.subheader("Heatmap: Type vs Rating")
heatmap_data = pd.crosstab(df_filtered['type'], df_filtered['rating'])
fig3, ax = plt.subplots()
sns.heatmap(heatmap_data, cmap='coolwarm', annot=True, fmt='d', ax=ax)
st.pyplot(fig3)

# 5. Violin Plot: Year vs Content Type
st.subheader("Violin Plot: Content Year Distribution by Type")
fig4 = px.violin(df_filtered, x="type", y="year_added", box=True, points="all", color="type")
st.plotly_chart(fig4, use_container_width=True)

# 6. Top Genres
st.subheader("Top 10 Genres")
genres = df_filtered['listed_in'].str.split(', ').explode()
top_genres = genres.value_counts().head(10)
st.bar_chart(top_genres)

# 7. Choropleth: Country Content Volume
st.subheader("World Map: Content Count by Country")
country_data = df_filtered['country'].str.split(', ').explode().value_counts().reset_index()
country_data.columns = ['country', 'count']
fig5 = px.choropleth(country_data, locations='country', locationmode='country names',
                     color='count', color_continuous_scale='Blues',
                     title="Content Count by Country")
st.plotly_chart(fig5)

# Footer
st.markdown("---")
st.markdown("📊 Built with Python | Pandas | Seaborn | Plotly | Streamlit")
