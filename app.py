# ================= IMPORTS =================
import streamlit as st
import pandas as pd
import pickle
import numpy as np
import plotly.graph_objects as go
import random
import os

# ================= LOAD MODEL =================
model = pickle.load(open("model.pkl", "rb"))
columns = pickle.load(open("columns.pkl", "rb"))

# ================= PAGE =================
st.set_page_config(page_title="Churn AI", layout="wide")

# ================= HEADER =================
st.title("🚀 Customer Churn Intelligence AI")
st.caption("Predict • Explain • Act — Smart Retention Insights")

st.markdown("---")

# ================= SIDEBAR =================
page = st.sidebar.radio("Navigation", ["Prediction", "Model Evaluation"])

# =========================================================
# ===================== PREDICTION =========================
# =========================================================
if page == "Prediction":

    st.markdown("### 📥 Customer Profile")

    c1, c2, c3 = st.columns(3)

    with c1:
        age = st.slider("Age", 18, 80, 30)
        tenure = st.slider("Tenure", 0, 72, 12)

    with c2:
        monthly = st.number_input("Monthly Charges", 100.0, 10000.0, 500.0)
        contract = st.selectbox("Contract", ["Month-to-month", "One year", "Two year"])

    with c3:
        gender = st.selectbox("Gender", ["Female", "Male", "Other"])
        payment = st.selectbox("Payment", ["Credit card", "Electronic check", "Mailed check"])

    # ================= FEATURES =================
    total = monthly * tenure

    data = {
        'Age': age,
        'Tenure': tenure,
        'MonthlyCharges': monthly,
        'TotalCharges': total,
        'Charge_per_Tenure': monthly/(tenure+1),
        'Tenure_Age_Ratio': tenure/(age+1),
        'Charge_to_Total_Ratio': monthly/(total+1),

        'Gender_Male': 1 if gender == "Male" else 0,
        'Gender_Other': 1 if gender == "Other" else 0,

        'Contract_One year': 1 if contract == "One year" else 0,
        'Contract_Two year': 1 if contract == "Two year" else 0,

        'PaymentMethod_Credit card': 1 if payment == "Credit card" else 0,
        'PaymentMethod_Electronic check': 1 if payment == "Electronic check" else 0,
        'PaymentMethod_Mailed check': 1 if payment == "Mailed check" else 0
    }

    input_df = pd.DataFrame([data])
    input_df = input_df.reindex(columns=columns, fill_value=0)

    # ================= PREDICTION =================
    prob = float(model.predict_proba(input_df)[0][1])

    # ================= SHAP =================
    shap_data = []
    shap_values = None

    try:
        import shap
        explainer = shap.TreeExplainer(model)
        shap_values = explainer(input_df)

        shap_data = sorted(
            zip(columns, shap_values.values[0]),
            key=lambda x: abs(x[1]),
            reverse=True
        )
    except:
        shap_data = []

    # ================= METRICS =================
    st.markdown("### 📊 Prediction Overview")

    k1, k2, k3 = st.columns(3)

    if prob >= 0.7:
        risk = "High 🔴"
    elif prob >= 0.4:
        risk = "Medium 🟠"
    else:
        risk = "Low 🟢"

    k1.metric("Risk", risk)
    k2.metric("Probability", f"{prob:.2f}")
    k3.metric("Tenure", f"{tenure} months")

    # ================= GAUGE =================
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=prob * 100,
        title={'text': "Churn Probability"},
        gauge={
            'axis': {'range': [0, 100]},
            'steps': [
                {'range': [0, 40], 'color': "green"},
                {'range': [40, 70], 'color': "orange"},
                {'range': [70, 100], 'color': "red"}
            ]
        }
    ))
    st.plotly_chart(fig, use_container_width=True)

    # ================= SHAP =================
    st.markdown("### 🔍 Explainability")

    if shap_values is not None:
        import matplotlib.pyplot as plt

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Local Explanation")
            shap.plots.waterfall(shap_values[0], show=False)
            st.pyplot(plt.gcf())
            plt.clf()

        with col2:
            st.subheader("Top Features")
            df_imp = pd.DataFrame(shap_data, columns=["Feature", "Impact"])
            df_imp["Impact"] = df_imp["Impact"].abs()
            st.bar_chart(df_imp.head(10).set_index("Feature"))

    else:
        st.warning("SHAP not available")

    # =====================================================
    # 🤖 AI CHURN ANALYST 
    # ==================================================
    st.markdown("---")
    st.markdown("## 🤖 AI Churn Analyst")

    if "chat" not in st.session_state:
        st.session_state.chat = []

    def clean(f):
        return (
            f.replace("_", " ")
            .replace("MonthlyCharges", "Monthly Charges")
            .replace("TotalCharges", "Total Spend")
            .replace("Tenure", "Customer Tenure")
        )

    user_msg = st.text_input("Ask about this customer")

    if user_msg:

        pos = [clean(f) for f, v in shap_data if v > 0][:3] if shap_data else []
        neg = [clean(f) for f, v in shap_data if v < 0][:3] if shap_data else []

        allowed_keywords = [
            "why", "risk", "churn", "reduce", "improve",
            "retain", "customer", "leave", "stay", "reason"
        ]

        if not any(k in user_msg.lower() for k in allowed_keywords):
            response = "❌ This question is not related to churn analysis."

        else:

            if prob >= 0.7:
                response = f"""
This customer is at **high risk of churn**.

The biggest drivers are **{', '.join(pos) if pos else "pricing and engagement"}**.

Some stability comes from **{', '.join(neg) if neg else "loyalty signals"}**, but it's not enough.

👉 **Business Action:**
- Immediate outreach
- Discount or retention offer
- Push long-term contract
"""

            elif prob >= 0.4:
                response = f"""
This customer is in a **medium risk zone**.

Risk is driven by **{', '.join(pos)}**, while **{', '.join(neg)}** help retention.

👉 **Business Action:**
- Improve engagement
- Offer loyalty benefits
- Monitor closely
"""

            else:
                response = f"""
This customer is **low risk**.

Strong retention factors: **{', '.join(neg)}**

Minor risks: **{', '.join(pos)}**

👉 **Business Action:**
- Upsell premium plans
- Encourage referrals
"""

            response += f"\n\n📊 Confidence: {prob:.2f}"

        st.session_state.chat.append(("user", user_msg))
        st.session_state.chat.append(("bot", response))

    for role, msg in st.session_state.chat:
        if role == "user":
            st.markdown(f"🧑 **You:** {msg}")
        else:
            st.markdown(f"🤖 **AI Analyst:** {msg}")

    # ================= PDF REPORT =================
    st.markdown("---")
    if st.button("📄 Download Report"):

        try:
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
            from reportlab.lib.styles import getSampleStyleSheet

            doc = SimpleDocTemplate("report.pdf")
            styles = getSampleStyleSheet()

            content = []
            content.append(Paragraph("Customer Churn Report", styles['Title']))
            content.append(Spacer(1, 10))
            content.append(Paragraph(f"Risk Level: {risk}", styles['Normal']))
            content.append(Paragraph(f"Probability: {prob:.2f}", styles['Normal']))

            doc.build(content)

            with open("report.pdf", "rb") as f:
                st.download_button("Download PDF", f, file_name="report.pdf")

        except:
            st.warning("Install reportlab: pip install reportlab")


# =========================================================
# ================= MODEL EVALUATION =======================
# =========================================================
elif page == "Model Evaluation":

    st.title("📊 Model Evaluation")

    uploaded_X = st.file_uploader("Upload X_test.pkl")
    uploaded_y = st.file_uploader("Upload y_test.pkl")

    if uploaded_X and uploaded_y:

        import matplotlib.pyplot as plt
        from sklearn.metrics import roc_curve, auc, confusion_matrix, ConfusionMatrixDisplay

        X_test = pickle.load(uploaded_X)
        y_test = pickle.load(uploaded_y)

        y_prob = model.predict_proba(X_test)[:, 1]
        y_pred = model.predict(X_test)

        # ROC
        fpr, tpr, _ = roc_curve(y_test, y_prob)
        roc_auc = auc(fpr, tpr)

        fig, ax = plt.subplots()
        ax.plot(fpr, tpr, label=f"AUC = {roc_auc:.2f}")
        ax.legend()
        st.pyplot(fig)

        # Confusion Matrix
        cm = confusion_matrix(y_test, y_pred)

        fig2, ax2 = plt.subplots()
        ConfusionMatrixDisplay(cm).plot(ax=ax2)
        st.pyplot(fig2)