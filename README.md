# 🚀 Customer Churn Intelligence AI

Predict • Explain • Act — Smart Retention Insights


##📌 Overview:

Customer Churn Intelligence AI is a production-ready machine learning application designed to help businesses predict, understand, and reduce customer churn.

It combines:

📊 Predictive Modeling
🔍 Explainable AI (SHAP)
🤖 AI-driven Business Insights

to transform raw customer data into actionable retention strategies.

##🧠 Problem Statement:

Customer churn directly impacts revenue and growth.
Most businesses struggle with:

Identifying at-risk customers early
Understanding why customers leave
Taking timely and effective action

👉 This project solves all three.

##💡 Solution:

This system provides an end-to-end churn intelligence platform:

Predicts churn probability
Explains model decisions using SHAP
Recommends business actions
Enables interactive analysis via chatbot

## 🖼️ Dashboard Preview

### 📊 Main Dashboard  
<p align="center">
  <img src="assets/dashboard.png" width="800"/>
</p>

### 🔍 SHAP Explainability  
<p align="center">
  <img src="assets/shap.png" width="800"/>
</p>

### 🤖 AI Chatbot  
<p align="center">
  <img src="assets/chatbot.png" width="800"/>
</p>



##📊 1. Churn Prediction Engine:

ML-based churn prediction model
Real-time probability scoring
Risk segmentation:
🟢 Low Risk
🟠 Medium Risk
🔴 High Risk

##🎯 2. Interactive SaaS Dashboard:

KPI cards (Risk, Probability, Tenure)
Gauge chart visualization
Clean, responsive UI

##🔍 3. Explainable AI (SHAP):

Waterfall chart (individual prediction)
Feature importance visualization
Global feature impact summary

👉 Helps understand why the model predicted churn.

##🤖 4. AI Churn Analyst (Chatbot) :

Human-like conversational insights
Explains churn reasoning
Provides business recommendations
Domain-controlled (only churn-related queries)
Follow-up suggestions like real analyst

##📊 5. Model Evaluation Module :

ROC Curve (AUC Score)
Confusion Matrix
Performance validation using test data

##📄 6. Automated PDF Report:

Business-ready customer summary
Includes:
Risk level
Key drivers
Recommended actions

##🧠 Tech Stack:

| Category       | Tools              |
| -------------- | ------------------ |
| Language       | Python             |
| ML             | Scikit-learn       |
| Data           | Pandas, NumPy      |
| Visualization  | Plotly, Matplotlib |
| Explainability | SHAP               |
| UI             | Streamlit          |
| Reporting      | ReportLab          |

##📁 Project Structure:
customer_churn/
│
├── assets/
│   ├── dashboard.png
│   ├── shap.png
│   └── chatbot.png
│
├── app.py
├── model.pkl
├── columns.pkl
├── requirements.txt
└── README.md

##⚙️ Run Locally:
git clone https://github.com/sumit312-cpu/customer_churn.git
cd customer_churn

pip install -r requirements.txt
streamlit run app.py

##🌐 Deployment:

This app is deployed on Streamlit Cloud:

👉 https://customerchurn-gpvp2yxqfhjmmtfvkfzcrw.streamlit.app/

##🎯 Business Use Cases:

📡 Telecom companies
💳 Banking & Financial Services
📦 Subscription-based platforms
💻 SaaS businesses

##📈 Impact:

✔ Identify high-risk customers early
✔ Reduce churn rate
✔ Improve customer retention
✔ Enable data-driven decisions

##🚀 Future Improvements:

🔐 User authentication system
🗄 Database integration (real-time data)
☁️ Scalable cloud deployment (AWS/GCP)
📊 Advanced analytics dashboard


## ⭐ Why This Project Stands Out

This project demonstrates:

✔ End-to-end ML pipeline development  
✔ Explainable AI (SHAP integration)  
✔ Business-focused thinking  
✔ Interactive product design  
✔ Real-world deployment  

👉 Built with a focus on **real industry use-cases**, not just academic learning.

## 👨‍💻 Author

**Sumit Tiwari**  
Aspiring Data Scientist / ML Engineer  
📍 Bengaluru, India