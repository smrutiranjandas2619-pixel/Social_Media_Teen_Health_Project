import streamlit as st
import os
import google.generativeai as genai

def get_gemini_client():
    # Load from environment variables (populated globally from .env in startup)
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key:
        try:
            genai.configure(api_key=api_key)
            # Use gemini-2.5-flash as the fast, standard model
            return genai.GenerativeModel("gemini-2.5-flash")
        except Exception as e:
            st.error(f"Failed to configure Gemini Client: {e}")
    return None

def show_copilot_page():
    st.markdown("<h1>💬 Gemini Youth <span class='neon-text'>Psychology Copilot</span></h1>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 16px; color: #94a3b8;'>Consult our Google Gemini clinical assistant for diagnostic write-ups and parenting/therapeutic screen strategies.</p>", unsafe_allow_html=True)

    model = get_gemini_client()
    if model is None:
        st.markdown(
            """
            <div class='glass-card' style='border-color: rgba(239, 68, 68, 0.3);'>
                <h4 style='color: #ef4444; margin-top: 0px;'>⚠️ Backend Generative AI API Key Not Configured</h4>
                <p style='font-size: 13px; color: #cbd5e1;'>The Gemini Clinical Copilot requires a Google AI Studio API Key to be configured in the backend. 
                Please contact the platform administrator to add the <code>GEMINI_API_KEY</code> inside the project <code>.env</code> file.</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        return

    # Two column layout: Left for Diagnostic Profile Report, Right for Dynamic Chat
    col_report, col_chat = st.columns([1, 1])

    # Dynamic diagnostic profile load
    df_diag = st.session_state.get('last_diagnostic_input')
    risk_prob = st.session_state.get('last_risk_probability')
    risk_class = st.session_state.get('last_risk_classification')

    with col_report:
        st.markdown("<div class='glass-card'><h3>📝 Automated Clinical Writeup</h3><p style='font-size:12px;color:#94a3b8;'>Generate complete psychotherapeutic screen-diet reports based on individual risk scores.</p></div>", unsafe_allow_html=True)

        if df_diag is not None:
            # Display summary of active diagnostic load
            st.markdown(
                f"<div style='background-color: rgba(0, 242, 254, 0.05); border: 1px solid rgba(0,242,254,0.15); border-radius: 8px; padding: 15px; margin-bottom: 20px;'>"
                f"<h5 style='color: #00f2fe; margin-top: 0px; margin-bottom: 8px;'>📥 Diagnostic Session Profile Loaded:</h5>"
                f"<ul>"
                f"<li><strong>Demographics:</strong> {df_diag.iloc[0]['age']}-year-old {df_diag.iloc[0]['gender'].capitalize()}</li>"
                f"<li><strong>Calculated Risk Probability:</strong> {risk_prob * 100:.1f}% (Class {risk_class})</li>"
                f"<li><strong>Social Media Usage:</strong> {df_diag.iloc[0]['daily_social_media_hours']:.1f} hrs/day ({df_diag.iloc[0]['platform_usage'].upper()})</li>"
                f"<li><strong>Sleep Duration:</strong> {df_diag.iloc[0]['sleep_hours']:.1f} hrs/night (Pre-sleep screen: {df_diag.iloc[0]['screen_time_before_sleep']:.1f} hrs)</li>"
                f"<li><strong>Clinical Indicators (1-10):</strong> Stress: {df_diag.iloc[0]['stress_level']}, Anxiety: {df_diag.iloc[0]['anxiety_level']}, Addiction: {df_diag.iloc[0]['addiction_level']}</li>"
                f"</ul>"
                f"</div>",
                unsafe_allow_html=True
            )

            writeup_btn = st.button("🪄 Generate AI Clinical Recommendation Plan")

            if writeup_btn:
                # Construct detailed clinical prompt
                clinical_prompt = f"""
                You are playing the role of an expert Pediatric Clinical Psychologist and Youth Digital Wellness Counselor. 
                An individual teenager has been flagged through a screen diagnostic dashboard, and you need to write a highly detailed, 
                professional, evidence-based Clinical Recommendation and Intervention Plan for their parents and educators.
                
                Teenager Cohort Profile:
                - Age: {df_diag.iloc[0]['age']} years old
                - Gender: {df_diag.iloc[0]['gender']}
                - Daily Social Media Hours: {df_diag.iloc[0]['daily_social_media_hours']} hours per day on {df_diag.iloc[0]['platform_usage']}
                - Sleep Hours: {df_diag.iloc[0]['sleep_hours']} hours per night (with {df_diag.iloc[0]['screen_time_before_sleep']} hours of active screen time right before sleep)
                - Academic Performance (GPA): {df_diag.iloc[0]['academic_performance']}/4.00
                - Physical Activity: {df_diag.iloc[0]['physical_activity']} hours per day
                - General Offline Social Interaction Level: {df_diag.iloc[0]['social_interaction_level']}
                - Clinician-Rated Indicators (Scale 1-10): Stress Level: {df_diag.iloc[0]['stress_level']}, Anxiety Level: {df_diag.iloc[0]['anxiety_level']}, Social Media Addiction Rating: {df_diag.iloc[0]['addiction_level']}
                - Machine Learning Calculated Depression Risk: {risk_prob * 100:.2f}% (Diagnostic Threshold Category: {"High Risk" if risk_prob > 0.65 else ("Moderate Risk" if risk_prob > 0.25 else "Low Risk")})

                Please write an exhaustive write-up with the following specific sections (in markdown format, professional, empathetic, and highly actionable):
                1. 📋 Clinical Summary & Impression
                   - Synthesize the data. Highlight the relationships between their screen hours, pre-sleep screen exposure, sleep deprivation, stress, and anxiety.
                2. 🧠 Psychological Risk Factor Breakdown
                   - Pinpoint which variables represent the greatest risk vectors for this teen (e.g. sleep deprivation vs social media addiction vs lack of physical movement).
                3. 🚫 Structured Screen-Time Restrictions & Boundaries
                   - Prescribe structured, healthy digital rules specific to this teen's platform usage and hours.
                4. 🛌 Sleep Hygiene & Routine Interventions
                   - Specific guidelines to address screen usage before bed and rebuild restorative sleep patterns.
                5. 🏫 School & Academic Support Plan
                   - Recommendations to mitigate the stress of GPA drops and handle test anxiety.
                6. 💬 Family & Parenting Conversation Starters
                   - 3 highly specific, empathetic prompts parents can use to open positive dialogue with this teenager.
                """

                with st.spinner("Analyzing profile and generating pediatric psychology plan..."):
                    try:
                        response = model.generate_content(clinical_prompt)
                        st.markdown("<div class='glass-card'><h4>💡 Clinical Write-Up Results:</h4></div>", unsafe_allow_html=True)
                        st.markdown(response.text)
                        
                        # Provide text area option to copy
                        st.text_area("Copy Report Markdown", value=response.text, height=200)
                    except Exception as e:
                        st.error(f"Error calling Gemini: {e}")
        else:
            st.markdown(
                """
                <div style='text-align: center; padding: 50px 20px; border: 1px dashed rgba(255,255,255,0.1); border-radius: 12px; background-color: rgba(30, 41, 59, 0.2);'>
                <p style='font-size: 32px;'>📥</p>
                <h4 style='color: #64748b; margin-top:0px;'>No Diagnostic Load Active</h4>
                <p style='color: #64748b; font-size: 13px;'>Navigate to the <strong>Teen Diagnostic Predictor</strong>, enter attributes, and execute a diagnostic prediction to auto-generate reports here.</p>
                </div>
                """,
                unsafe_allow_html=True
            )

    with col_chat:
        st.markdown("<div class='glass-card'><h3>💬 Interactive Counselor Sandbox</h3><p style='font-size:12px;color:#94a3b8;'>Ask specialized parenting queries, request therapeutic guidelines, or explore custom scenarios.</p></div>", unsafe_allow_html=True)

        # Initialize chat history if not present
        if 'chat_history' not in st.session_state:
            st.session_state['chat_history'] = [
                {"role": "assistant", "content": "Hello! I am your Youth Psychology AI Assistant. I am trained in digital pediatric wellness and clinical youth psychology. How can I assist you with teenager digital diets or mental health strategies today?"}
            ]

        # Display Chat History
        chat_container = st.container(height=450)
        with chat_container:
            for msg in st.session_state['chat_history']:
                if msg["role"] == "assistant":
                    st.chat_message("assistant", avatar="🧠").write(msg["content"])
                else:
                    st.chat_message("user", avatar="👤").write(msg["content"])

        # Input query
        user_query = st.chat_input("Type your counseling query here...")

        if user_query:
            # Append user message
            st.session_state['chat_history'].append({"role": "user", "content": user_query})
            
            # Formulate chat context
            system_context = """
            You are playing the role of an expert Pediatric Clinical Psychologist and Youth Digital Wellness Counselor. 
            You are discussing parenting strategies, screen-time contracts, adolescent sleep hygiene, school stress, and adolescent depression/anxiety. 
            Respond with professional, scientific, highly empathetic, and practical clinical counseling advice. Maintain the safety of the conversation (no explicit self-harm instructions; if severe depression is mentioned, always advise immediate consulting of a physical child psychologist).
            """
            
            # Format chat history for Gemini input
            chat_context = f"{system_context}\n\n"
            # Limit history to last 6 messages to keep tokens low and responses fast
            for msg in st.session_state['chat_history'][-6:]:
                chat_context += f"{msg['role'].upper()}: {msg['content']}\n"
            chat_context += "ASSISTANT:"

            with st.spinner("Formulating guidance..."):
                try:
                    response = model.generate_content(chat_context)
                    ans_text = response.text
                    
                    st.session_state['chat_history'].append({"role": "assistant", "content": ans_text})
                    st.rerun()
                except Exception as e:
                    st.error(f"Error calling Gemini in chat: {e}")

        # Clear chat option
        if st.button("Clear Conversation"):
            st.session_state['chat_history'] = [
                {"role": "assistant", "content": "Conversation cleared. Hello! I am your Youth Psychology AI Assistant. How can I assist you today?"}
            ]
            st.rerun()
