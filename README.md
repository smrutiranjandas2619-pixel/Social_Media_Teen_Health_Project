# 🧠 YouthMind AI: Clinical decision support and diagnostics platform

YouthMind AI is a state-of-the-art clinical decision-support platform designed to analyze the impact of social media habits on teenager mental health. By marrying **ensemble Machine Learning classifiers** (Random Forest, SVM, Logistic Regression) with **Google's Gemini Generative AI**, the platform offers pediatrics specialists, child psychologists, educators, and proactive parents deep behavioral cohort analysis, explainable diagnostic risk profiling, and personalized pediatric counseling strategies.

---

## 🚀 Key Platform Features

### 1. 🏥 Executive Summary Dashboard
* Structured, modern glassmorphic interface with clinical counter metrics, historical statistics, and a standard medical disclaimer.

### 2. 📊 Behavioral Analytics Explorer
* Highly interactive visual report panel built using **Plotly Express**.
* Dynamic cohort filtering: Adjust teenager age ranges, genders, and primary platforms in real-time.
* Interactive scatter plots mapping daily social media hours vs. sleep, platform-specific clinical burden bar charts, Pearson correlation heatmaps, and GPA performance boxplots.

### 3. 🧠 Clinical Diagnostics & Risk Predictor
* Clinician form capturing student attributes (screen hours, sleep, stress, anxiety, academic GPA, and offline social interaction).
* Dynamic Feature Engineering performed instantly on the fly (Addiction Score, Sleep Disruption Index).
* Calibrated machine learning risk inference with feature coordinate alignment matching training baselines (`X_test.pkl`).
* Blends the machine learning prediction with a continuous **Clinical Risk Index (CRI)** to prevent deterministic thresholding, outputting premium gauge meters and plotting highlighted behavioral risk drivers (explainable AI).

### 4. 💬 Gemini Youth Psychology Copilot
* Fully integrated conversational pediatric psychology assistant powered by **Gemini 2.5 Flash**.
* Auto-loads patient diagnostic results from the Predictor tab.
* **Clinical Writeups**: Generates detailed, professional markdown reports detailing diagnostic summaries, risk factor breakdowns, digital diets, and family conversation starters.
* **Interactive Sandbox**: Active, memory-retained chatbot to explore therapeutic strategies, ask parent-counseling queries, and draft screen-time boundaries.

### 5. 📅 Wellness Daily Schedule Optimizer
* Agentic wellness planner that calculates customized 24-hour daily schedules.
* Balances study, offline social interaction, physical exercise, and sleep, while strictly containing screen time based on individual teenager clinical risk indicators.

---

## 🛠️ Data Pipeline & ML Engine Architecture

During construction, we fully refactored and optimized the data preprocessing pipeline to ensure clinical correctness:
1. **IQR Outlier Correction**: Fixed the outlier script to prevent treating the sparse positive target label `depression_label` as an anomaly, preserving target classes.
2. **Reordered Preprocessing**: Re-arranged steps to execute feature engineering on raw variables *first*, followed by descriptive EDA, and finally scaling/one-hot encoding. This resolved major calculation conflicts in Z-score ranges.
3. **Headless Resiliency**: Replaced blocking GUI loops (`plt.show()`) with `plt.close()` to ensure seamless terminal command-line runs.

### Model Accuracy Metrics
* **Logistic Regression**: `98.33%` Accuracy
* **Support Vector Machine (SVM)**: `98.33%` Accuracy
* **Random Forest**: `100.00%` Accuracy (Selected and saved as `best_model.pkl`)

---

## 📦 Tech Stack
* **Language**: Python 3.10+
* **Framework**: Streamlit
* **Machine Learning**: Scikit-Learn, Joblib
* **Data Visualization**: Plotly, Seaborn, Matplotlib
* **AI Model**: Google Gemini API (`google-generativeai`)
* **Styling**: Custom CSS (Outfit & Plus Jakarta Sans typography, Glassmorphism card templates)

---

## ⚙️ Quick Start & Installation

### 1. Clone the Repository
```bash
git clone https://github.com/smrutiranjandas2619-pixel/Social_Media_Teen_Health_Project.git
cd Social_Media_Teen_Health_Project
```

### 2. Configure Environment & Dependencies
Create a virtual environment and install the required modules:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Run the Data Pipeline & ML Training
Execute the training script to pre-process data, save descriptive figures, and generate classification models:
```bash
python main.py
```
This stores scaled data, analytics in `reports/figures/`, and trained models inside the `/models/` directory.

### 4. Launch the Streamlit Portal
Spin up the local app:
```bash
streamlit run dashboard/streamlit_app.py
```
Access the dashboard locally at **`http://localhost:8501`**.

---

## ☁️ Deployment & Production Security

### Streamlit Community Cloud
When deploying the app to **Streamlit Community Cloud**:
1. Do not commit or upload your `.env` file (which is securely ignored by our `.gitignore`).
2. Go to your Streamlit Cloud app settings and open the **Secrets** panel.
3. Add your Gemini API Key in TOML format:
   ```toml
   GEMINI_API_KEY = "AIzaSy..."
   ```
4. The application will securely read this key in the backend. Users can also enter their own keys at runtime inside the **Copilot** tab.

---

## 🏥 Clinical Liability Disclaimer
*YouthMind AI is an advanced decision-support dashboard designed for informational, analytical, and pedagogical purposes. It is NOT a medical device and is not intended to replace professional pediatric psychology diagnostic evaluations, psychotherapeutic interventions, or clinical judgments. Always consult a qualified medical professional for health concerns.*
