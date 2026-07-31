import streamlit as st
import pickle
import base64
from utils.preprocess import transform_text
from utils.helper import get_risk_level, get_reason

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="AI Email & SMS Security Assistant",
    page_icon="🛡️",
    layout="centered"
)

# -----------------------------
# Load CSS
# -----------------------------
def load_css():
    try:
        with open("assets/style.css") as f:
            st.markdown(
                f"<style>{f.read()}</style>",
                unsafe_allow_html=True
            )
    except:
        pass

load_css()

# -----------------------------
# Load Model
# -----------------------------
with open("model/vectorizer.pkl", "rb") as f:
    tfidf = pickle.load(f)

with open("model/model.pkl", "rb") as f:
    model = pickle.load(f)

# -----------------------------
# Sidebar
# -----------------------------
with st.sidebar:

    logo_b64 = base64.b64encode(open("assets/logo.png", "rb").read()).decode()

    st.markdown(
        f"""
        <div style="display:flex;justify-content:center;">
            <img src="data:image/png;base64,{logo_b64}" width="140">
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.title("About")

    st.write("""
This application detects whether an SMS or Email is **Spam** or **Legitimate** using Machine Learning.

### Model
- Multinomial Naive Bayes

### NLP
- Tokenization
- Stopword Removal
- Stemming
- TF-IDF

### Dataset
SMS Spam Collection Dataset

---
Developed by **Vedanti Rahatikar**
""")

# -----------------------------
# Header
# -----------------------------
_, center, _ = st.columns([2, 1, 2])

with center:
    st.image("assets/logo.png", width=120)

st.markdown(
    "<h1 style='text-align:center;'>AI Email & SMS Security Assistant</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<p class='subtitle'>Detect spam and suspicious SMS/Emails using Natural Language Processing and Machine Learning.</p>",
    unsafe_allow_html=True
)

# -----------------------------
# Input
# -----------------------------
input_sms = st.text_area(
    "Enter your message",
    height=180,
    placeholder="Type your SMS or Email here..."
)

if "history" not in st.session_state:
    st.session_state.history = []

# -----------------------------
# Predict
# -----------------------------
if st.button("🔍 Scan Message"):

    if input_sms.strip() == "":
        st.warning("Please enter a message.")

    else:

        transformed_sms = transform_text(input_sms)

        vector = tfidf.transform([transformed_sms])

        prediction = model.predict(vector)[0]

        probability = model.predict_proba(vector)

        spam_probability = probability[0][1] * 100

        is_spam = prediction == 1
        verdict_class = "spam" if is_spam else "safe"
        verdict_icon = "🚨" if is_spam else "✅"
        verdict_title = "Spam Detected" if is_spam else "Message Looks Safe"
        risk_level = get_risk_level(spam_probability)

        # -----------------------------
        # Verdict card
        # -----------------------------
        st.markdown(
            f"""
            <div class="verdict-card {verdict_class}">
                <div class="verdict-icon">{verdict_icon}</div>
                <div>
                    <p class="verdict-title">{verdict_title}</p>
                    <p class="verdict-meta">Scanned message · {len(input_sms)} characters</p>
                </div>
                <div class="verdict-badges">
                    <span class="badge">Confidence {spam_probability:.1f}%</span>
                    <span class="badge">Threat: {risk_level}</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.progress(int(spam_probability))

        st.markdown("---")

        st.subheader("Why was this flagged?")

        reasons = get_reason(input_sms)

        reasons_html = "".join(f"<div>✓ {reason}</div>" for reason in reasons)
        st.markdown(f"<div class='reason-list'>{reasons_html}</div>", unsafe_allow_html=True)

        result = "🚨 Spam" if is_spam else "✅ Safe"

        st.session_state.history.insert(0, result)

# -----------------------------
# Prediction History
# -----------------------------
if len(st.session_state.history) > 0:

    st.markdown("---")

    st.subheader("Recent Scans")

    history_html = ""
    for item in st.session_state.history[:5]:
        is_spam_item = "Spam" in item
        dot_class = "spam" if is_spam_item else "safe"
        label = item.replace("🚨 ", "").replace("✅ ", "")
        history_html += f"<div class='history-row'><span class='dot {dot_class}'></span>{label}</div>"

    st.markdown(f"<div>{history_html}</div>", unsafe_allow_html=True)

# -----------------------------
# Example Messages
# -----------------------------
st.markdown("---")

st.subheader("Try a Sample Scan")

col1, col2 = st.columns(2, gap="medium")

with col1:
    st.markdown(
        """
        <div class="sample-card spam">
            <div class="sample-label">🚨 Spam Example</div>
            <p class="sample-text">Congratulations! You've won ₹10,000. Click here to claim your reward.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        """
        <div class="sample-card safe">
            <div class="sample-label">✅ Legitimate Example</div>
            <p class="sample-text">Hey! Are we meeting tomorrow at 6 PM?</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# -----------------------------
# Footer
# -----------------------------
st.markdown("---")

st.caption(
    "🛡️ AI Email & SMS Security Assistant | Built using Streamlit + Scikit-Learn + NLTK"
)