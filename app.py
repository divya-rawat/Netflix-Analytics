import streamlit as st
import pandas as pd
import plotly.express as px

# =========================================
# PAGE CONFIG
# =========================================

st.set_page_config(
    page_title="Netflix Analytics",
    page_icon="🌌",
    layout="wide"
)

# =========================================
# LOAD DATA
# =========================================

df = pd.read_csv("netflix_titles.csv")

# FILTER NULL COUNTRIES
df.dropna(subset=["country"], inplace=True)

# =========================================
# SIDEBAR
# =========================================

st.sidebar.title("Filters")

selected_type = st.sidebar.selectbox(
    "Select Content Type",
    ["All", "Movie", "TV Show"]
)

# COUNTRY FILTER

all_countries = sorted(
    df['country']
    .dropna()
    .str.split(', ')
    .explode()
    .unique()
)

selected_country = st.sidebar.selectbox(
    "🌍 Select Country",
    ["All"] + all_countries
)

# GENRE FILTER

all_genres = sorted(
    df['listed_in']
    .dropna()
    .str.split(', ')
    .explode()
    .unique()
)

selected_genre = st.sidebar.selectbox(
    "🎭 Select Genre",
    ["All"] + all_genres
)

# =========================================
# FILTERING LOGIC
# =========================================

filtered_df = df.copy()

# TYPE FILTER

if selected_type != "All":
    filtered_df = filtered_df[
        filtered_df["type"] == selected_type
    ]

# COUNTRY FILTER

if selected_country != "All":

    filtered_df = filtered_df[
        filtered_df['country']
        .str.contains(selected_country, na=False)
    ]

# GENRE FILTER

if selected_genre != "All":

    filtered_df = filtered_df[
        filtered_df['listed_in']
        .str.contains(selected_genre, na=False)
    ]

# =========================================
# KPI CALCULATIONS
# =========================================

total_movies = filtered_df[filtered_df['type'] == 'Movie'].shape[0]

total_shows = filtered_df[filtered_df['type'] == 'TV Show'].shape[0]

total_countries = filtered_df['country'].nunique()

genres = filtered_df['listed_in'].str.split(', ').explode()

top_genre = genres.value_counts().idxmax()

# =========================================
# CYBERPUNK CSS
# =========================================

st.markdown("""
<style>

/* MAIN BACKGROUND */

[data-testid="stAppViewContainer"] {
    background: #0D0B1F;
    color: white;
}

/* MAIN CONTENT */

.main .block-container {
    padding-top: 2rem;
    background: #0D0B1F;
}

/* REMOVE WHITE HEADER */

[data-testid="stHeader"] {
    background: rgba(0,0,0,0);
}

/* SIDEBAR */

section[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #140021,
        #0D0B1F
    );
    border-right: 1px solid rgba(168,85,247,0.3);
}

/* SIDEBAR TEXT */

section[data-testid="stSidebar"] * {
    color: white;
}

/* SIDEBAR SELECTBOX */

.stSelectbox div[data-baseweb="select"] {
    background-color: rgba(255,255,255,0.05);
    border: 1px solid rgba(168,85,247,0.4);
    border-radius: 12px;
}

/* SIDEBAR GLOW */

section[data-testid="stSidebar"]::after {
    content: "";
    position: absolute;
    top: 0;
    right: -2px;
    width: 3px;
    height: 100%;
    background: #A855F7;
    box-shadow: 0px 0px 20px #A855F7;
}

/* MAIN TITLE */

.main-title {
    font-size: 65px;
    font-weight: bold;
    text-align: center;
    color: #C084FC;
    text-shadow: 0px 0px 25px #9333EA;
    margin-top: 10px;
}

/* SUBTITLE */

.subtitle {
    text-align: center;
    font-size: 24px;
    color: #E9D5FF;
    margin-bottom: 45px;
}

/* KPI CARDS */

.card {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(192,132,252,0.3);
    padding: 25px;
    border-radius: 22px;
    text-align: center;
    box-shadow: 0px 0px 20px rgba(168,85,247,0.25);
    transition: 0.3s;
    min-height: 180px;
}

.card:hover {
    transform: scale(1.03);
    box-shadow: 0px 0px 30px rgba(192,132,252,0.6);
}

/* CARD NUMBER */

.card-number {
    font-size: 42px;
    font-weight: bold;
    color: #F0ABFC;
    margin-top: 20px;
}

/* CARD TEXT */

.card-text {
    font-size: 20px;
    color: #E9D5FF;
    margin-top: 15px;
}

/* FIX LONG GENRE TEXT */

.genre-fix {
    font-size: 28px !important;
    word-wrap: break-word;
    padding: 10px;
}

</style>
""", unsafe_allow_html=True)

# =========================================
# HERO SECTION
# =========================================

st.markdown(
    '<div class="main-title">NETFLIX ANALYTICS PROJECT</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Explore Netflix trends with dynamic insights</div>',
    unsafe_allow_html=True
)

# =========================================
# KPI CARDS
# =========================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="card">
        <div class="card-number">{total_movies}</div>
        <div class="card-text">Movies</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="card">
        <div class="card-number">{total_shows}</div>
        <div class="card-text">TV Shows</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="card">
        <div class="card-number">{total_countries}</div>
        <div class="card-text">Countries</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="card">
        <div class="card-number genre-fix">{top_genre}</div>
        <div class="card-text">Top Genre</div>
    </div>
    """, unsafe_allow_html=True)

# SPACING
st.write("")
st.write("")

# =========================================
# SECTION TITLE
# =========================================

st.subheader("📊 Streaming Intelligence")

# =========================================
# DASHBOARD ROW 1
# =========================================

col_left, col_right = st.columns(2)

# =========================================
# LEFT CHART — TOP GENRES
# =========================================

with col_left:

    genre_counts = genres.value_counts().head(10)

    fig_genres = px.bar(
        x=genre_counts.values,
        y=genre_counts.index,
        orientation='h',
        labels={
            'x': 'Titles',
            'y': 'Genre'
        }
    )

    fig_genres.update_layout(

        paper_bgcolor='#111111',
        plot_bgcolor='rgba(0,0,0,0)',

        font_color='white',

        title={
            'text': '🌌 Top Genres',
            'x': 0.03,
            'font': {
                'size': 24,
                'color': '#C084FC'
            }
        },

        xaxis=dict(
            showgrid=True,
            gridcolor='rgba(168,85,247,0.15)',
            zeroline=False
        ),

        yaxis=dict(
            showgrid=False
        ),

        height=500,

        margin=dict(
            l=20,
            r=20,
            t=70,
            b=20
        )
    )

    fig_genres.update_traces(
        marker=dict(
            color='#A855F7',
            line=dict(
                color='#F0ABFC',
                width=2
            )
        )
    )

    st.plotly_chart(fig_genres, use_container_width=True)

    # =========================================
    # DYNAMIC GENRE INSIGHT
    # =========================================

    top_genre_name = genre_counts.index[0]
    top_genre_count = genre_counts.values[0]

    st.markdown(f"""
    <div style="
    background: rgba(255,255,255,0.05);
    padding:18px;
    border-radius:16px;
    border-left: 4px solid #A855F7;
    margin-top:10px;
    margin-bottom:25px;
    box-shadow: 0px 0px 12px rgba(168,85,247,0.2);
    ">

    <h4 style="color:#E9D5FF;">📌 Genre Insight</h4>

    <p style="color:white; font-size:16px; line-height:1.7;">
    <b>{top_genre_name}</b> is currently the most dominant genre with 
    <b>{top_genre_count}</b> titles in the selected dataset. 
    This suggests strong audience demand and continued platform investment in this category.
    </p>

    </div>
    """, unsafe_allow_html=True)

# =========================================
# RIGHT CHART — DONUT CHART
# =========================================

with col_right:

    type_counts = filtered_df['type'].value_counts()

    fig_donut = px.pie(
        values=type_counts.values,
        names=type_counts.index,
        hole=0.6
    )

    fig_donut.update_traces(
        textinfo='percent+label',
        marker=dict(
            colors=['#A855F7', '#EC4899'],
            line=dict(
                color='#1E1B4B',
                width=3
            )
        )
    )

    fig_donut.update_layout(

        paper_bgcolor='#111111',
        plot_bgcolor='rgba(0,0,0,0)',

        font_color='white',

        title={
            'text': '🍿 Content Distribution',
            'x': 0.12,
            'font': {
                'size': 24,
                'color': '#C084FC'
            }
        },

        height=500,

        showlegend=True
    )

    st.plotly_chart(fig_donut, use_container_width=True)

    # =========================================
    # DYNAMIC CONTENT INSIGHT
    # =========================================

    dominant_type = type_counts.idxmax()
    dominant_percent = round(
        (type_counts.max() / type_counts.sum()) * 100,
        1
    )

    st.markdown(f"""
    <div style="
    background: rgba(255,255,255,0.05);
    padding:18px;
    border-radius:16px;
    border-left: 4px solid #EC4899;
    margin-top:10px;
    margin-bottom:25px;
    box-shadow: 0px 0px 12px rgba(236,72,153,0.2);
    ">

    <h4 style="color:#FBCFE8;">📌 Content Insight</h4>

    <p style="color:white; font-size:16px; line-height:1.7;">
    <b>{dominant_type}</b> content dominates the filtered dataset, accounting for 
    <b>{dominant_percent}%</b> of total titles. 
    This reflects Netflix’s strategic emphasis on this content format.
    </p>

    </div>
    """, unsafe_allow_html=True)

# =========================================
# RELEASE TREND CHART
# =========================================

st.write("")
st.write("")

release_year_data = (
    filtered_df['release_year']
    .value_counts()
    .sort_index()
)

fig_line = px.line(
    x=release_year_data.index,
    y=release_year_data.values,
    labels={
        "x": "Release Year",
        "y": "Number of Titles"
    }
)

fig_line.update_traces(
    line=dict(
        color='#C084FC',
        width=4
    )
)

fig_line.update_layout(

    paper_bgcolor='#111111',
    plot_bgcolor='rgba(0,0,0,0)',

    font_color='white',

    title={
        'text': '📈 Netflix Growth Over Time',
        'x': 0.03,
        'font': {
            'size': 28,
            'color': '#C084FC'
        }
    },

    xaxis=dict(
        showgrid=False
    ),

    yaxis=dict(
        showgrid=True,
        gridcolor='rgba(168,85,247,0.12)'
    ),

    height=500
)

st.plotly_chart(fig_line, use_container_width=True)

# =========================================
# DYNAMIC GROWTH INSIGHT
# =========================================

peak_year = release_year_data.idxmax()
peak_titles = release_year_data.max()

st.markdown(f"""
<div style="
background: rgba(255,255,255,0.05);
padding:18px;
border-radius:16px;
border-left: 4px solid #C084FC;
margin-top:10px;
margin-bottom:30px;
box-shadow: 0px 0px 12px rgba(192,132,252,0.2);
">

<h4 style="color:#E9D5FF;">📌 Growth Insight</h4>

<p style="color:white; font-size:16px; line-height:1.7;">
Netflix content production peaked around <b>{peak_year}</b> 
with approximately <b>{peak_titles}</b> titles released. 
This may indicate a major expansion phase in streaming content investment.
</p>

</div>
""", unsafe_allow_html=True)

# =========================================
# ROW 3 — COUNTRIES + HEATMAP
# =========================================

st.write("")
st.write("")

col3_left, col3_right = st.columns(2)

# =========================================
# TOP COUNTRIES CHART
# =========================================

with col3_left:

    country_counts = (
        filtered_df['country']
        .str.split(', ')
        .explode()
        .value_counts()
        .head(10)
    )

    fig_country = px.bar(
        x=country_counts.values,
        y=country_counts.index,
        orientation='h',
        labels={
            'x': 'Titles',
            'y': 'Country'
        }
    )

    fig_country.update_layout(

        paper_bgcolor='#111111',
        plot_bgcolor='rgba(0,0,0,0)',

        font_color='white',

        title={
            'text': '🌍 Top Content Producing Countries',
            'x': 0.03,
            'font': {
                'size': 24,
                'color': '#C084FC'
            }
        },

        xaxis=dict(
            showgrid=True,
            gridcolor='rgba(168,85,247,0.15)',
            zeroline=False
        ),

        yaxis=dict(
            showgrid=False
        ),

        height=500
    )

    fig_country.update_traces(
        marker=dict(
            color='#9333EA',
            line=dict(
                color='#F0ABFC',
                width=2
            )
        )
    )

    st.plotly_chart(fig_country, use_container_width=True)

    # =========================================
    # DYNAMIC COUNTRY INSIGHT
    # =========================================

    top_country = country_counts.index[0]
    top_country_titles = country_counts.values[0]

    st.markdown(f"""
    <div style="
    background: rgba(255,255,255,0.05);
    padding:18px;
    border-radius:16px;
    border-left: 4px solid #9333EA;
    margin-top:10px;
    margin-bottom:25px;
    box-shadow: 0px 0px 12px rgba(147,51,234,0.2);
    ">

    <h4 style="color:#E9D5FF;">📌 Regional Insight</h4>

    <p style="color:white; font-size:16px; line-height:1.7;">
    <b>{top_country}</b> contributes the highest number of titles 
    with <b>{top_country_titles}</b> entries in the filtered dataset. 
    This highlights the region’s strong influence in Netflix’s content ecosystem.
    </p>

    </div>
    """, unsafe_allow_html=True)

# =========================================
# GENRE HEATMAP
# =========================================

with col3_right:

    heatmap_data = (
        filtered_df.assign(
            main_genre=filtered_df['listed_in']
            .str.split(',')
            .str[0]
        )
        .groupby(['release_year', 'main_genre'])
        .size()
        .reset_index(name='count')
    )

    top_heatmap_genres = (
        heatmap_data.groupby('main_genre')['count']
        .sum()
        .sort_values(ascending=False)
        .head(6)
        .index
    )

    heatmap_filtered = heatmap_data[
        heatmap_data['main_genre'].isin(top_heatmap_genres)
    ]

    heatmap_pivot = heatmap_filtered.pivot(
        index='main_genre',
        columns='release_year',
        values='count'
    ).fillna(0)

    fig_heatmap = px.imshow(
        heatmap_pivot,
        aspect='auto',
        color_continuous_scale='purples'
    )

    fig_heatmap.update_layout(

        paper_bgcolor='#111111',
        plot_bgcolor='rgba(0,0,0,0)',

        font_color='white',

        title={
            'text': '🌌 Genre Popularity Heatmap',
            'x': 0.03,
            'font': {
                'size': 24,
                'color': '#C084FC'
            }
        },

        height=500
    )

    st.plotly_chart(fig_heatmap, use_container_width=True)

    # =========================================
    # DYNAMIC HEATMAP INSIGHT
    # =========================================

    top_heatmap_genre = (
        heatmap_data.groupby('main_genre')['count']
        .sum()
        .idxmax()
    )

    st.markdown(f"""
    <div style="
    background: rgba(255,255,255,0.05);
    padding:18px;
    border-radius:16px;
    border-left: 4px solid #7C3AED;
    margin-top:10px;
    margin-bottom:25px;
    box-shadow: 0px 0px 12px rgba(124,58,237,0.2);
    ">

    <h4 style="color:#DDD6FE;">📌 Heatmap Insight</h4>

    <p style="color:white; font-size:16px; line-height:1.7;">
    The heatmap reveals that <b>{top_heatmap_genre}</b> consistently appears 
    as one of the most prominent genres across multiple years, indicating 
    long-term viewer engagement and sustained platform focus.
    </p>

    </div>
    """, unsafe_allow_html=True)

# =========================================
# FOOTER
# =========================================

st.caption("⚡ Built with Python, Plotly & Cyberpunk Energy")