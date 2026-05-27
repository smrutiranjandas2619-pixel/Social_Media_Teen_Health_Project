import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os

def load_app_data():
    # Fallback checking to ensure the data is loaded correctly
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    cleaned_path = os.path.join(base_dir, "data", "cleaned", "cleaned_dataset.csv")
    raw_path = os.path.join(base_dir, "data", "raw", "Teen_Mental_Health_Dataset.csv")
    
    if os.path.exists(cleaned_path):
        return pd.read_csv(cleaned_path)
    elif os.path.exists(raw_path):
        # Raw fallback if cleaned is not yet fully saved
        df = pd.read_csv(raw_path)
        # Apply minimal cleaning to categorical columns so they look nice
        for col in df.select_dtypes(include='object').columns:
            df[col] = df[col].astype(str).str.lower().str.strip()
        # Add basic feature engineering on the fly for visualization
        if 'daily_social_media_hours' in df.columns and 'screen_time_before_sleep' in df.columns:
            df['addiction_score'] = df['daily_social_media_hours'] * df['screen_time_before_sleep']
        if 'sleep_hours' in df.columns:
            df['sleep_disruption'] = np.where(df['sleep_hours'] < 6, 1, 0)
        if 'daily_social_media_hours' in df.columns:
            df['usage_category'] = pd.cut(
                df['daily_social_media_hours'],
                bins=[0, 2, 5, 24],
                labels=['low', 'medium', 'high']
            )
        return df
    else:
        st.error("Error: Dataset files not found. Please run main.py first.")
        return None

def show_visualization_page():
    st.markdown("<h1>📊 Behavioral <span class='neon-text'>Analytics Explorer</span></h1>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 16px; color: #94a3b8;'>Inspect, filter, and discover statistical correlations in teenager screen habits and psychiatric indicators.</p>", unsafe_allow_html=True)

    df = load_app_data()
    if df is None:
        return

    # Clean display formatting
    df['gender'] = df['gender'].str.capitalize()
    df['platform_usage'] = df['platform_usage'].str.capitalize()
    if 'social_interaction_level' in df.columns:
        df['social_interaction_level'] = df['social_interaction_level'].str.capitalize()

    # Dynamic Filter Sidebar
    st.markdown("<div class='glass-card'><h4>🔍 Dynamic Cohort Filtering</h4><p style='font-size: 13px; color: #94a3b8;'>Adjust variables to filter the teen study population in real-time.</p></div>", unsafe_allow_html=True)
    
    col_filters_1, col_filters_2, col_filters_3 = st.columns(3)
    
    with col_filters_1:
        age_range = st.slider(
            "Teenager Age Range",
            min_value=int(df['age'].min()),
            max_value=int(df['age'].max()),
            value=(int(df['age'].min()), int(df['age'].max()))
        )
    with col_filters_2:
        gender_options = ["All"] + list(df['gender'].unique())
        selected_gender = st.selectbox("Filter Gender", gender_options)
    with col_filters_3:
        platform_options = ["All"] + list(df['platform_usage'].unique())
        selected_platform = st.selectbox("Primary Social Platform", platform_options)

    # Filter application
    filtered_df = df[
        (df['age'] >= age_range[0]) & 
        (df['age'] <= age_range[1])
    ]
    if selected_gender != "All":
        filtered_df = filtered_df[filtered_df['gender'] == selected_gender]
    if selected_platform != "All":
        filtered_df = filtered_df[filtered_df['platform_usage'] == selected_platform]

    # Metrics Summary Row
    st.markdown("---")
    m_col1, m_col2, m_col3, m_col4 = st.columns(4)
    with m_col1:
        st.markdown(
            f"<div class='metric-card'><h5 style='color:#94a3b8;margin-top:0px;'>Filtered Cohort</h5>"
            f"<h2 style='margin-bottom:0px;color:#00f2fe;'>{len(filtered_df)} teens</h2></div>", 
            unsafe_allow_html=True
        )
    with m_col2:
        avg_screen = filtered_df['daily_social_media_hours'].mean()
        st.markdown(
            f"<div class='metric-card'><h5 style='color:#94a3b8;margin-top:0px;'>Avg. Daily Hours</h5>"
            f"<h2 style='margin-bottom:0px;color:#00f2fe;'>{avg_screen:.2f} hrs</h2></div>", 
            unsafe_allow_html=True
        )
    with m_col3:
        avg_sleep = filtered_df['sleep_hours'].mean()
        st.markdown(
            f"<div class='metric-card'><h5 style='color:#94a3b8;margin-top:0px;'>Avg. Sleep</h5>"
            f"<h2 style='margin-bottom:0px;color:#00f2fe;'>{avg_sleep:.2f} hrs</h2></div>", 
            unsafe_allow_html=True
        )
    with m_col4:
        depression_rate = (filtered_df['depression_label'].sum() / len(filtered_df)) * 100
        st.markdown(
            f"<div class='metric-card'><h5 style='color:#94a3b8;margin-top:0px;'>Depression Rate</h5>"
            f"<h2 style='margin-bottom:0px;color:#ef4444;'>{depression_rate:.1f}%</h2></div>", 
            unsafe_allow_html=True
        )

    # Core Charts Section
    st.markdown("<h3 style='margin-top: 30px;'>📈 Primary Cohort Analysis</h3>", unsafe_allow_html=True)
    
    col_chart_1, col_chart_2 = st.columns(2)
    
    with col_chart_1:
        st.markdown("<div class='glass-card'><h4>📺 Screen Time vs. Sleep Disruption</h4></div>", unsafe_allow_html=True)
        fig_scatter = px.scatter(
            filtered_df,
            x="daily_social_media_hours",
            y="sleep_hours",
            color="depression_label",
            color_continuous_scale=["#00f2fe", "#ef4444"],
            labels={
                "daily_social_media_hours": "Daily Social Media Hours",
                "sleep_hours": "Sleep Hours",
                "depression_label": "Depression Flag"
            },
            title="Inverse Correlation of Screen Usage and Sleep Hours",
            template="plotly_dark"
        )
        fig_scatter.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_family='Plus Jakarta Sans'
        )
        st.plotly_chart(fig_scatter, use_container_width=True)

    with col_chart_2:
        st.markdown("<div class='glass-card'><h4>📊 Mental Health Burden by Social Platform</h4></div>", unsafe_allow_html=True)
        
        # Calculate platform metrics
        platform_metrics = filtered_df.groupby("platform_usage").agg(
            avg_anxiety=("anxiety_level", "mean"),
            avg_stress=("stress_level", "mean"),
            avg_addiction=("addiction_level", "mean")
        ).reset_index()
        
        fig_platform = go.Figure(data=[
            go.Bar(name='Avg Anxiety', x=platform_metrics['platform_usage'], y=platform_metrics['avg_anxiety'], marker_color='#00f2fe'),
            go.Bar(name='Avg Stress', x=platform_metrics['platform_usage'], y=platform_metrics['avg_stress'], marker_color='#a855f7'),
            go.Bar(name='Avg Addiction', x=platform_metrics['platform_usage'], y=platform_metrics['avg_addiction'], marker_color='#f43f5e')
        ])
        fig_platform.update_layout(
            barmode='group',
            title="Anxiety, Stress, and Addiction Levels (Scale 1-10) by Platform",
            template="plotly_dark",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_family='Plus Jakarta Sans'
        )
        st.plotly_chart(fig_platform, use_container_width=True)

    st.markdown("---")
    
    col_chart_3, col_chart_4 = st.columns(2)
    
    with col_chart_3:
        st.markdown("<div class='glass-card'><h4>🔥 Full Demographic & Clinical Heatmap</h4></div>", unsafe_allow_html=True)
        
        # Calculate numerical correlations
        corr_cols = [
            "age", "daily_social_media_hours", "sleep_hours", 
            "screen_time_before_sleep", "academic_performance", 
            "physical_activity", "stress_level", "anxiety_level", 
            "addiction_level", "depression_label", "addiction_score"
        ]
        # Keep only existing columns to be resilient
        corr_cols = [c for c in corr_cols if c in filtered_df.columns]
        corr_matrix = filtered_df[corr_cols].corr()
        
        fig_heatmap = px.imshow(
            corr_matrix,
            labels=dict(x="Clinical Feature", y="Clinical Feature", color="Pearson r"),
            x=corr_matrix.columns,
            y=corr_matrix.index,
            color_continuous_scale="RdBu_r",
            zmin=-1, zmax=1,
            title="Feature Correlation Matrix",
            template="plotly_dark"
        )
        fig_heatmap.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_family='Plus Jakarta Sans'
        )
        st.plotly_chart(fig_heatmap, use_container_width=True)
        
    with col_chart_4:
        st.markdown("<div class='glass-card'><h4>📉 Sleep & Academic Performance Relationship</h4></div>", unsafe_allow_html=True)
        
        fig_gpa = px.box(
            filtered_df,
            x="stress_level",
            y="academic_performance",
            color="depression_label",
            color_discrete_map={0: "#00f2fe", 1: "#ef4444"},
            labels={
                "stress_level": "Stress Level (1-10)",
                "academic_performance": "Academic Performance (GPA)",
                "depression_label": "Depression Flag"
            },
            title="Impact of Elevated Stress and Depression on GPA Performance",
            template="plotly_dark"
        )
        fig_gpa.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_family='Plus Jakarta Sans'
        )
        st.plotly_chart(fig_gpa, use_container_width=True)
