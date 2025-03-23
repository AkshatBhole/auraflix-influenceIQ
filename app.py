import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image
import requests
from io import BytesIO
import time

# Set page configuration
st.set_page_config(
    page_title="InfluenceIQ - AI-Powered Influence Ranking",
    page_icon="🌟",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS styling
def local_css():
    st.markdown("""
    <style>
        .main-header {
            font-size: 3rem !important;
            font-weight: 700 !important;
            color: #1E88E5 !important;
            text-align: center !important;
            margin-bottom: 1rem !important;
        }
        .sub-header {
            font-size: 1.5rem !important;
            font-weight: 500 !important;
            color: #424242 !important;
            text-align: center !important;
            margin-bottom: 2rem !important;
        }
        .metric-card {
            background-color: #f5f5f5;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .profile-header {
            display: flex;
            align-items: center;
        }
        .profile-image {
            border-radius: 50%;
            margin-right: 20px;
        }
        .btn-primary {
            background-color: #1E88E5;
            color: white;
            padding: 10px 24px;
            border-radius: 8px;
            font-weight: 600;
            text-align: center;
            margin: 20px auto;
            display: block;
            width: 200px;
        }
        .category-badge {
            background-color: #E3F2FD;
            color: #1E88E5;
            padding: 5px 10px;
            border-radius: 15px;
            font-size: 0.8rem;
            margin-right: 10px;
        }
    </style>
    """, unsafe_allow_html=True)

local_css()

# Sample data - in a real implementation, this would come from your backend
sample_influencers = [
    {
        "id": 1,
        "name": "Tech Visionary",
        "image_url": "https://randomuser.me/api/portraits/men/32.jpg",
        "category": "Technology",
        "bio": "Founder of multiple tech startups with a focus on AI and sustainability. Regular speaker at industry conferences and author of a bestselling book on future technologies.",
        "scores": {
            "overall": 87.4,
            "credibility": 92.0,
            "longevity": 85.3,
            "engagement": 74.2,
            "sentiment": 88.5,
            "authenticity": 94.3
        },
        "monthly_data": {
            "months": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
            "followers": [920000, 950000, 985000, 1020000, 1075000, 1140000],
            "engagement": [0.078, 0.081, 0.079, 0.082, 0.085, 0.084]
        },
        "content_quality": {
            "categories": ["Technical Depth", "Accuracy", "Originality", "Educational Value", "Presentation"],
            "scores": [9.2, 9.5, 8.7, 9.0, 8.6]
        },
        "platform_presence": {
            "platforms": ["Twitter", "LinkedIn", "YouTube", "Medium", "GitHub"],
            "scores": [87, 94, 76, 89, 95]
        }
    },
    {
        "id": 2,
        "name": "Viral Creator",
        "image_url": "https://randomuser.me/api/portraits/women/44.jpg",
        "category": "Entertainment",
        "bio": "Rising social media star known for viral content. Previously appeared in several commercials and has recently launched a merchandise line.",
        "scores": {
            "overall": 72.3,
            "credibility": 61.5,
            "longevity": 48.7,
            "engagement": 94.8,
            "sentiment": 76.4,
            "authenticity": 65.2
        },
        "monthly_data": {
            "months": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
            "followers": [1000000, 2500000, 3800000, 3500000, 3200000, 3000000],
            "engagement": [0.15, 0.14, 0.13, 0.12, 0.10, 0.09]
        },
        "content_quality": {
            "categories": ["Entertainment Value", "Production Quality", "Originality", "Consistency", "Audience Connection"],
            "scores": [9.3, 8.5, 7.2, 6.8, 9.1]
        },
        "platform_presence": {
            "platforms": ["TikTok", "Instagram", "YouTube", "Twitter", "Snapchat"],
            "scores": [96, 92, 78, 65, 89]
        }
    },
    {
        "id": 3,
        "name": "Industry Expert",
        "image_url": "https://randomuser.me/api/portraits/women/68.jpg",
        "category": "Business",
        "bio": "Former Fortune 500 executive with over 20 years of experience in business strategy. Regular contributor to leading business publications and advisor to multiple companies.",
        "scores": {
            "overall": 84.9,
            "credibility": 95.2,
            "longevity": 91.5,
            "engagement": 62.8,
            "sentiment": 84.3,
            "authenticity": 93.7
        },
        "monthly_data": {
            "months": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
            "followers": [420000, 435000, 450000, 468000, 482000, 498000],
            "engagement": [0.045, 0.047, 0.048, 0.052, 0.054, 0.056]
        },
        "content_quality": {
            "categories": ["Expertise Depth", "Research Quality", "Actionable Insights", "Clarity", "Thought Leadership"],
            "scores": [9.8, 9.6, 9.4, 8.9, 9.7]
        },
        "platform_presence": {
            "platforms": ["LinkedIn", "Twitter", "Harvard Business Review", "Forbes", "Podcast Network"],
            "scores": [96, 82, 91, 88, 79]
        }
    }
]

# Convert to DataFrame for easier manipulation
df_influencers = pd.DataFrame([
    {
        "id": infl["id"],
        "name": infl["name"],
        "image_url": infl["image_url"],
        "category": infl["category"],
        "overall_score": infl["scores"]["overall"],
        "credibility": infl["scores"]["credibility"],
        "longevity": infl["scores"]["longevity"],
        "engagement": infl["scores"]["engagement"]
    } for infl in sample_influencers
])

# Main function to manage app state
def main():
    # Session state initialization
    if 'page' not in st.session_state:
        st.session_state.page = 'intro'
    if 'selected_influencer' not in st.session_state:
        st.session_state.selected_influencer = None
    
    # Navigation
    if st.session_state.page == 'intro':
        show_intro_page()
    elif st.session_state.page == 'rankings':
        show_rankings_page()
    elif st.session_state.page == 'profile':
        show_profile_page(st.session_state.selected_influencer)

# Function to display intro page
def show_intro_page():
    st.markdown('<h1 class="main-header">InfluenceIQ</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">The AI-Powered System That Ranks Who Really Matters!</p>', unsafe_allow_html=True)
    
    # Introduction content
    col1, col2, col3 = st.columns([1, 6, 1])
    with col2:
        st.image("https://img.freepik.com/free-vector/gradient-network-connection-background_23-2148865392.jpg", use_column_width=True)
        
        st.markdown("""
        ## 🚀 The Real Challenge
        
        In a world where fame is just a click away, how do we truly measure lasting influence? 
        Viral sensations fade, but how do we recognize those who stay relevant and credible over time? 
        
        Unlike movies that have IMDb ratings, public figures—be it influencers, entrepreneurs, athletes, or creators—lack 
        a universal system that fairly measures their impact and long-term relevance.
        
        ## 🌟 Our Solution
        
        InfluenceIQ is a next-generation rating system that doesn't just track popularity but values:
        
        - ⭐ **Credibility & Trustworthiness** - How credible are they in their field?
        - ⏳ **Fame Longevity** - How long have they remained relevant?
        - 📈 **Meaningful Engagement** - Are they influencing for the better or just trending for the moment?
        
        ## 🤖 AI-Powered Analysis
        
        Our platform leverages advanced AI to:
        
        - Analyze sentiment across social media and news mentions
        - Detect artificial engagement and follower patterns
        - Assess content quality and substance beyond surface metrics
        - Predict long-term influence based on historical patterns
        """)
        
        # Button to rankings page
        if st.button('View Influencer Rankings', key='to_rankings'):
            st.session_state.page = 'rankings'
            st.experimental_rerun()

# Function to display rankings page
def show_rankings_page():
    st.markdown('<h1 class="main-header">Influencer Rankings</h1>', unsafe_allow_html=True)
    
    # Filters
    col1, col2 = st.columns(2)
    with col1:
        category_filter = st.selectbox('Filter by Category', ['All Categories'] + list(df_influencers['category'].unique()))
    with col2:
        sort_by = st.selectbox('Sort by', ['Overall Score', 'Credibility', 'Longevity', 'Engagement'])
    
    # Apply filters
    filtered_df = df_influencers
    if category_filter != 'All Categories':
        filtered_df = filtered_df[filtered_df['category'] == category_filter]
    
    # Apply sorting
    sort_column = 'overall_score' if sort_by == 'Overall Score' else sort_by.lower()
    filtered_df = filtered_df.sort_values(by=sort_column, ascending=False).reset_index(drop=True)
    
    # Display rankings
    st.markdown("### Top Ranked Influencers")
    
    # Create three columns for each row
    for i, row in filtered_df.iterrows():
        col1, col2 = st.columns([1, 3])
        
        with col1:
            st.image(row['image_url'], width=100)
        
        with col2:
            st.markdown(f"#### {i+1}. {row['name']}")
            st.markdown(f"<span class='category-badge'>{row['category']}</span>", unsafe_allow_html=True)
            
            # Score bars
            col_score1, col_score2 = st.columns(2)
            with col_score1:
                st.markdown(f"**Overall Score:** {row['overall_score']}")
                st.progress(row['overall_score']/100)
            with col_score2:
                st.markdown(f"**Credibility:** {row['credibility']}")
                st.progress(row['credibility']/100)
            
            # View profile button
            if st.button(f"View Full Profile", key=f"view_{row['id']}"):
                st.session_state.selected_influencer = next((infl for infl in sample_influencers if infl['id'] == row['id']), None)
                st.session_state.page = 'profile'
                st.experimental_rerun()
        
        st.markdown("---")
    
    # Back button
    if st.button('Back to Introduction', key='back_to_intro'):
        st.session_state.page = 'intro'
        st.experimental_rerun()

# Function to display individual profile
def show_profile_page(influencer):
    if not influencer:
        st.error("Influencer not found")
        return
    
    # Header with image and basic info
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.image(influencer['image_url'], width=200)
    
    with col2:
        st.markdown(f"# {influencer['name']}")
        st.markdown(f"<span class='category-badge'>{influencer['category']}</span>", unsafe_allow_html=True)
        st.markdown(f"**Overall InfluenceIQ Score:** {influencer['scores']['overall']}")
        st.progress(influencer['scores']['overall']/100)
        st.markdown(influencer['bio'])
    
    st.markdown("---")
    
    # Main metrics
    st.markdown("## Key Metrics")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### Credibility")
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = influencer['scores']['credibility'],
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Credibility"},
            gauge = {
                'axis': {'range': [None, 100]},
                'bar': {'color': "royalblue"},
                'steps': [
                    {'range': [0, 50], 'color': "lightgray"},
                    {'range': [50, 75], 'color': "gray"}],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 90}}))
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### Longevity")
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = influencer['scores']['longevity'],
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Longevity"},
            gauge = {
                'axis': {'range': [None, 100]},
                'bar': {'color': "green"},
                'steps': [
                    {'range': [0, 50], 'color': "lightgray"},
                    {'range': [50, 75], 'color': "gray"}],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 90}}))
        st.plotly_chart(fig, use_container_width=True)
    
    with col3:
        st.markdown("### Engagement")
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = influencer['scores']['engagement'],
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Engagement"},
            gauge = {
                'axis': {'range': [None, 100]},
                'bar': {'color': "orange"},
                'steps': [
                    {'range': [0, 50], 'color': "lightgray"},
                    {'range': [50, 75], 'color': "gray"}],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 90}}))
        st.plotly_chart(fig, use_container_width=True)
    
    # AI-Powered Analysis
    st.markdown("## AI-Powered Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Sentiment Analysis")
        sentiment_score = influencer['scores']['sentiment']
        st.markdown(f"**Public Sentiment Score:** {sentiment_score}")
        st.progress(sentiment_score/100)
        
        sentiment_color = "green" if sentiment_score > 75 else "orange" if sentiment_score > 50 else "red"
        sentiment_label = "Positive" if sentiment_score > 75 else "Mixed" if sentiment_score > 50 else "Negative"
        
        st.markdown(f"<span style='color:{sentiment_color};font-weight:bold;'>Overall Public Sentiment: {sentiment_label}</span>", unsafe_allow_html=True)
        st.markdown("*Based on AI analysis of mentions across social media, news, and forums*")
    
    with col2:
        st.markdown("### Authenticity Detection")
        authenticity_score = influencer['scores']['authenticity']
        st.markdown(f"**Authenticity Score:** {authenticity_score}")
        st.progress(authenticity_score/100)
        
        auth_color = "green" if authenticity_score > 75 else "orange" if authenticity_score > 50 else "red"
        auth_label = "Highly Authentic" if authenticity_score > 75 else "Moderately Authentic" if authenticity_score > 50 else "Potential Concerns"
        
        st.markdown(f"<span style='color:{auth_color};font-weight:bold;'>Engagement Pattern: {auth_label}</span>", unsafe_allow_html=True)
        st.markdown("*Based on AI detection of unusual patterns in follower growth and engagement*")
    
    # Historical data
    st.markdown("## Historical Trends")
    
    fig = px.line(
        x=influencer['monthly_data']['months'], 
        y=influencer['monthly_data']['followers'],
        labels={'x': 'Month', 'y': 'Followers'},
        title='Follower Growth Over Time'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Content quality
    st.markdown("## Content Quality Assessment")
    
    fig = px.radar(
        r=influencer['content_quality']['scores'],
        theta=influencer['content_quality']['categories'],
        range_r=[0, 10],
        title='Content Quality Breakdown'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Platform presence
    st.markdown("## Platform Presence")
    
    fig = px.bar(
        x=influencer['platform_presence']['platforms'],
        y=influencer['platform_presence']['scores'],
        labels={'x': 'Platform', 'y': 'Influence Score'},
        title='Cross-Platform Influence',
        color=influencer['platform_presence']['scores'],
        color_continuous_scale=px.colors.sequential.Viridis
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Back button
    if st.button('Back to Rankings', key='back_to_rankings'):
        st.session_state.page = 'rankings'
        st.experimental_rerun()

# Run the app
if __name__ == "__main__":
    main()