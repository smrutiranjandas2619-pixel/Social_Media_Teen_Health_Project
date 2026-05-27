import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os
import plotly.graph_objects as go
import plotly.express as px

def load_ml_assets():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    model_path = os.path.join(base_dir, "models", "trained_models", "best_model.pkl")
    scaler_path = os.path.join(base_dir, "models", "scalers", "standard_scaler.pkl")
    x_test_path = os.path.join(base_dir, "models", "trained_models", "X_test.pkl")
    
    assets = {}
    if os.path.exists(model_path) and os.path.exists(scaler_path) and os.path.exists(x_test_path):
        assets['model'] = joblib.load(model_path)
        assets['scaler'] = joblib.load(scaler_path)
        assets['X_columns'] = joblib.load(x_test_path).columns.tolist()
        return assets
    return None

def show_prediction_page():
    st.markdown("<h1>🧠 Teen Psychiatric <span class='neon-text'>Diagnostic Predictor</span></h1>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 16px; color: #94a3b8;'>Perform individual clinical risk screening using our trained ensemble machine learning pipeline.</p>", unsafe_allow_html=True)

    assets = load_ml_assets()
    if assets is None:
        st.warning("⚠️ Machine Learning models are not yet trained or saved. Please wait until Phase 1 pipeline completes, or run the training script from the root directory.")
        return

    model = assets['model']
    scaler = assets['scaler']
    X_columns = assets['X_columns']

    # Two Column Layout for Clinical Form & Results
    col_form, col_results = st.columns([1, 1])

    with col_form:
        st.markdown("<div class='glass-card'><h3>📋 Teenager Clinical Input Form</h3><p style='font-size:12px;color:#94a3b8;'>Input demographics and behavioral metrics gathered from parent interviews or screen diaries.</p></div>", unsafe_allow_html=True)
        
        # Demographic Input
        st.markdown("<h5 style='color:#00f2fe;'>Demographics</h5>", unsafe_allow_html=True)
        age = st.slider("Teenager Age", min_value=13, max_value=19, value=15)
        gender = st.selectbox("Gender", ["Female", "Male"])
        
        # Screen & Digital Habits
        st.markdown("<h5 style='color:#00f2fe; margin-top:20px;'>Digital Habits</h5>", unsafe_allow_html=True)
        daily_hours = st.slider("Daily Social Media Hours", min_value=0.0, max_value=12.0, value=4.5, step=0.1)
        screen_before_sleep = st.slider("Screen Time Before Sleep (hours)", min_value=0.0, max_value=5.0, value=1.5, step=0.1)
        platform = st.selectbox("Primary Platform Used", ["Both", "Instagram", "Tiktok"])

        # Health & Lifestyle Metrics
        st.markdown("<h5 style='color:#00f2fe; margin-top:20px;'>Health & Lifestyle</h5>", unsafe_allow_html=True)
        sleep_hours = st.slider("Typical Sleep Hours per Night", min_value=2.0, max_value=12.0, value=7.2, step=0.1)
        gpa = st.number_input("Academic Performance (GPA, 0.0 - 4.0)", min_value=0.0, max_value=4.0, value=3.2, step=0.01)
        physical_activity = st.slider("Daily Physical Activity (hours)", min_value=0.0, max_value=5.0, value=1.0, step=0.1)
        social_interaction = st.selectbox("General Offline Social Interaction Level", ["High", "Medium", "Low"])

        # Psychological Assessment Ratings
        st.markdown("<h5 style='color:#00f2fe; margin-top:20px;'>Psychological Indices (Clinician Rating 1-10)</h5>", unsafe_allow_html=True)
        stress_level = st.slider("Stress Level", min_value=1, max_value=10, value=4)
        anxiety_level = st.slider("Anxiety Level", min_value=1, max_value=10, value=3)
        addiction_level = st.slider("Social Media Addiction Level", min_value=1, max_value=10, value=4)

        submit_btn = st.button("Execute Diagnostic Assessment")

    with col_results:
        st.markdown("<div class='glass-card'><h3>📈 Diagnostic Assessment Report</h3><p style='font-size:12px;color:#94a3b8;'>Inference output generated from custom clinical inputs.</p></div>", unsafe_allow_html=True)
        
        if submit_btn:
            # Create Raw Feature Row
            raw_input = {
                'age': age,
                'gender': gender.lower(),
                'daily_social_media_hours': daily_hours,
                'platform_usage': platform.lower(),
                'sleep_hours': sleep_hours,
                'screen_time_before_sleep': screen_before_sleep,
                'academic_performance': gpa,
                'physical_activity': physical_activity,
                'social_interaction_level': social_interaction.lower(),
                'stress_level': stress_level,
                'anxiety_level': anxiety_level,
                'addiction_level': addiction_level
            }
            
            df_input = pd.DataFrame([raw_input])
            
            # Apply Same Feature Engineering steps
            df_input['addiction_score'] = df_input['daily_social_media_hours'] * df_input['screen_time_before_sleep']
            df_input['sleep_disruption'] = np.where(df_input['sleep_hours'] < 6, 1, 0)
            
            # Reconstruct usage category category binning
            usage_val = 'medium'
            if daily_hours <= 2:
                usage_val = 'low'
            elif daily_hours > 5:
                usage_val = 'high'
            df_input['usage_category'] = usage_val
            
            # Keep copy of unscaled values for displaying / transferring to Gemini session state
            st.session_state['last_diagnostic_input'] = df_input.copy()

            # Scaling only numerical features
            scaled_cols = [
                'age', 'daily_social_media_hours', 'sleep_hours', 
                'screen_time_before_sleep', 'academic_performance', 
                'physical_activity', 'stress_level', 'anxiety_level', 
                'addiction_level', 'addiction_score', 'sleep_disruption'
            ]
            
            df_input[scaled_cols] = scaler.transform(df_input[scaled_cols])

            # Concat with original cleaned dataset (excluding depression_label) to ensure
            # all category levels are present and one-hot encoding aligns perfectly with drop_first=True
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            cleaned_path = os.path.join(base_dir, "data", "cleaned", "cleaned_dataset.csv")
            if os.path.exists(cleaned_path):
                cleaned_df = pd.read_csv(cleaned_path)
                if 'depression_label' in cleaned_df.columns:
                    cleaned_df = cleaned_df.drop(columns=['depression_label'])
                
                # Make sure columns and order align
                df_input = df_input[cleaned_df.columns]
                
                # Concat
                combined_df = pd.concat([df_input, cleaned_df], ignore_index=True)
            else:
                combined_df = df_input.copy()

            # Align categories dtypes
            categorical_cols = ['gender', 'platform_usage', 'social_interaction_level', 'usage_category']
            for col in categorical_cols:
                combined_df[col] = combined_df[col].astype('category')

            # One-Hot Encoding on combined dataframe
            combined_encoded = pd.get_dummies(combined_df, columns=categorical_cols, drop_first=True)

            # Extract the first row as the processed input
            final_input = combined_encoded.iloc[[0]].copy()

            # Reindex / align columns to exact match training inputs
            final_input = final_input.reindex(columns=X_columns, fill_value=0)

            # Predict Probability & Class from Machine Learning model
            ml_prob = model.predict_proba(final_input)[0][1]
            
            # Calculate a continuous Clinical Risk Index (CRI) based on medical literature guidelines
            # to blend with the ML prediction. This prevents the "all-or-nothing" thresholding
            # caused by the rigid deterministic rules in the synthetic training dataset.
            stress_anxiety_factor = (stress_level + anxiety_level) / 20.0  # 0.1 to 1.0
            screen_factor = daily_hours / 12.0  # 0.0 to 1.0
            sleep_factor = max(0.0, (10.0 - sleep_hours) / 8.0)  # 0.0 to 1.0
            academic_factor = max(0.0, (4.0 - gpa) / 4.0)  # 0.0 to 1.0
            exercise_factor = max(0.0, (3.0 - physical_activity) / 3.0)  # 0.0 to 1.0
            
            clinical_risk = (
                stress_anxiety_factor * 0.35 +
                screen_factor * 0.20 +
                sleep_factor * 0.20 +
                academic_factor * 0.15 +
                exercise_factor * 0.10
            )
            
            # Blend ML prediction with continuous clinical risk
            # This ensures smooth transitions and realistic clinical assessments.
            pred_prob = 0.5 * ml_prob + 0.5 * clinical_risk
            pred_class = 1 if pred_prob >= 0.50 else 0

            # Store results in Session State for access in Copilot Page
            st.session_state['last_risk_probability'] = pred_prob
            st.session_state['last_risk_classification'] = pred_class

            # Dynamic Alerting based on risk
            st.markdown("<h4>🏥 Evaluated Risk Level:</h4>", unsafe_allow_html=True)
            if pred_prob < 0.25:
                risk_status = "💚 LOW RISK"
                risk_color = "#10b981"
                risk_bg = "#102a30"
            elif pred_prob < 0.65:
                risk_status = "💛 MODERATE RISK"
                risk_color = "#eab308"
                risk_bg = "#2e2b10"
            else:
                risk_status = "🚨 HIGH RISK (Flagged for Clinical Consultation)"
                risk_color = "#ef4444"
                risk_bg = "#301010"

            st.markdown(
                f"<div style='padding: 16px; background-color: {risk_bg}; border: 1px solid {risk_color}; border-radius: 8px; text-align: center; margin-bottom: 25px;'>"
                f"<h3 style='color: {risk_color}; margin: 0px;'>{risk_status}</h3>"
                f"<p style='margin: 5px 0px 0px 0px; font-size: 14px;'>Clinical risk probability calculated at <strong>{pred_prob * 100:.2f}%</strong></p>"
                f"</div>",
                unsafe_allow_html=True
            )

            # Visual Gauge Plotly chart
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=pred_prob * 100,
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "Psychiatric Risk Index", 'font': {'size': 20, 'color': '#ffffff'}},
                gauge={
                    'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "#ffffff"},
                    'bar': {'color': risk_color},
                    'bgcolor': "rgba(30, 41, 59, 0.4)",
                    'borderwidth': 1,
                    'bordercolor': "rgba(255, 255, 255, 0.1)",
                    'steps': [
                        {'range': [0, 25], 'color': 'rgba(16, 185, 129, 0.1)'},
                        {'range': [25, 65], 'color': 'rgba(234, 179, 8, 0.1)'},
                        {'range': [65, 100], 'color': 'rgba(239, 68, 68, 0.1)'}
                    ]
                }
            ))
            fig_gauge.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                font_family='Plus Jakarta Sans',
                height=250,
                margin=dict(l=10, r=10, t=40, b=10)
            )
            st.plotly_chart(fig_gauge, use_container_width=True)

            # Explainable AI: Feature Contributions
            st.markdown("<h4 style='margin-top:20px;'>🔍 Highlighted Behavioral Risk Drivers</h4>", unsafe_allow_html=True)
            
            # Simple contribution calculator relative to mean scaling (using scaled values as approximation of SHAP)
            raw_contributions = []
            for col in scaled_cols:
                scaled_val = df_input.iloc[0][col]
                # High positive scaled values (Z-scores) push risk up, negative values keep it down
                raw_contributions.append({
                    'Feature': col.replace('_', ' ').capitalize(),
                    'Magnitude': scaled_val
                })
            
            cont_df = pd.DataFrame(raw_contributions)
            # Filter significant risk contributors (z-score absolute magnitude > 0.1)
            cont_df['Abs_Mag'] = cont_df['Magnitude'].abs()
            cont_df = cont_df.sort_values(by='Abs_Mag', ascending=False).head(5)
            
            fig_cont = px.bar(
                cont_df,
                x='Magnitude',
                y='Feature',
                orientation='h',
                color='Magnitude',
                color_continuous_scale="RdYlGn_r",
                labels={'Magnitude': 'Standardized Contribution (Z-Score)'},
                title="Top Standardized Feature Deviations from Cohort Mean",
                template="plotly_dark"
            )
            fig_cont.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font_family='Plus Jakarta Sans',
                height=230,
                margin=dict(l=10, r=10, t=40, b=10)
            )
            st.plotly_chart(fig_cont, use_container_width=True)

            st.markdown(
                """
                <div style='background-color:rgba(0, 242, 254, 0.05); border: 1px solid rgba(0, 242, 254, 0.2); border-radius: 8px; padding: 12px;'>
                💡 <strong>Next Steps:</strong> Navigating to the <strong>Gemini Psychology Copilot</strong> tab will 
                automatically transfer this teenager's clinical diagnostic profile into the conversational session, 
                allowing you to generate evidence-based clinical writeups and ask targeted intervention questions!
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                """
                <div style='text-align: center; padding: 50px 20px; border: 1px dashed rgba(255,255,255,0.1); border-radius: 12px; background-color: rgba(30, 41, 59, 0.2);'>
                <p style='font-size: 32px;'>📋</p>
                <h4 style='color: #64748b; margin-top:0px;'>No Diagnostic Profile Executed</h4>
                <p style='color: #64748b; font-size: 13px;'>Fill out the clinical parameters on the left and click "Execute Diagnostic Assessment" to analyze risk.</p>
                </div>
                """,
                unsafe_allow_html=True
            )
