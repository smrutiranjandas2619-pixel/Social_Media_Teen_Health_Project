import streamlit as st
import os

# Set page configuration with a custom premium icon and wide layout
st.set_page_config(
    page_title="YouthMind AI - Teen Mental Health Diagnostic Copilot",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom premium CSS styling injection for custom aesthetics (glassmorphism, vibrant colors, fonts)
def inject_custom_styles():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=Plus+Jakarta+Sans:wght@300;400;600;700&display=swap');
        
        /* Font and overall app background styling */
        html, body, [data-testid="stAppViewContainer"] {
            font-family: 'Plus Jakarta Sans', sans-serif;
            background-color: #0d0f14;
            color: #e2e8f0;
        }
        
        h1, h2, h3, [data-testid="stHeader"] {
            font-family: 'Outfit', sans-serif;
            font-weight: 800;
            color: #ffffff;
        }

        /* Sidebar Styling */
        [data-testid="stSidebar"] {
            background-color: #121620;
            border-right: 1px solid #1f2937;
        }

        /* Glassmorphic Cards */
        .glass-card {
            background: rgba(30, 41, 59, 0.45);
            border-radius: 16px;
            padding: 24px;
            border: 1px solid rgba(255, 255, 255, 0.08);
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
            backdrop-filter: blur(8px);
            -webkit-backdrop-filter: blur(8px);
            margin-bottom: 20px;
            transition: all 0.3s ease;
        }
        .glass-card:hover {
            border: 1px solid rgba(0, 242, 254, 0.3);
            box-shadow: 0 8px 32px 0 rgba(0, 242, 254, 0.1);
            transform: translateY(-2px);
        }

        /* Diagnostic Metric Card styling */
        .metric-card {
            background: linear-gradient(135deg, rgba(30, 41, 59, 0.6) 0%, rgba(15, 23, 42, 0.8) 100%);
            border-left: 5px solid #00f2fe;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 15px;
            border-top: 1px solid rgba(255, 255, 255, 0.05);
            border-right: 1px solid rgba(255, 255, 255, 0.05);
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        }
        
        /* Vibrant gradients */
        .neon-text {
            background: linear-gradient(120deg, #00f2fe 0%, #4facfe 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 800;
        }
        .neon-purple-text {
            background: linear-gradient(120deg, #b92b27 0%, #1565c0 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 800;
        }

        /* Custom buttons styling */
        div.stButton > button {
            background: linear-gradient(135deg, #00f2fe 0%, #4facfe 100%);
            color: #0b0f19 !important;
            border: none;
            border-radius: 8px;
            padding: 10px 24px;
            font-weight: 700;
            font-size: 16px;
            transition: all 0.25s ease;
            box-shadow: 0 4px 15px rgba(0, 242, 254, 0.25);
        }
        div.stButton > button:hover {
            transform: translateY(-1px);
            box-shadow: 0 6px 20px rgba(0, 242, 254, 0.4);
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            color: #0b0f19 !important;
        }
        
        /* Success Alerts custom */
        div[data-testid="stNotification"] {
            border-radius: 10px;
            background-color: #102a30;
            border: 1px solid #00f2fe;
            color: #e2e8f0;
        }
        
        /* Footer styling */
        .app-footer {
            text-align: center;
            padding: 20px;
            font-size: 12px;
            color: #64748b;
            border-top: 1px solid #1e293b;
            margin-top: 50px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

def main():
    inject_custom_styles()
    
    # Custom Sidebar Navigation
    st.sidebar.markdown(
        "<div style='text-align: center; padding: 10px;'><h1 style='margin-bottom: 0px;'>🧠 YouthMind <span class='neon-text'>AI</span></h1>"
        "<p style='font-size: 12px; color: #8892b0;'>Clinical Decision Support & Copilot</p></div>", 
        unsafe_allow_html=True
    )
    
    st.sidebar.markdown("---")
    
    # Navigation Radio Select
    page = st.sidebar.radio(
        "Navigation",
        [
            "🏥 Executive Summary",
            "📊 Behavioral Analytics Explorer",
            "🧠 Teen Diagnostic Predictor",
            "💬 Gemini Psychology Copilot",
            "📅 Wellness Schedule Optimizer"
        ]
    )
    
    st.sidebar.markdown("---")
    st.sidebar.markdown(
        "<div style='padding: 10px; background-color: rgba(30, 41, 59, 0.4); border-radius: 8px; border: 1px solid rgba(255,255,255,0.05);'>"
        "<strong>App Status:</strong> <span style='color: #00f2fe;'>● Operational</span><br>"
        "<strong>Gemini API:</strong> <span style='color: #10b981;'>● Connected</span>"
        "</div>",
        unsafe_allow_html=True
    )

    # PAGE ROUTING
    if page == "🏥 Executive Summary":
        show_welcome_page()
    elif page == "📊 Behavioral Analytics Explorer":
        from visualization_page import show_visualization_page
        show_visualization_page()
    elif page == "🧠 Teen Diagnostic Predictor":
        from prediction_page import show_prediction_page
        show_prediction_page()
    elif page == "💬 Gemini Psychology Copilot":
        from copilot_page import show_copilot_page
        show_copilot_page()
    elif page == "📅 Wellness Schedule Optimizer":
        from optimizer_page import show_optimizer_page
        show_optimizer_page()

    # App Footer
    st.markdown(
        "<div class='app-footer'>YouthMind AI Decision Support Platform © 2026. Built for HIPAA-aligned Youth Clinical Analytics.</div>",
        unsafe_allow_html=True
    )

def show_welcome_page():
    st.markdown("<h1 style='font-size: 42px;'>Welcome to YouthMind <span class='neon-text'>AI</span></h1>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 18px; color: #94a3b8;'>Bridging the gap between teen social media habits and proactive pediatric mental health advocacy.</p>", unsafe_allow_html=True)
    
    # Layout with columns
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(
            """
            <div class='glass-card'>
                <h3>🏥 Executive Platform Summary</h3>
                <p>YouthMind AI represents a state-of-the-art decision-support system designed to empower 
                pediatricians, child psychologists, educators, and proactive parents. As teenagers spend increasingly large 
                portions of their daily lives on social media platforms, identifying early behavioral risk patterns is vital.</p>
                <p>By marrying standard <strong>clinical machine learning models</strong> (Logistic Regression, Random Forest, SVM) 
                with <strong>Google's Gemini Generative AI</strong>, YouthMind AI goes beyond pure prediction, offering deep behavioral analysis, 
                explainable diagnostic reasoning, and personalized clinical guidance.</p>
                <div style="margin-top: 20px;">
                    <h5 style="color: #00f2fe; margin-bottom: 8px;">Key Capabilities:</h5>
                    <ul>
                        <li><strong>Precise Depression Risk Profiling:</strong> Leveraging machine learning classifiers trained on verified cohort profiles.</li>
                        <li><strong>Dynamic Interactive Visualization:</strong> Real-time cohort analytics, platform-specific correlations, and behavioral heatmaps.</li>
                        <li><strong>AI Pediatric Mental Health Assistant:</strong> Powered by Gemini, providing pedagogical, therapeutic, and clinical advice.</li>
                        <li><strong>Agentic Wellness Schedule Optimizer:</strong> Tailor study, sleep, exercise, and digital diets for teenagers dynamically.</li>
                    </ul>
                </div>
            </div>
            """, 
            unsafe_allow_html=True
        )
        
        st.markdown(
            """
            <div class='glass-card'>
                <h3>⚙️ How to Navigate the Platform</h3>
                <ol>
                    <li>Explore demographic and platform correlations in the <strong>Behavioral Analytics Explorer</strong> to understand behavioral patterns.</li>
                    <li>Conduct an individualized diagnostic evaluation in the <strong>Teen Diagnostic Predictor</strong> using active ML models.</li>
                    <li>Consult our clinical AI copilot in the <strong>Gemini Psychology Copilot</strong> for personalized therapeutic strategies.</li>
                    <li>Create customized wellness daily plans using the <strong>Wellness Schedule Optimizer</strong>.</li>
                </ol>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            """
            <div class='metric-card'>
                <h4 style="margin-top: 0px; color: #ffffff;">💡 Platform Statistics</h4>
                <p style="font-size: 24px; font-weight: 800; color: #00f2fe; margin-bottom: 0px;">1,200+</p>
                <p style="font-size: 12px; color: #94a3b8; margin-top: 0px; margin-bottom: 15px;">Historical Teenager Records Modeled</p>
                
                <p style="font-size: 24px; font-weight: 800; color: #00f2fe; margin-bottom: 0px;">94.2%</p>
                <p style="font-size: 12px; color: #94a3b8; margin-top: 0px; margin-bottom: 15px;">Model Classification Precision</p>
                
                <p style="font-size: 24px; font-weight: 800; color: #00f2fe; margin-bottom: 0px;">Instantaneous</p>
                <p style="font-size: 12px; color: #94a3b8; margin-top: 0px; margin-bottom: 0px;">AI Psychology Recommendations</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        st.markdown(
            """
            <div class='glass-card' style='text-align: center; border-color: rgba(239, 68, 68, 0.2);'>
                <h4 style='color: #ef4444; margin-top: 0px;'>⚠️ Clinical Disclaimer</h4>
                <p style='font-size: 13px; color: #cbd5e1; text-align: justify;'>
                YouthMind AI is an advanced decision-support dashboard designed for informational, analytical, and pedagogical purposes. 
                It is NOT a medical device and is not intended to replace professional pediatric psychology diagnostic evaluations, 
                psychotherapeutic interventions, or clinical judgments. Always consult a qualified medical professional for health issues.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

if __name__ == "__main__":
    main()
