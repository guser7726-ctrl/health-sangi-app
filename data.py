import streamlit as st
import json
import math
from datetime import datetime, date, timedelta
import random

# ─── Page Config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="স্বাস্থ্য সঙ্গী ১.০",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS & Animations ─────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Hind+Siliguri:wght@300;400;500;600;700&display=swap');

* { font-family: 'Hind Siliguri', sans-serif; }

/* Gradient background */
.stApp {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 25%, #f093fb 50%, #f5576c 75%, #4facfe 100%);
    background-size: 400% 400%;
    animation: gradientShift 15s ease infinite;
}
@keyframes gradientShift {
    0%   { background-position: 0% 50%; }
    50%  { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* Main content area */
.main .block-container {
    background: rgba(255,255,255,0.95);
    border-radius: 20px;
    padding: 2rem;
    box-shadow: 0 20px 60px rgba(0,0,0,0.2);
    backdrop-filter: blur(10px);
}

/* Header */
.app-header {
    text-align: center;
    padding: 2rem 1rem 1rem;
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    border-radius: 20px;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.app-header::before {
    content: '';
    position: absolute;
    top:-50%; left:-50%;
    width:200%; height:200%;
    background: radial-gradient(circle, rgba(255,255,255,0.05) 0%, transparent 60%);
    animation: pulse 4s ease-in-out infinite;
}
@keyframes pulse {
    0%,100% { transform: scale(1); opacity:0.5; }
    50%      { transform: scale(1.2); opacity:1; }
}
.app-title {
    font-size: 3rem;
    font-weight: 700;
    color: #fff;
    text-shadow: 0 0 30px rgba(100,200,255,0.8);
    margin: 0;
    animation: glow 2s ease-in-out infinite alternate;
}
@keyframes glow {
    from { text-shadow: 0 0 10px #fff, 0 0 20px #4facfe, 0 0 30px #4facfe; }
    to   { text-shadow: 0 0 20px #fff, 0 0 40px #f093fb, 0 0 60px #f093fb; }
}
.app-subtitle {
    color: rgba(255,255,255,0.8);
    font-size: 1rem;
    margin-top: 0.5rem;
}
.app-creator {
    color: rgba(255,255,255,0.6);
    font-size: 0.85rem;
    margin-top: 0.3rem;
}
.disclaimer {
    background: linear-gradient(135deg, #ff6b6b22, #feca5722);
    border: 1px solid #ff6b6b55;
    border-radius: 10px;
    padding: 0.5rem 1rem;
    color: #ff6b6b;
    font-size: 0.8rem;
    margin-top: 0.8rem;
    display: inline-block;
}

/* Section cards */
.section-card {
    background: linear-gradient(135deg, #ffffff, #f8f9ff);
    border-radius: 16px;
    padding: 1.5rem;
    margin: 1rem 0;
    box-shadow: 0 8px 25px rgba(0,0,0,0.08);
    border-left: 5px solid;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}
.section-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 15px 40px rgba(0,0,0,0.15);
}

/* Metric cards */
.metric-card {
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: white;
    border-radius: 12px;
    padding: 1rem;
    text-align: center;
    margin: 0.5rem 0;
    box-shadow: 0 5px 20px rgba(102,126,234,0.4);
    animation: fadeInUp 0.6s ease;
}
@keyframes fadeInUp {
    from { opacity:0; transform:translateY(20px); }
    to   { opacity:1; transform:translateY(0); }
}
.metric-value { font-size: 2rem; font-weight: 700; }
.metric-label { font-size: 0.85rem; opacity: 0.9; }

/* Risk badges */
.risk-low    { background:linear-gradient(135deg,#56ab2f,#a8e063); color:white; border-radius:8px; padding:0.3rem 1rem; font-weight:600; }
.risk-medium { background:linear-gradient(135deg,#f7971e,#ffd200); color:white; border-radius:8px; padding:0.3rem 1rem; font-weight:600; }
.risk-high   { background:linear-gradient(135deg,#cb2d3e,#ef473a); color:white; border-radius:8px; padding:0.3rem 1rem; font-weight:600; }

/* Doctor card */
.doctor-card {
    background: linear-gradient(135deg, #e0f7fa, #e8f5e9);
    border-radius: 14px;
    padding: 1.2rem;
    margin: 0.8rem 0;
    border: 1px solid #b2dfdb;
    box-shadow: 0 4px 15px rgba(0,150,136,0.15);
    transition: all 0.3s;
}
.doctor-card:hover {
    transform: scale(1.02);
    box-shadow: 0 8px 25px rgba(0,150,136,0.25);
}
.doctor-name { font-size:1.1rem; font-weight:700; color:#004d40; }
.doctor-spec { color:#00796b; font-size:0.9rem; }

/* Hospital card */
.hospital-card {
    background: linear-gradient(135deg, #fce4ec, #f3e5f5);
    border-radius: 14px;
    padding: 1.2rem;
    margin: 0.8rem 0;
    border: 1px solid #f48fb1;
    box-shadow: 0 4px 15px rgba(233,30,99,0.1);
    transition: all 0.3s;
}
.hospital-card:hover {
    transform: scale(1.02);
    box-shadow: 0 8px 25px rgba(233,30,99,0.2);
}

/* Blood bank card */
.blood-card {
    background: linear-gradient(135deg, #ffebee, #fce4ec);
    border-radius: 14px;
    padding: 1rem;
    margin: 0.5rem 0;
    border-left: 4px solid #e53935;
    box-shadow: 0 3px 12px rgba(229,57,53,0.15);
}

/* Ambulance card */
.ambulance-card {
    background: linear-gradient(135deg, #fff3e0, #fff8e1);
    border-radius: 14px;
    padding: 1rem;
    margin: 0.5rem 0;
    border-left: 4px solid #ff6f00;
    box-shadow: 0 3px 12px rgba(255,111,0,0.15);
}

/* Pharmacy card */
.pharmacy-card {
    background: linear-gradient(135deg, #e8f5e9, #f1f8e9);
    border-radius: 12px;
    padding: 1rem;
    margin: 0.5rem 0;
    border-left: 4px solid #43a047;
}

/* Symptom checkboxes */
.symptom-section {
    background: #f8f9ff;
    border-radius: 12px;
    padding: 1rem;
    margin: 0.5rem 0;
}

/* Nav buttons */
.stButton > button {
    width: 100%;
    border-radius: 12px;
    border: none;
    padding: 0.6rem 1rem;
    font-weight: 600;
    transition: all 0.3s ease;
    font-family: 'Hind Siliguri', sans-serif;
}
.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(0,0,0,0.2);
}

/* Info boxes */
.info-box {
    background: linear-gradient(135deg, #e3f2fd, #e8eaf6);
    border-radius: 12px;
    padding: 1rem;
    margin: 0.5rem 0;
    border-left: 4px solid #1976d2;
}
.success-box {
    background: linear-gradient(135deg, #e8f5e9, #f1f8e9);
    border-radius: 12px;
    padding: 1rem;
    margin: 0.5rem 0;
    border-left: 4px solid #43a047;
}
.warning-box {
    background: linear-gradient(135deg, #fff3e0, #fff8e1);
    border-radius: 12px;
    padding: 1rem;
    margin: 0.5rem 0;
    border-left: 4px solid #f57c00;
}
.danger-box {
    background: linear-gradient(135deg, #ffebee, #fce4ec);
    border-radius: 12px;
    padding: 1rem;
    margin: 0.5rem 0;
    border-left: 4px solid #e53935;
}

/* Sidebar styling */
.css-1d391kg { background: linear-gradient(180deg, #1a1a2e, #16213e); }
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
}
section[data-testid="stSidebar"] * { color: white !important; }

/* Progress bar */
.stProgress > div > div { border-radius: 10px; }

/* Tab styling */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background: linear-gradient(135deg, #667eea22, #764ba222);
    border-radius: 12px;
    padding: 0.5rem;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 8px;
    padding: 0.4rem 1rem;
    font-weight: 600;
}

/* Floating animation for emojis */
@keyframes float {
    0%,100% { transform: translateY(0); }
    50%      { transform: translateY(-8px); }
}
.float-emoji { display:inline-block; animation: float 3s ease-in-out infinite; }

/* Table styling */
.dataframe { border-radius: 12px; overflow: hidden; }

/* Step indicator */
.step-box {
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: white;
    border-radius: 50%;
    width: 36px; height: 36px;
    display: inline-flex;
    align-items: center; justify-content: center;
    font-weight: 700;
    margin-right: 0.5rem;
    box-shadow: 0 3px 10px rgba(102,126,234,0.5);
}
</style>
""", unsafe_allow_html=True)

# ─── Load All Data ────────────────────────────────────────────────────────────
from data import (
    DISEASES, DOCTORS, HOSPITALS, BLOOD_BANKS, AMBULANCES, PHARMACIES,
    MEDICINES, HEALTH_TIPS, HERBAL_REMEDIES, DISEASE_PREVENTION,
    VACCINATION_SCHEDULE, NUTRITION_ADVICE, HEALTH_QUIZ, BLOOD_DONORS
)

# ─── Header ──────────────────────────────────────────────────────────────────
st.markdown("""
<div class="app-header">
    <div class="float-emoji" style="font-size:3rem;">🏥</div>
    <div class="app-title">স্বাস্থ্য সঙ্গী ১.০</div>
    <div class="app-subtitle">আপনার বিশ্বস্ত স্বাস্থ্য সহায়ক | Your Trusted Health Companion</div>
    <div class="app-creator">✨ Created by Kaliagonj Naziraton High School (Soundarjya) ✨</div>
    <div class="disclaimer">⚠️ এটি শুধু প্রাথমিক স্বাস্থ্য পরামর্শের জন্য তৈরি। এটি ডাক্তারের বিকল্প নয়।</div>
</div>
""", unsafe_allow_html=True)

# ─── Sidebar Navigation ───────────────────────────────────────────────────────
st.sidebar.markdown("## 🧭 মেনু")
menu_options = {
    "🔍 রোগ নির্ণয় ও পরামর্শ": "diagnosis",
    "🏥 হাসপাতাল তালিকা": "hospitals",
    "💊 ফার্মেসি ও ওষুধ খোঁজ": "pharmacy",
    "🌿 ভেষজ চিকিৎসা": "herbal",
    "👶 মা ও শিশু পরামর্শ": "mother_child",
    "🩸 ব্লাড ব্যাংক": "blood_bank",
    "🚑 অ্যাম্বুলেন্স সেবা": "ambulance",
    "💡 স্বাস্থ্য পরামর্শ": "health_tips",
    "📊 BMI ও স্বাস্থ্য বিশ্লেষণ": "bmi",
    "🩺 ডায়াবেটিস ঝুঁকি": "diabetes_risk",
    "💓 প্রেসার বিশ্লেষণ": "bp_analysis",
    "📄 স্বাস্থ্য রিপোর্ট": "report",
    "💉 টিকা রিমাইন্ডার": "vaccine",
    "🥗 খাবার ও পুষ্টি পরামর্শ": "nutrition",
    "💧 পানির প্রয়োজনীয়তা": "water_calc",
    "🧠 স্বাস্থ্য কুইজ": "quiz",
    "🛡️ রোগ প্রতিরোধ গাইড": "prevention",
    "❤️ রক্তদাতা খোঁজা": "blood_donor",
    "🔢 মেডিকেল ক্যালকুলেটর": "calc",
    "📰 স্বাস্থ্য সংবাদ": "news",
    "⚠️ রোগের ঝুঁকি স্কোর": "risk_score",
}

selected = st.sidebar.radio("বিভাগ নির্বাচন করুন:", list(menu_options.keys()), label_visibility="collapsed")
page = menu_options[selected]

st.sidebar.markdown("---")
st.sidebar.markdown("### 🚨 জরুরি নম্বর")
st.sidebar.markdown("🆘 **জাতীয় জরুরি:** 999")
st.sidebar.markdown("🚑 **অ্যাম্বুলেন্স:** 16430")
st.sidebar.markdown("🏥 **স্বাস্থ্য হেল্পলাইন:** 16676")
st.sidebar.markdown("---")

# ═══════════════════════════════════════════════════════════════════
# PAGE 1: রোগ নির্ণয় ও পরামর্শ
# ═══════════════════════════════════════════════════════════════════
if page == "diagnosis":
    st.markdown("## 🔍 রোগ নির্ণয় ও পরামর্শ")

    tab1, tab2 = st.tabs(["📋 ধাপে ধাপে তথ্য দিন", "✅ উপসর্গ চেকলিস্ট"])

    with tab1:
        st.markdown("### <span class='step-box'>১</span> আপনার শারীরিক তথ্য দিন", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        with col1:
            age = st.number_input("বয়স (বছর)", 1, 120, 30)
            weight = st.number_input("ওজন (কেজি)", 10.0, 200.0, 60.0, 0.5)
        with col2:
            bp_sys = st.number_input("সিস্টোলিক বিপি (mmHg)", 60, 250, 120)
            bp_dia = st.number_input("ডায়াস্টোলিক বিপি (mmHg)", 40, 160, 80)
        with col3:
            sugar = st.number_input("রক্তে সুগার (mg/dL)", 50, 600, 100)
            pulse = st.number_input("পালস রেট (bpm)", 30, 250, 75)

        st.markdown("### <span class='step-box'>২</span> আপনার উপসর্গ লিখুন (ঐচ্ছিক)", unsafe_allow_html=True)
        custom_symptoms = st.text_area("আপনার উপসর্গ এখানে বিস্তারিত লিখুন...", height=80, placeholder="যেমন: মাথাব্যথা, জ্বর, বুকে ব্যথা...")

        st.markdown("### <span class='step-box'>৩</span> নিচের উপসর্গগুলো থেকে বেছে নিন", unsafe_allow_html=True)

        all_symptoms = sorted(set(
            sym for d in DISEASES for sym in d["symptoms_keywords"]
        ))

        # Group symptoms
        symptom_groups = {
            "💓 হৃদয় ও রক্তসঞ্চালন": ["বুকে ব্যথা","বুক ধড়ফড়","শ্বাসকষ্ট","পা ফোলা","মাথা ঘোরা","অজ্ঞান","পালস কম","পালস বেশি"],
            "🧠 মাথা ও স্নায়ু": ["মাথাব্যথা","মাথা ঘোরা","অবশ","স্মৃতিভ্রম","খিঁচুনি","কাঁপুনি","দৃষ্টি ঝাপসা"],
            "🤒 জ্বর ও সংক্রমণ": ["জ্বর","কাশি","সর্দি","গলাব্যথা","শরীর ব্যথা","বমি","ডায়রিয়া"],
            "🫀 পেট ও হজম": ["পেটব্যথা","বমি ভাব","অ্যাসিডিটি","কোষ্ঠকাঠিন্য","জন্ডিস","ক্ষুধামন্দা"],
            "🦴 হাড় ও জোড়া": ["জোড়ায় ব্যথা","কোমর ব্যথা","ঘাড় ব্যথা","হাঁটু ব্যথা"],
            "💧 কিডনি ও প্রস্রাব": ["প্রস্রাবে জ্বালা","ঘন প্রস্রাব","প্রস্রাব কম","শরীর ফোলা"],
            "🌡️ সাধারণ": ["ওজন কমা","ওজন বাড়া","ক্লান্তি","দুর্বলতা","ঘাম","চুলপড়া"],
        }

        selected_symptoms = []
        for group, syms in symptom_groups.items():
            with st.expander(group):
                cols = st.columns(2)
                for i, sym in enumerate(syms):
                    if cols[i % 2].checkbox(sym, key=f"sym_{sym}"):
                        selected_symptoms.append(sym)

        if st.button("🔍 বিশ্লেষণ করুন", type="primary", use_container_width=True):
            st.markdown("---")
            st.markdown("## 📊 বিশ্লেষণের ফলাফল")

            # ── Vital Signs Analysis ──────────────────────────────
            col1, col2, col3, col4 = st.columns(4)
            # BP
            if bp_sys < 90 or bp_dia < 60:
                bp_status = "⬇️ Low BP"; bp_color = "#2196F3"
            elif bp_sys <= 120 and bp_dia <= 80:
                bp_status = "✅ Normal BP"; bp_color = "#4CAF50"
            elif bp_sys <= 139 or bp_dia <= 89:
                bp_status = "⚠️ Pre-Hypertension"; bp_color = "#FF9800"
            else:
                bp_status = "🔴 Hypertension"; bp_color = "#F44336"

            # Sugar
            if sugar < 70:
                sugar_status = "⬇️ Low"; sugar_color = "#2196F3"
            elif sugar <= 100:
                sugar_status = "✅ Normal"; sugar_color = "#4CAF50"
            elif sugar <= 125:
                sugar_status = "⚠️ Pre-Diabetic"; sugar_color = "#FF9800"
            else:
                sugar_status = "🔴 High"; sugar_color = "#F44336"

            # Pulse
            if pulse < 60:
                pulse_status = "⬇️ Bradycardia"; pulse_color = "#2196F3"
            elif pulse <= 100:
                pulse_status = "✅ Normal"; pulse_color = "#4CAF50"
            else:
                pulse_status = "🔴 Tachycardia"; pulse_color = "#F44336"

            h = 160; bmi_val = weight / ((h/100)**2)
            if bmi_val < 18.5: bmi_status = "⬇️ কম ওজন"; bmi_color="#2196F3"
            elif bmi_val < 25: bmi_status = "✅ স্বাভাবিক"; bmi_color="#4CAF50"
            elif bmi_val < 30: bmi_status = "⚠️ অতিরিক্ত"; bmi_color="#FF9800"
            else: bmi_status = "🔴 স্থূল"; bmi_color="#F44336"

            with col1:
                st.markdown(f"""<div class="metric-card" style="background:linear-gradient(135deg,{bp_color}aa,{bp_color});">
                <div class="metric-label">🩺 রক্তচাপ</div>
                <div class="metric-value">{bp_sys}/{bp_dia}</div>
                <div>{bp_status}</div></div>""", unsafe_allow_html=True)
            with col2:
                st.markdown(f"""<div class="metric-card" style="background:linear-gradient(135deg,{sugar_color}aa,{sugar_color});">
                <div class="metric-label">🍬 সুগার</div>
                <div class="metric-value">{sugar}</div>
                <div>{sugar_status}</div></div>""", unsafe_allow_html=True)
            with col3:
                st.markdown(f"""<div class="metric-card" style="background:linear-gradient(135deg,{pulse_color}aa,{pulse_color});">
                <div class="metric-label">💓 পালস</div>
                <div class="metric-value">{pulse}</div>
                <div>{pulse_status}</div></div>""", unsafe_allow_html=True)
            with col4:
                st.markdown(f"""<div class="metric-card" style="background:linear-gradient(135deg,{bmi_color}aa,{bmi_color});">
                <div class="metric-label">⚖️ সূচক (BMI*)</div>
                <div class="metric-value">{bmi_val:.1f}</div>
                <div>{bmi_status}</div></div>""", unsafe_allow_html=True)

            # ── Disease Matching ───────────────────────────────────
            st.markdown("### 🩺 সম্ভাব্য রোগ ও পরামর্শ")

            # Build search text
            search_text = " ".join(selected_symptoms) + " " + custom_symptoms.lower()
            # Add vitals to search
            if bp_sys >= 140 or bp_dia >= 90: search_text += " উচ্চ রক্তচাপ"
            if bp_sys < 90: search_text += " লো বিপি"
            if sugar > 126: search_text += " সুগার ডায়াবেটিস"
            if pulse < 60: search_text += " পালস কম"
            if pulse > 100: search_text += " পালস বেশি"

            matched = []
            for disease in DISEASES:
                score = sum(1 for kw in disease["symptoms_keywords"] if kw in search_text)
                if score > 0:
                    matched.append((score, disease))
            matched.sort(key=lambda x: -x[0])

            if matched:
                for score, disease in matched[:5]:
                    confidence = min(100, score * 20)
                    if confidence >= 60: risk_class = "risk-high"
                    elif confidence >= 40: risk_class = "risk-medium"
                    else: risk_class = "risk-low"

                    with st.expander(f"🔸 {disease['name_bn']} ({disease['name_en']})", expanded=(matched.index((score,disease))==0)):
                        col_a, col_b = st.columns([2,1])
                        with col_a:
                            st.markdown(f"**📋 প্রধান উপসর্গ:** {disease['symptoms']}")
                            st.markdown(f"**💡 পরামর্শ:** {disease['advice']}")
                            st.markdown(f"**👨‍⚕️ বিশেষজ্ঞ চিকিৎসক:** {disease['specialist']}")
                        with col_b:
                            st.markdown(f'<div class="{risk_class}">মিল: {confidence}%</div>', unsafe_allow_html=True)
                            st.progress(confidence/100)

                        # Suggest doctors
                        st.markdown("**🏥 প্রস্তাবিত ডাক্তার:**")
                        relevant_docs = [d for d in DOCTORS if any(
                            spec.lower() in d["specialty"].lower()
                            for spec in disease["specialist_keywords"]
                        )][:3]
                        if not relevant_docs:
                            relevant_docs = DOCTORS[:3]
                        for doc in relevant_docs:
                            st.markdown(f"""<div class="doctor-card">
                            <div class="doctor-name">👨‍⚕️ {doc['name']}</div>
                            <div class="doctor-spec">{doc['specialty']}</div>
                            <div>📍 {doc['chamber']} | ⏰ {doc['time']}</div>
                            <div>💰 ফি: {doc['fee']} | 📞 {doc['phone']}</div>
                            </div>""", unsafe_allow_html=True)

                        # Suggest hospitals
                        st.markdown("**🏨 প্রস্তাবিত হাসপাতাল:**")
                        rel_hosp = [h for h in HOSPITALS if any(
                            kw in h["facilities"].lower()
                            for kw in disease.get("hospital_keywords", [])
                        )][:2]
                        if not rel_hosp:
                            rel_hosp = HOSPITALS[:2]
                        for hosp in rel_hosp:
                            st.markdown(f"""<div class="hospital-card">
                            🏥 <strong>{hosp['name']}</strong><br>
                            📍 {hosp['location']} | ✅ {hosp['facilities'][:100]}...
                            </div>""", unsafe_allow_html=True)
            else:
                st.info("কোনো নির্দিষ্ট রোগ শনাক্ত হয়নি। দয়া করে একজন ডাক্তারের পরামর্শ নিন।")

    with tab2:
        st.markdown("### ✅ ১০২টি রোগের উপসর্গ চেকলিস্ট")
        st.info("নিচের তালিকা থেকে আপনার সাথে মিলে যাওয়া উপসর্গগুলোতে টিক দিন।")

        checked_diseases = []
        for disease in DISEASES:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"**{disease['name_bn']}** — {disease['symptoms'][:80]}...")
            with col2:
                if st.checkbox("✓ মিলেছে", key=f"chk_{disease['id']}"):
                    checked_diseases.append(disease)

        if checked_diseases:
            st.markdown("### 📝 চিহ্নিত রোগের পরামর্শ:")
            for d in checked_diseases:
                st.markdown(f"""<div class="success-box">
                <strong>🔸 {d['name_bn']} ({d['name_en']})</strong><br>
                💡 {d['advice']}<br>
                👨‍⚕️ {d['specialist']}
                </div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════
# PAGE 2: হাসপাতাল তালিকা
# ═══════════════════════════════════════════════════════════════════
elif page == "hospitals":
    st.markdown("## 🏥 হাসপাতাল তালিকা")
    col1, col2 = st.columns(2)
    with col1:
        dist = st.selectbox("জেলা বেছে নিন:", ["সব", "পঞ্চগড়", "ঠাকুরগাঁও"])
    with col2:
        search_h = st.text_input("🔍 হাসপাতাল খুঁজুন:", placeholder="নাম বা সুবিধা লিখুন...")

    filtered = HOSPITALS
    if dist != "সব":
        filtered = [h for h in filtered if h.get("district") == dist]
    if search_h:
        filtered = [h for h in filtered if search_h.lower() in h["name"].lower() or search_h.lower() in h["facilities"].lower()]

    st.markdown(f"**মোট {len(filtered)}টি চিকিৎসা কেন্দ্র পাওয়া গেছে**")
    for h in filtered:
        with st.expander(f"🏥 {h['name']} — {h.get('district','')}"):
            st.markdown(f"""<div class="hospital-card">
            <strong>🏥 {h['name']}</strong><br>
            📌 <strong>ধরন:</strong> {h.get('type','')}<br>
            📍 <strong>অবস্থান:</strong> {h['location']}<br>
            ✅ <strong>সুবিধাসমূহ:</strong> {h['facilities']}
            </div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════
# PAGE 3: ফার্মেসি ও ওষুধ
# ═══════════════════════════════════════════════════════════════════
elif page == "pharmacy":
    st.markdown("## 💊 ফার্মেসি ও ওষুধ খোঁজ")
    tab1, tab2 = st.tabs(["🔍 ওষুধ খোঁজ", "🏪 ফার্মেসি তালিকা"])

    with tab1:
        medicine_search = st.text_input("💊 ওষুধের নাম লিখুন:", placeholder="যেমন: Paracetamol, Metformin...")
        if medicine_search:
            found_meds = [m for m in MEDICINES if medicine_search.lower() in m["name"].lower() or
                         medicine_search.lower() in m.get("generic","").lower()]
            if found_meds:
                for med in found_meds:
                    with st.expander(f"💊 {med['name']} ({med.get('generic','')})"):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown(f"**কাজ:** {med['use']}")
                            st.markdown(f"**ডোজ:** {med['dose']}")
                            st.markdown(f"**পার্শ্বপ্রতিক্রিয়া:** {med['side_effects']}")
                            st.markdown(f"**সতর্কতা:** {med['warning']}")
                        with col2:
                            st.markdown("**পাওয়া যাবে এই ফার্মেসিতে:**")
                            avail_pharmacies = random.sample(PHARMACIES, min(3, len(PHARMACIES)))
                            for ph in avail_pharmacies:
                                st.markdown(f"""<div class="pharmacy-card">
                                🏪 <strong>{ph['name']}</strong><br>
                                📍 {ph['location']}<br>
                                📞 {ph['phone']} | ⏰ {ph['hours']}
                                </div>""", unsafe_allow_html=True)
            else:
                st.warning("এই নামে কোনো ওষুধ পাওয়া যায়নি।")
                # Show nearby pharmacies anyway
                st.markdown("### নিকটবর্তী ফার্মেসি:")
                for ph in PHARMACIES[:5]:
                    st.markdown(f"""<div class="pharmacy-card">
                    🏪 <strong>{ph['name']}</strong> | 📍 {ph['location']} | 📞 {ph['phone']}
                    </div>""", unsafe_allow_html=True)

    with tab2:
        dist_ph = st.selectbox("জেলা:", ["সব", "পঞ্চগড়", "ঠাকুরগাঁও"], key="ph_dist")
        filtered_ph = PHARMACIES if dist_ph == "সব" else [p for p in PHARMACIES if p.get("district")==dist_ph]
        for ph in filtered_ph:
            st.markdown(f"""<div class="pharmacy-card">
            <strong>🏪 {ph['name']}</strong><br>
            📍 {ph['location']} | 📞 {ph['phone']}<br>
            ⏰ {ph['hours']}
            </div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════
# PAGE 4: ভেষজ চিকিৎসা
# ═══════════════════════════════════════════════════════════════════
elif page == "herbal":
    st.markdown("## 🌿 ভেষজ ও ঘরোয়া চিকিৎসা")
    st.markdown("""<div class="warning-box">
    ⚠️ <strong>সতর্কতা:</strong> এই ঘরোয়া পদ্ধতিগুলো শুধুমাত্র হালকা অসুস্থতার জন্য। গুরুতর রোগে অবশ্যই ডাক্তারের পরামর্শ নিন।
    </div>""", unsafe_allow_html=True)

    for i, remedy in enumerate(HERBAL_REMEDIES, 1):
        with st.expander(f"🌿 {i}. {remedy['condition']}"):
            col1, col2 = st.columns([2, 1])
            with col1:
                st.markdown(f"**🌱 ঘরোয়া পদ্ধতি:**")
                for method in remedy['methods']:
                    st.markdown(f"• {method}")
            with col2:
                st.markdown(f"""<div class="success-box">
                ✅ <strong>কার্যকারিতা:</strong> {remedy.get('effectiveness','সীমিত')}
                </div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════
# PAGE 5: মা ও শিশু পরামর্শ
# ═══════════════════════════════════════════════════════════════════
elif page == "mother_child":
    st.markdown("## 👶 মা ও শিশুদের পরামর্শ")

    tabs = st.tabs(["🤰 গর্ভকালীন", "🍼 নবজাতক", "👦 শিশুর পুষ্টি", "💉 টিকার তালিকা", "⚠️ বিপদ লক্ষণ", "🧠 মানসিক স্বাস্থ্য"])

    with tabs[0]:
        st.markdown("### 🤰 গর্ভবতী মায়েদের জন্য পরামর্শ")
        for tip in NUTRITION_ADVICE.get("pregnant", []):
            st.markdown(f"""<div class="info-box">💚 {tip}</div>""", unsafe_allow_html=True)

        st.markdown("### 📅 গর্ভকালীন পরীক্ষা-নিরীক্ষা")
        checks = [
            ("১ম ত্রৈমাসিক (১-১২ সপ্তাহ)", ["রক্তের গ্রুপ পরীক্ষা", "হিমোগ্লোবিন", "আল্ট্রাসনোগ্রাফি", "থাইরয়েড TSH", "ব্লাড সুগার"]),
            ("২য় ত্রৈমাসিক (১৩-২৭ সপ্তাহ)", ["অ্যানোমালি স্ক্যান (১৮-২০ সপ্তাহ)", "গ্লুকোজ টলারেন্স টেস্ট", "রক্তচাপ পর্যবেক্ষণ"]),
            ("৩য় ত্রৈমাসিক (২৮-৪০ সপ্তাহ)", ["NST (শিশুর হার্ট মনিটর)", "আল্ট্রা ডপলার", "গ্রুপ B স্ট্রেপ টেস্ট"]),
        ]
        for period, tests in checks:
            with st.expander(f"📅 {period}"):
                for t in tests:
                    st.markdown(f"✅ {t}")

    with tabs[1]:
        st.markdown("### 🍼 নবজাতক শিশুর যত্ন")
        newborn_tips = [
            ("🤱 বুকের দুধ", "জন্মের ১ ঘন্টার মধ্যে শালদুধ দিন। ৬ মাস পর্যন্ত শুধু বুকের দুধ।"),
            ("🌡️ উষ্ণ রাখুন", "শিশুকে পরিষ্কার কাপড়ে জড়িয়ে রাখুন। মাথা ঢেকে রাখুন।"),
            ("🛁 গোসল", "নাড়ি শুকানোর আগে শরীর মুছিয়ে দিন।"),
            ("👁️ চোখের যত্ন", "পরিষ্কার কাপড় দিয়ে চোখ মুছুন।"),
            ("😴 ঘুম", "শিশুকে সবসময় চিত করে শোয়ান।"),
        ]
        for title, desc in newborn_tips:
            st.markdown(f"""<div class="info-box"><strong>{title}:</strong> {desc}</div>""", unsafe_allow_html=True)

    with tabs[2]:
        st.markdown("### 🥗 শিশুর পুষ্টি")
        age_group = st.select_slider("শিশুর বয়স:", ["০-৬ মাস", "৬-১২ মাস", "১-২ বছর", "২-৫ বছর", "৫+ বছর"])
        if age_group == "০-৬ মাস":
            st.success("✅ শুধুমাত্র মায়ের বুকের দুধ। পানিও নয়।")
        elif age_group == "৬-১২ মাস":
            foods = ["নরম খিচুড়ি (ডাল+সবজি+চাল)", "ডিম (সিদ্ধ)", "কলা", "আলু", "মিষ্টি কুমড়া"]
            st.markdown("**শুরু করুন এই খাবার দিয়ে:**")
            for f in foods: st.markdown(f"✅ {f}")
        elif age_group == "১-২ বছর":
            foods = ["পরিবারের সাথে নরম খাবার", "দুধ ও দুধজাত খাবার", "ডিম, মাছ, মাংস", "সব ধরনের সবজি ও ফল"]
            for f in foods: st.markdown(f"✅ {f}")
        else:
            st.markdown("**স্বাস্থ্যকর খাদ্যাভ্যাস গড়ে তুলুন:**")
            foods = ["ভাত/রুটি", "ডাল ও সবজি", "মাছ/মাংস/ডিম", "দুধ", "তাজা ফল", "প্রচুর পানি"]
            for f in foods: st.markdown(f"✅ {f}")

    with tabs[3]:
        st.markdown("### 💉 টিকার তালিকা (EPI Schedule)")
        for vaccine in VACCINATION_SCHEDULE:
            st.markdown(f"""<div class="info-box">
            💉 <strong>{vaccine['name']}</strong> — বয়স: {vaccine['age']}<br>
            🛡️ সুরক্ষা: {vaccine['protects']}
            </div>""", unsafe_allow_html=True)

    with tabs[4]:
        st.markdown("### ⚠️ বিপদজনক লক্ষণ — সঙ্গে সঙ্গে ডাক্তারের কাছে যান")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**🤰 মায়ের ক্ষেত্রে:**")
            danger_mom = ["প্রচণ্ড রক্তপাত", "খিঁচুনি", "শ্বাসকষ্ট", "তীব্র মাথাব্যথা", "উচ্চ রক্তচাপ (১৪০/৯০+)", "শিশুর নড়াচড়া কমে যাওয়া", "দৃষ্টি ঝাপসা", "পেটে তীব্র ব্যথা"]
            for d in danger_mom: st.markdown(f"""<div class="danger-box">🚨 {d}</div>""", unsafe_allow_html=True)
        with col2:
            st.markdown("**👶 শিশুর ক্ষেত্রে:**")
            danger_baby = ["জ্বর ১০০.৪°F+ (২ মাসের কম)", "শ্বাসকষ্ট", "খেতে না চাওয়া", "বারবার বমি", "খিঁচুনি", "অস্বাভাবিক ঘুমিয়ে থাকা", "শরীর নীলচে হওয়া", "ফন্টানেল ফোলা"]
            for d in danger_baby: st.markdown(f"""<div class="danger-box">🚨 {d}</div>""", unsafe_allow_html=True)

    with tabs[5]:
        st.markdown("### 🧠 প্রসব-পরবর্তী মানসিক স্বাস্থ্য")
        st.markdown("""<div class="warning-box">
        অনেক মা সন্তান জন্মের পর মানসিক চাপ বা বিষণ্নতায় ভুগতে পারেন। এটি স্বাভাবিক। পরিবারের সাহায্য দরকার।
        </div>""", unsafe_allow_html=True)
        tips_mental = [
            "মায়ের পাশে থাকুন, একা ছেড়ে যাবেন না",
            "পর্যাপ্ত বিশ্রামের সুযোগ দিন",
            "মানসিক সমর্থন প্রদান করুন",
            "লক্ষণ গুরুতর হলে মানসিক বিশেষজ্ঞ দেখান",
            "বাচ্চা দেখার কাজে সাহায্য করুন",
        ]
        for t in tips_mental: st.markdown(f"""<div class="info-box">💚 {t}</div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════
# PAGE 6: ব্লাড ব্যাংক
# ═══════════════════════════════════════════════════════════════════
elif page == "blood_bank":
    st.markdown("## 🩸 ব্লাড ব্যাংক")
    col1, col2 = st.columns(2)
    with col1:
        dist = st.selectbox("জেলা:", ["সব", "পঞ্চগড়", "ঠাকুরগাঁও"])
    with col2:
        search_bb = st.text_input("🔍 খুঁজুন:", placeholder="নাম বা এলাকা...")

    filtered_bb = BLOOD_BANKS
    if dist != "সব": filtered_bb = [b for b in filtered_bb if b.get("district")==dist]
    if search_bb: filtered_bb = [b for b in filtered_bb if search_bb.lower() in b["name"].lower() or search_bb.lower() in b.get("address","").lower()]

    st.markdown(f"**মোট {len(filtered_bb)}টি ব্লাড ব্যাংক পাওয়া গেছে**")
    for bb in filtered_bb:
        st.markdown(f"""<div class="blood-card">
        🩸 <strong>{bb['name']}</strong><br>
        📍 {bb.get('address','')} — {bb.get('district','')}<br>
        📞 {bb.get('phone','তথ্য নেই')}
        </div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════
# PAGE 7: অ্যাম্বুলেন্স
# ═══════════════════════════════════════════════════════════════════
elif page == "ambulance":
    st.markdown("## 🚑 অ্যাম্বুলেন্স সেবা")
    st.markdown("""<div class="danger-box">
    🚨 <strong>জরুরি অবস্থায়:</strong> জাতীয় জরুরি সেবা <strong>999</strong> বা স্বাস্থ্য হেল্পলাইন <strong>16430</strong>
    </div>""", unsafe_allow_html=True)

    dist = st.selectbox("জেলা:", ["সব", "পঞ্চগড়", "ঠাকুরগাঁও"])
    filtered_amb = AMBULANCES if dist == "সব" else [a for a in AMBULANCES if a.get("district")==dist]

    for amb in filtered_amb:
        st.markdown(f"""<div class="ambulance-card">
        🚑 <strong>{amb['name']}</strong><br>
        📍 {amb['address']} — {amb.get('district','')}<br>
        📞 <strong style="color:#e65100;font-size:1.1rem;">{amb['phone']}</strong><br>
        ⏰ {amb.get('hours','২৪ ঘন্টা')}
        </div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════
# PAGE 8: স্বাস্থ্য পরামর্শ
# ═══════════════════════════════════════════════════════════════════
elif page == "health_tips":
    st.markdown("## 💡 সুস্থ জীবনের জন্য স্বাস্থ্য পরামর্শ")
    for i, tip in enumerate(HEALTH_TIPS, 1):
        emoji_list = ["🌿","💧","🏃","😴","🥗","🚭","🧼","😊","☀️","💊","🧘","🫀","🦷","⚖️","🩺"]
        emoji = emoji_list[(i-1) % len(emoji_list)]
        st.markdown(f"""<div class="info-box" style="margin:0.4rem 0;">
        {emoji} <strong>{i}.</strong> {tip}
        </div>""", unsafe_allow_html=True)

    st.markdown("### ⭐ প্রতিদিনের সহজ রুটিন")
    routine = [
        ("ভোর ৫-৬টা", "ঘুম থেকে উঠুন, ১-২ গ্লাস পানি পান করুন"),
        ("সকাল ৬-৭টা", "২০-৩০ মিনিট হাঁটুন বা ব্যায়াম করুন"),
        ("সকাল ৭-৮টা", "পুষ্টিকর নাস্তা করুন"),
        ("দুপুর ১২-১টা", "পুষ্টিকর দুপুরের খাবার খান"),
        ("বিকেল ৫-৬টা", "হালকা নাস্তা ও পানি পান"),
        ("রাত ৮-৯টা", "হালকা রাতের খাবার"),
        ("রাত ১০-১১টা", "মোবাইল বন্ধ করে ঘুমাতে যান"),
    ]
    for time, activity in routine:
        col1, col2 = st.columns([1, 3])
        with col1:
            st.markdown(f"""<div style="background:linear-gradient(135deg,#667eea,#764ba2);color:white;border-radius:8px;padding:0.4rem;text-align:center;font-weight:600;">
            ⏰ {time}</div>""", unsafe_allow_html=True)
        with col2:
            st.markdown(f"""<div class="info-box" style="margin:0.2rem 0;">✅ {activity}</div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════
# PAGE 9: BMI বিশ্লেষণ
# ═══════════════════════════════════════════════════════════════════
elif page == "bmi":
    st.markdown("## 📊 BMI ও স্বাস্থ্য বিশ্লেষণ")
    col1, col2, col3 = st.columns(3)
    with col1:
        weight_bmi = st.number_input("ওজন (কেজি):", 10.0, 300.0, 65.0, 0.5)
    with col2:
        height_bmi = st.number_input("উচ্চতা (সেমি):", 50.0, 250.0, 160.0, 0.5)
    with col3:
        age_bmi = st.number_input("বয়স:", 5, 120, 30)
        gender_bmi = st.selectbox("লিঙ্গ:", ["পুরুষ", "মহিলা"])

    if st.button("📊 BMI হিসাব করুন", type="primary", use_container_width=True):
        bmi = weight_bmi / ((height_bmi/100)**2)
        ideal_low = 18.5 * (height_bmi/100)**2
        ideal_high = 24.9 * (height_bmi/100)**2

        if bmi < 18.5:
            cat = "কম ওজন (Underweight)"; color = "#2196F3"; advice_bmi = "পুষ্টিকর খাবার বেশি খান, ডাক্তারের পরামর্শ নিন।"
        elif bmi < 25:
            cat = "স্বাভাবিক (Normal)"; color = "#4CAF50"; advice_bmi = "চমৎকার! এই ওজন বজায় রাখুন।"
        elif bmi < 30:
            cat = "অতিরিক্ত ওজন (Overweight)"; color = "#FF9800"; advice_bmi = "নিয়মিত ব্যায়াম ও স্বাস্থ্যকর খাবার খান।"
        else:
            cat = "স্থূলতা (Obese)"; color = "#F44336"; advice_bmi = "জরুরি! ডাক্তারের পরামর্শ নিন, ওজন কমানো প্রয়োজন।"

        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.markdown(f"""<div class="metric-card" style="background:linear-gradient(135deg,{color}99,{color});">
            <div class="metric-label">BMI মান</div>
            <div class="metric-value">{bmi:.1f}</div>
            <div>{cat}</div></div>""", unsafe_allow_html=True)
        with col_b:
            st.markdown(f"""<div class="metric-card" style="background:linear-gradient(135deg,#4CAF5099,#4CAF50);">
            <div class="metric-label">আদর্শ ওজন</div>
            <div class="metric-value">{ideal_low:.0f}-{ideal_high:.0f}</div>
            <div>কেজি</div></div>""", unsafe_allow_html=True)
        with col_c:
            diff = weight_bmi - ideal_high if weight_bmi > ideal_high else (ideal_low - weight_bmi if weight_bmi < ideal_low else 0)
            status = f"{'বেশি' if weight_bmi>ideal_high else 'কম'} {diff:.1f} কেজি" if diff > 0 else "আদর্শ পরিসরে"
            st.markdown(f"""<div class="metric-card">
            <div class="metric-label">পার্থক্য</div>
            <div class="metric-value" style="font-size:1.2rem;">{status}</div>
            </div>""", unsafe_allow_html=True)

        st.markdown(f"""<div class="{'success-box' if bmi<25 else 'warning-box' if bmi<30 else 'danger-box'}">
        💡 <strong>পরামর্শ:</strong> {advice_bmi}
        </div>""", unsafe_allow_html=True)

        # Progress bar visualization
        st.markdown("**BMI স্কেল:**")
        bmi_progress = min(1.0, bmi / 40)
        st.progress(bmi_progress)
        st.caption(f"স্বাভাবিক পরিসর: 18.5 – 24.9 | আপনার BMI: {bmi:.1f}")

# ═══════════════════════════════════════════════════════════════════
# PAGE 10: ডায়াবেটিস ঝুঁকি
# ═══════════════════════════════════════════════════════════════════
elif page == "diabetes_risk":
    st.markdown("## 🩺 ডায়াবেটিস ঝুঁকি মূল্যায়ন")
    col1, col2 = st.columns(2)
    with col1:
        d_age = st.number_input("বয়স:", 10, 100, 40)
        d_weight = st.number_input("ওজন (কেজি):", 30.0, 200.0, 70.0)
        d_height = st.number_input("উচ্চতা (সেমি):", 100.0, 220.0, 165.0)
        d_sugar = st.number_input("রক্তে সুগার (mg/dL):", 60, 500, 105)
    with col2:
        d_family = st.checkbox("পরিবারে ডায়াবেটিসের ইতিহাস আছে?")
        d_exercise = st.selectbox("ব্যায়ামের অভ্যাস:", ["নিয়মিত (সপ্তাহে ৫+ দিন)", "মাঝে মাঝে", "নেই বললেই চলে"])
        d_sweet = st.selectbox("মিষ্টি ও কার্বোহাইড্রেট খাওয়ার পরিমাণ:", ["কম", "মাঝারি", "বেশি"])
        d_bp = st.checkbox("উচ্চ রক্তচাপ আছে?")

    if st.button("⚕️ ঝুঁকি বিশ্লেষণ করুন", type="primary", use_container_width=True):
        risk_score = 0
        if d_age >= 45: risk_score += 2
        elif d_age >= 35: risk_score += 1
        bmi_d = d_weight / (d_height/100)**2
        if bmi_d >= 30: risk_score += 3
        elif bmi_d >= 25: risk_score += 2
        if d_sugar >= 126: risk_score += 4
        elif d_sugar >= 100: risk_score += 2
        if d_family: risk_score += 3
        if d_exercise == "নেই বললেই চলে": risk_score += 2
        elif d_exercise == "মাঝে মাঝে": risk_score += 1
        if d_sweet == "বেশি": risk_score += 2
        elif d_sweet == "মাঝারি": risk_score += 1
        if d_bp: risk_score += 2

        max_score = 18
        pct = risk_score / max_score

        if risk_score <= 5:
            level = "🟢 কম ঝুঁকি"; color = "#4CAF50"; box = "success-box"
            advice_d = "আপনার ডায়াবেটিসের ঝুঁকি কম। স্বাস্থ্যকর জীবনযাপন অব্যাহত রাখুন।"
        elif risk_score <= 10:
            level = "🟡 মাঝারি ঝুঁকি"; color = "#FF9800"; box = "warning-box"
            advice_d = "মাঝারি ঝুঁকিতে আছেন। নিয়মিত ব্যায়াম করুন, মিষ্টি কমান এবং বছরে একবার সুগার পরীক্ষা করুন।"
        else:
            level = "🔴 উচ্চ ঝুঁকি"; color = "#F44336"; box = "danger-box"
            advice_d = "উচ্চ ঝুঁকিতে আছেন! দ্রুত ডায়াবেটোলজিস্টের পরামর্শ নিন।"

        st.markdown(f"""<div class="metric-card" style="background:linear-gradient(135deg,{color}99,{color});">
        <div class="metric-label">ডায়াবেটিস ঝুঁকি স্কোর</div>
        <div class="metric-value">{risk_score}/{max_score}</div>
        <div style="font-size:1.2rem;">{level}</div></div>""", unsafe_allow_html=True)
        st.progress(pct)
        st.markdown(f"""<div class="{box}">💡 <strong>পরামর্শ:</strong> {advice_d}</div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════
# PAGE 11: প্রেসার বিশ্লেষণ
# ═══════════════════════════════════════════════════════════════════
elif page == "bp_analysis":
    st.markdown("## 💓 রক্তচাপ (BP) বিশ্লেষণ")
    col1, col2 = st.columns(2)
    with col1:
        bp_s = st.number_input("সিস্টোলিক (উপরের সংখ্যা):", 60, 300, 120)
    with col2:
        bp_d = st.number_input("ডায়াস্টোলিক (নিচের সংখ্যা):", 40, 200, 80)

    if st.button("💓 বিশ্লেষণ করুন", type="primary", use_container_width=True):
        if bp_s < 90 or bp_d < 60:
            cat = "⬇️ Low BP (নিম্ন রক্তচাপ)"; color = "#2196F3"
            desc = "রক্তচাপ স্বাভাবিকের চেয়ে কম।"
            advice_bp = ["বেশি পানি পান করুন", "লবণ সামান্য বাড়ান", "হঠাৎ উঠে দাঁড়াবেন না", "ডাক্তারের পরামর্শ নিন"]
        elif bp_s <= 120 and bp_d <= 80:
            cat = "✅ Normal BP (স্বাভাবিক)"; color = "#4CAF50"
            desc = "আপনার রক্তচাপ সম্পূর্ণ স্বাভাবিক।"
            advice_bp = ["বর্তমান জীবনযাপন বজায় রাখুন", "নিয়মিত ব্যায়াম করুন", "কম লবণ খান"]
        elif bp_s <= 129 and bp_d < 80:
            cat = "⚠️ Elevated (উচ্চের দিকে)"; color = "#8BC34A"
            desc = "রক্তচাপ সামান্য উপরে।"
            advice_bp = ["লবণ কমান", "নিয়মিত ব্যায়াম করুন", "ওজন নিয়ন্ত্রণ করুন"]
        elif (bp_s <= 139 or bp_d <= 89):
            cat = "⚠️ Pre-Hypertension (পূর্ব উচ্চ রক্তচাপ)"; color = "#FF9800"
            desc = "উচ্চ রক্তচাপের পূর্বাবস্থা।"
            advice_bp = ["লবণ কমিয়ে দিন", "ব্যায়াম শুরু করুন", "মানসিক চাপ কমান", "ডাক্তার দেখান"]
        elif bp_s <= 179 or bp_d <= 109:
            cat = "🔴 Hypertension Stage 1"; color = "#F44336"
            desc = "উচ্চ রক্তচাপ - চিকিৎসা প্রয়োজন।"
            advice_bp = ["অবিলম্বে ডাক্তার দেখান", "লবণ বন্ধ করুন", "ধূমপান বন্ধ করুন", "নিয়মিত ওষুধ খান"]
        else:
            cat = "🚨 Hypertension Stage 2 / Crisis"; color = "#B71C1C"
            desc = "অত্যন্ত বিপজ্জনক! জরুরি চিকিৎসা প্রয়োজন।"
            advice_bp = ["এখনই হাসপাতালে যান!", "999 নম্বরে কল করুন", "মাথা উঁচু রেখে শুয়ে থাকুন"]

        st.markdown(f"""<div class="metric-card" style="background:linear-gradient(135deg,{color}99,{color});">
        <div class="metric-label">রক্তচাপ মূল্যায়ন</div>
        <div class="metric-value">{bp_s}/{bp_d} mmHg</div>
        <div style="font-size:1.1rem;">{cat}</div></div>""", unsafe_allow_html=True)
        st.markdown(f"📋 **{desc}**")
        st.markdown("**পরামর্শ:**")
        for a in advice_bp:
            st.markdown(f"{'<div class=\"danger-box\">' if '!' in a else '<div class=\"info-box\">'} ✅ {a}</div>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════
# PAGE 12: স্বাস্থ্য রিপোর্ট
# ═══════════════════════════════════════════════════════════════════
elif page == "report":
    st.markdown("## 📄 স্বাস্থ্য রিপোর্ট")
    st.markdown("### রোগীর তথ্য দিন")

    col1, col2 = st.columns(2)
    with col1:
        r_name = st.text_input("রোগীর নাম:")
        r_age = st.number_input("বয়স:", 1, 120, 30)
        r_gender = st.selectbox("লিঙ্গ:", ["পুরুষ", "মহিলা", "অন্যান্য"])
    with col2:
        r_bp = st.text_input("রক্তচাপ (যেমন: 120/80):", "120/80")
        r_sugar = st.number_input("রক্তে সুগার (mg/dL):", 60, 600, 100)
        r_pulse = st.number_input("পালস:", 30, 250, 75)

    r_weight = st.number_input("ওজন (কেজি):", 10.0, 200.0, 60.0)
    r_height = st.number_input("উচ্চতা (সেমি):", 50.0, 250.0, 160.0)
    r_symptoms = st.text_area("উপসর্গ:", placeholder="রোগীর উপসর্গগুলো লিখুন...")
    r_disease = st.text_input("সম্ভাব্য রোগ (যদি জানা থাকে):")

    if st.button("📄 রিপোর্ট তৈরি করুন", type="primary", use_container_width=True) and r_name:
        bmi_r = r_weight / (r_height/100)**2
        report_date = datetime.now().strftime("%d/%m/%Y %H:%M")

        report_html = f"""
<div style="background:white;border-radius:16px;padding:2rem;border:2px solid #1976d2;font-family:'Hind Siliguri',sans-serif;">
  <div style="text-align:center;background:linear-gradient(135deg,#1a1a2e,#0f3460);color:white;padding:1.5rem;border-radius:12px;margin-bottom:1.5rem;">
    <h2 style="margin:0;font-size:1.8rem;">🏥 স্বাস্থ্য সঙ্গী ১.০</h2>
    <p style="margin:0.3rem 0 0;opacity:0.8;">Created by Kaliagonj Naziraton High School (Soundarjya)</p>
    <p style="margin:0.2rem 0 0;opacity:0.7;font-size:0.9rem;">রিপোর্ট তারিখ: {report_date}</p>
  </div>

  <h3 style="color:#1976d2;border-bottom:2px solid #1976d2;padding-bottom:0.5rem;">👤 রোগীর তথ্য</h3>
  <table style="width:100%;border-collapse:collapse;">
    <tr><td style="padding:0.4rem;font-weight:600;">নাম:</td><td style="padding:0.4rem;">{r_name}</td>
        <td style="padding:0.4rem;font-weight:600;">বয়স:</td><td style="padding:0.4rem;">{r_age} বছর</td></tr>
    <tr><td style="padding:0.4rem;font-weight:600;">লিঙ্গ:</td><td style="padding:0.4rem;">{r_gender}</td>
        <td style="padding:0.4rem;font-weight:600;">তারিখ:</td><td style="padding:0.4rem;">{report_date}</td></tr>
  </table>

  <h3 style="color:#1976d2;border-bottom:2px solid #1976d2;padding-bottom:0.5rem;margin-top:1.5rem;">📊 ভাইটাল সাইন</h3>
  <table style="width:100%;border-collapse:collapse;background:#f8f9ff;border-radius:8px;">
    <tr style="background:#e3f2fd;">
      <th style="padding:0.5rem;text-align:left;">পরীক্ষা</th>
      <th style="padding:0.5rem;text-align:left;">ফলাফল</th>
      <th style="padding:0.5rem;text-align:left;">স্বাভাবিক মান</th>
      <th style="padding:0.5rem;text-align:left;">মন্তব্য</th>
    </tr>
    <tr><td style="padding:0.5rem;">রক্তচাপ</td><td>{r_bp}</td><td>120/80 mmHg</td><td>—</td></tr>
    <tr style="background:#f8f9ff;"><td style="padding:0.5rem;">রক্তে সুগার</td><td>{r_sugar} mg/dL</td><td>70-100 mg/dL</td>
      <td>{'✅ স্বাভাবিক' if r_sugar<=100 else '⚠️ পরীক্ষা করুন'}</td></tr>
    <tr><td style="padding:0.5rem;">পালস</td><td>{r_pulse} bpm</td><td>60-100 bpm</td>
      <td>{'✅ স্বাভাবিক' if 60<=r_pulse<=100 else '⚠️ অস্বাভাবিক'}</td></tr>
    <tr style="background:#f8f9ff;"><td style="padding:0.5rem;">BMI</td><td>{bmi_r:.1f}</td><td>18.5-24.9</td>
      <td>{'✅ স্বাভাবিক' if 18.5<=bmi_r<=24.9 else '⚠️ পরীক্ষা করুন'}</td></tr>
    <tr><td style="padding:0.5rem;">ওজন</td><td>{r_weight} কেজি</td><td>উচ্চতা অনুযায়ী</td><td>—</td></tr>
  </table>

  {"<h3 style='color:#1976d2;border-bottom:2px solid #1976d2;padding-bottom:0.5rem;margin-top:1.5rem;'>🩺 উপসর্গ ও সম্ভাব্য রোগ</h3><p>উপসর্গ: " + r_symptoms + "</p><p>সম্ভাব্য রোগ: <strong>" + (r_disease or "নির্ধারিত নয়") + "</strong></p>" if r_symptoms else ""}

  <div style="background:#fff3e0;border-radius:10px;padding:1rem;margin-top:1.5rem;border-left:4px solid #f57c00;">
    ⚠️ <strong>দ্রষ্টব্য:</strong> এই রিপোর্টটি শুধুমাত্র প্রাথমিক তথ্যের উপর ভিত্তি করে তৈরি।
    এটি ডাক্তারের বিকল্প নয়। সঠিক রোগ নির্ণয়ের জন্য অবশ্যই যোগ্য চিকিৎসকের পরামর্শ নিন।
  </div>
</div>
"""
        st.markdown(report_html, unsafe_allow_html=True)
        st.download_button("📥 রিপোর্ট ডাউনলোড করুন (HTML)", report_html,
                           file_name=f"health_report_{r_name}_{datetime.now().strftime('%Y%m%d')}.html",
                           mime="text/html")

# ═══════════════════════════════════════════════════════════════════
# PAGE 13: টিকা রিমাইন্ডার
# ═══════════════════════════════════════════════════════════════════
elif page == "vaccine":
    st.markdown("## 💉 টিকা রিমাইন্ডার")
    tab1, tab2, tab3 = st.tabs(["👶 শিশুদের টিকা", "🤰 গর্ভবতী মায়ের টিকা", "🧑 প্রাপ্তবয়স্কদের টিকা"])

    with tab1:
        st.markdown("### বাংলাদেশ EPI (সম্প্রসারিত টিকাদান কর্মসূচি)")
        for v in VACCINATION_SCHEDULE:
            st.markdown(f"""<div class="info-box">
            💉 <strong>{v['name']}</strong> — ⏰ {v['age']}<br>
            🛡️ সুরক্ষা: {v['protects']}<br>
            📍 সরকারি স্বাস্থ্যকেন্দ্র থেকে বিনামূল্যে
            </div>""", unsafe_allow_html=True)

    with tab2:
        pregnant_vaccines = [
            ("টিটেনাস টক্সয়েড (TT-1)", "গর্ভের প্রথম সফরে", "ধনুষ্টংকার প্রতিরোধ"),
            ("টিটেনাস টক্সয়েড (TT-2)", "TT-1 এর ৪ সপ্তাহ পর", "দীর্ঘমেয়াদী সুরক্ষা"),
            ("ইনফ্লুয়েঞ্জা", "যেকোনো ত্রৈমাসিকে", "ফ্লু ও শ্বাসতন্ত্রের সংক্রমণ"),
        ]
        for name, time, protects in pregnant_vaccines:
            st.markdown(f"""<div class="info-box">💉 <strong>{name}</strong> — {time}<br>🛡️ {protects}</div>""", unsafe_allow_html=True)

    with tab3:
        adult_vaccines = [
            ("COVID-19 বুস্টার", "প্রতি বছর বা ডাক্তারের পরামর্শে"),
            ("ইনফ্লুয়েঞ্জা", "প্রতি বছর (বিশেষত বয়স্ক ও ডায়াবেটিক)"),
            ("হেপাটাইটিস বি", "৩ ডোজ — না নিয়ে থাকলে"),
            ("নিউমোকক্কাল", "৬৫+ বছর বা দীর্ঘমেয়াদী রোগীদের জন্য"),
            ("জলাতংক (ARV)", "কুকুর বা বানরে কামড় দিলে"),
        ]
        for name, info in adult_vaccines:
            st.markdown(f"""<div class="info-box">💉 <strong>{name}</strong><br>ℹ️ {info}</div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════
# PAGE 14: পুষ্টি পরামর্শ
# ═══════════════════════════════════════════════════════════════════
elif page == "nutrition":
    st.markdown("## 🥗 খাবার ও পুষ্টি পরামর্শ")
    condition = st.selectbox("আপনার অবস্থা/রোগ:", ["সাধারণ সুস্থ ব্যক্তি","ডায়াবেটিস রোগী","উচ্চ রক্তচাপ","কিডনি রোগী","শিশু (৬মাস-৫বছর)","গর্ভবতী মা","হৃদরোগ","গ্যাস্ট্রিক/আলসার"])

    key_map = {
        "সাধারণ সুস্থ ব্যক্তি": "general",
        "ডায়াবেটিস রোগী": "diabetes",
        "উচ্চ রক্তচাপ": "hypertension",
        "কিডনি রোগী": "kidney",
        "শিশু (৬মাস-৫বছর)": "child",
        "গর্ভবতী মা": "pregnant",
        "হৃদরোগ": "heart",
        "গ্যাস্ট্রিক/আলসার": "gastric",
    }
    key = key_map.get(condition, "general")
    advice_list = NUTRITION_ADVICE.get(key, [])

    col1, col2 = st.columns(2)
    eat_list = [a for a in advice_list if not a.startswith("❌")]
    avoid_list = [a for a in advice_list if a.startswith("❌")]
    with col1:
        st.markdown("### ✅ খেতে পারবেন:")
        for a in eat_list:
            st.markdown(f"""<div class="success-box">{a}</div>""", unsafe_allow_html=True)
    with col2:
        st.markdown("### ❌ এড়িয়ে চলুন:")
        for a in avoid_list:
            st.markdown(f"""<div class="danger-box">{a}</div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════
# PAGE 15: পানির ক্যালকুলেটর
# ═══════════════════════════════════════════════════════════════════
elif page == "water_calc":
    st.markdown("## 💧 পানির প্রয়োজনীয়তা ক্যালকুলেটর")
    col1, col2, col3 = st.columns(3)
    with col1:
        w_weight = st.number_input("ওজন (কেজি):", 20.0, 200.0, 65.0)
    with col2:
        w_activity = st.selectbox("শারীরিক কার্যক্রম:", ["কম (বসে থাকা কাজ)", "মাঝারি (হাঁটাচলা)", "বেশি (শ্রমজীবী/খেলাধুলা)"])
    with col3:
        w_weather = st.selectbox("আবহাওয়া:", ["স্বাভাবিক", "গরম/আর্দ্র", "ঠান্ডা"])

    base = w_weight * 35  # ml
    if w_activity == "মাঝারি (হাঁটাচলা)": base *= 1.2
    elif w_activity == "বেশি (শ্রমজীবী/খেলাধুলা)": base *= 1.5
    if w_weather == "গরম/আর্দ্র": base *= 1.2
    elif w_weather == "ঠান্ডা": base *= 0.9

    liters = base / 1000
    glasses = base / 250

    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.markdown(f"""<div class="metric-card">
        <div class="metric-label">💧 প্রতিদিন পানি</div>
        <div class="metric-value">{liters:.1f}L</div>
        <div>লিটার</div></div>""", unsafe_allow_html=True)
    with col_b:
        st.markdown(f"""<div class="metric-card" style="background:linear-gradient(135deg,#00b4db,#0083b0);">
        <div class="metric-label">🥛 গ্লাস (২৫০মিলি)</div>
        <div class="metric-value">{glasses:.0f}টি</div>
        <div>গ্লাস পানি</div></div>""", unsafe_allow_html=True)
    with col_c:
        st.markdown(f"""<div class="metric-card" style="background:linear-gradient(135deg,#43e97b,#38f9d7);">
        <div class="metric-label">⏰ প্রতি ঘন্টায়</div>
        <div class="metric-value">{(liters/16):.2f}L</div>
        <div>জাগ্রত থাকা সময়ে</div></div>""", unsafe_allow_html=True)

    st.markdown("### 💡 পানি পানের টিপস:")
    water_tips = [
        "সকালে উঠে খালি পেটে ১-২ গ্লাস পানি পান করুন",
        "খাওয়ার ৩০ মিনিট আগে ১ গ্লাস পানি পান করুন",
        "প্রতি ঘন্টায় অন্তত ১ গ্লাস পানি পান করুন",
        "প্রস্রাবের রং হলুদ হলে আরও পানি পান করুন",
        "চা-কফি পানের পাশাপাশি পানি পানও বজায় রাখুন",
    ]
    for tip in water_tips:
        st.markdown(f"""<div class="info-box">💧 {tip}</div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════
# PAGE 16: স্বাস্থ্য কুইজ
# ═══════════════════════════════════════════════════════════════════
elif page == "quiz":
    st.markdown("## 🧠 স্বাস্থ্য সচেতনতা কুইজ")
    st.info("প্রতিটি প্রশ্নের সঠিক উত্তর বেছে নিন। আপনার স্বাস্থ্য জ্ঞান যাচাই করুন!")

    if "quiz_answers" not in st.session_state:
        st.session_state.quiz_answers = {}
    if "quiz_submitted" not in st.session_state:
        st.session_state.quiz_submitted = False

    selected_quiz = HEALTH_QUIZ[:20]

    if not st.session_state.quiz_submitted:
        for i, q in enumerate(selected_quiz):
            st.markdown(f"**{i+1}. {q['question']}**")
            answer = st.radio("", q['options'], key=f"q_{i}", label_visibility="collapsed")
            st.session_state.quiz_answers[i] = answer
            st.markdown("---")

        if st.button("✅ ফলাফল দেখুন", type="primary", use_container_width=True):
            st.session_state.quiz_submitted = True
            st.rerun()
    else:
        score = 0
        for i, q in enumerate(selected_quiz):
            user_ans = st.session_state.quiz_answers.get(i, "")
            correct = q['correct']
            is_correct = user_ans == correct
            if is_correct: score += 1
            emoji = "✅" if is_correct else "❌"
            box = "success-box" if is_correct else "danger-box"
            st.markdown(f"""<div class="{box}">
            {emoji} <strong>প্র. {i+1}:</strong> {q['question']}<br>
            আপনার উত্তর: {user_ans}<br>
            {'✅ সঠিক!' if is_correct else f'❌ সঠিক উত্তর: {correct}'}
            </div>""", unsafe_allow_html=True)

        pct = score / len(selected_quiz)
        if pct >= 0.8: level = "🏆 চমৎকার! আপনি স্বাস্থ্য সচেতন।"; color = "#4CAF50"
        elif pct >= 0.5: level = "👍 ভালো! আরও জ্ঞান অর্জন করুন।"; color = "#FF9800"
        else: level = "📚 আরও পড়াশোনা করুন।"; color = "#F44336"

        st.markdown(f"""<div class="metric-card" style="background:linear-gradient(135deg,{color}99,{color});">
        <div class="metric-label">আপনার স্কোর</div>
        <div class="metric-value">{score}/{len(selected_quiz)}</div>
        <div>{level}</div></div>""", unsafe_allow_html=True)
        st.progress(pct)

        if st.button("🔄 আবার চেষ্টা করুন", use_container_width=True):
            st.session_state.quiz_submitted = False
            st.session_state.quiz_answers = {}
            st.rerun()

# ═══════════════════════════════════════════════════════════════════
# PAGE 17: রোগ প্রতিরোধ গাইড
# ═══════════════════════════════════════════════════════════════════
elif page == "prevention":
    st.markdown("## 🛡️ রোগ প্রতিরোধ গাইড")
    for disease_prev in DISEASE_PREVENTION:
        with st.expander(f"🛡️ {disease_prev['name']} প্রতিরোধ"):
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**⚠️ লক্ষণ সম্পর্কে জানুন:**")
                for sym in disease_prev['symptoms']:
                    st.markdown(f"• {sym}")
            with col2:
                st.markdown("**✅ প্রতিরোধের উপায়:**")
                for prev in disease_prev['prevention']:
                    st.markdown(f"• {prev}")
            if disease_prev.get('treatment'):
                st.markdown(f"**💊 চিকিৎসা:** {disease_prev['treatment']}")

# ═══════════════════════════════════════════════════════════════════
# PAGE 18: রক্তদাতা খোঁজা
# ═══════════════════════════════════════════════════════════════════
elif page == "blood_donor":
    st.markdown("## ❤️ রক্তদাতা খোঁজা")
    st.markdown("""<div class="info-box">
    ❤️ <strong>রক্তদান মহৎ কাজ।</strong> একজন দাতার রক্ত ৩ জনের জীবন বাঁচাতে পারে।
    </div>""", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        blood_group = st.selectbox("প্রয়োজনীয় রক্তের গ্রুপ:", ["A+","A-","B+","B-","O+","O-","AB+","AB-","সব"])
    with col2:
        location = st.selectbox("জেলা:", ["সব","পঞ্চগড়","ঠাকুরগাঁও"])
    with col3:
        st.text_input("মোবাইল নম্বর (নিজের):", placeholder="01XXXXXXXXX")

    filtered_donors = BLOOD_DONORS
    if blood_group != "সব": filtered_donors = [d for d in filtered_donors if d['blood_group']==blood_group]
    if location != "সব": filtered_donors = [d for d in filtered_donors if d.get('district')==location]

    st.markdown(f"**{len(filtered_donors)}জন রক্তদাতা পাওয়া গেছে**")
    for donor in filtered_donors:
        st.markdown(f"""<div class="blood-card">
        <span style="background:#e53935;color:white;border-radius:6px;padding:2px 8px;font-weight:700;font-size:1.1rem;">
        🩸 {donor['blood_group']}</span>
        <strong style="margin-left:0.5rem;">{donor['name']}</strong><br>
        📍 {donor.get('area','')} — {donor.get('district','')}<br>
        📞 {donor['phone']}
        </div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════
# PAGE 19: মেডিকেল ক্যালকুলেটর
# ═══════════════════════════════════════════════════════════════════
elif page == "calc":
    st.markdown("## 🔢 মেডিকেল ক্যালকুলেটর")
    tab1, tab2, tab3, tab4 = st.tabs(["⚖️ BMI","🔥 BMR","🎯 Ideal Weight","🤰 Due Date"])

    with tab1:
        w = st.number_input("ওজন (কেজি):", 10.0, 300.0, 65.0, key="c_w")
        h = st.number_input("উচ্চতা (সেমি):", 50.0, 250.0, 165.0, key="c_h")
        if w and h:
            bmi_c = w/(h/100)**2
            st.markdown(f"""<div class="metric-card"><div class="metric-label">BMI</div>
            <div class="metric-value">{bmi_c:.2f}</div>
            <div>{'কম ওজন' if bmi_c<18.5 else 'স্বাভাবিক' if bmi_c<25 else 'অতিরিক্ত' if bmi_c<30 else 'স্থূলতা'}</div></div>""",
            unsafe_allow_html=True)

    with tab2:
        w2 = st.number_input("ওজন (কেজি):", 10.0, 300.0, 65.0, key="c_w2")
        h2 = st.number_input("উচ্চতা (সেমি):", 50.0, 250.0, 165.0, key="c_h2")
        a2 = st.number_input("বয়স:", 10, 100, 30, key="c_a2")
        g2 = st.selectbox("লিঙ্গ:", ["পুরুষ","মহিলা"], key="c_g2")
        act2 = st.selectbox("কার্যক্রম স্তর:", ["শুধু বিশ্রাম","হালকা সক্রিয়","মাঝারি সক্রিয়","বেশি সক্রিয়","অতিরিক্ত সক্রিয়"])
        if st.button("BMR হিসাব", key="bmr_btn"):
            if g2 == "পুরুষ":
                bmr = 88.362 + (13.397*w2) + (4.799*h2) - (5.677*a2)
            else:
                bmr = 447.593 + (9.247*w2) + (3.098*h2) - (4.330*a2)
            mult = {"শুধু বিশ্রাম":1.2,"হালকা সক্রিয়":1.375,"মাঝারি সক্রিয়":1.55,"বেশি সক্রিয়":1.725,"অতিরিক্ত সক্রিয়":1.9}
            tdee = bmr * mult[act2]
            col_a, col_b = st.columns(2)
            with col_a:
                st.markdown(f"""<div class="metric-card"><div class="metric-label">BMR (বেসাল মেটাবলিক রেট)</div>
                <div class="metric-value">{bmr:.0f}</div><div>ক্যালরি/দিন</div></div>""", unsafe_allow_html=True)
            with col_b:
                st.markdown(f"""<div class="metric-card" style="background:linear-gradient(135deg,#f093fb,#f5576c);">
                <div class="metric-label">TDEE (মোট প্রয়োজন)</div>
                <div class="metric-value">{tdee:.0f}</div><div>ক্যালরি/দিন</div></div>""", unsafe_allow_html=True)

    with tab3:
        h3 = st.number_input("উচ্চতা (সেমি):", 50.0, 250.0, 165.0, key="c_h3")
        g3 = st.selectbox("লিঙ্গ:", ["পুরুষ","মহিলা"], key="c_g3")
        if h3:
            if g3 == "পুরুষ":
                ideal = 50 + 0.91 * (h3 - 152.4)
            else:
                ideal = 45.5 + 0.91 * (h3 - 152.4)
            st.markdown(f"""<div class="metric-card"><div class="metric-label">আদর্শ ওজন (Devine Formula)</div>
            <div class="metric-value">{ideal:.1f} কেজি</div>
            <div>সীমা: {ideal-5:.1f} – {ideal+5:.1f} কেজি</div></div>""", unsafe_allow_html=True)

    with tab4:
        lmp = st.date_input("শেষ মাসিকের তারিখ (LMP):", value=date.today()-timedelta(days=60))
        if lmp:
            due_date = lmp + timedelta(days=280)
            weeks = (date.today() - lmp).days // 7
            st.markdown(f"""<div class="metric-card" style="background:linear-gradient(135deg,#f093fb,#f5576c);">
            <div class="metric-label">🤰 আনুমানিক প্রসবের তারিখ</div>
            <div class="metric-value">{due_date.strftime('%d %B %Y')}</div>
            <div>গর্ভকাল: {weeks} সপ্তাহ</div></div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════
# PAGE 20: স্বাস্থ্য সংবাদ
# ═══════════════════════════════════════════════════════════════════
elif page == "news":
    st.markdown("## 📰 স্বাস্থ্য সচেতনতা ও টিপস")
    health_news = [
        {"title":"ডেঙ্গু প্রতিরোধে সতর্কতা","content":"বর্ষা মৌসুমে এডিস মশার প্রজনন রোধে জমা পানি পরিষ্কার রাখুন।","category":"সতর্কতা"},
        {"title":"ডায়াবেটিস নিয়ন্ত্রণের সহজ উপায়","content":"নিয়মিত হাঁটা, মিষ্টি কম খাওয়া এবং নিয়মিত সুগার পরীক্ষা করুন।","category":"স্বাস্থ্য টিপস"},
        {"title":"হার্ট অ্যাটাকের পূর্বলক্ষণ","content":"বুকে চাপ, বাম হাতে ব্যথা, শ্বাসকষ্ট দেখা দিলে দ্রুত হাসপাতালে যান।","category":"জরুরি"},
        {"title":"শিশুর টিকাদান সময়সূচি মেনে চলুন","content":"সরকারি EPI টিকা শিশুকে ১০টি মারাত্মক রোগ থেকে সুরক্ষা দেয়।","category":"শিশু স্বাস্থ্য"},
        {"title":"যক্ষ্মা (TB) সম্পূর্ণ নিরাময়যোগ্য","content":"৬ মাসের সম্পূর্ণ ডটস চিকিৎসায় যক্ষ্মা সম্পূর্ণ ভালো হয়। সরকারি সেন্টারে বিনামূল্যে পাবেন।","category":"রোগ তথ্য"},
    ]
    for news in health_news:
        cat_color = {"সতর্কতা":"#F44336","স্বাস্থ্য টিপস":"#4CAF50","জরুরি":"#FF5722","শিশু স্বাস্থ্য":"#2196F3","রোগ তথ্য":"#9C27B0"}.get(news["category"],"#607D8B")
        st.markdown(f"""<div class="section-card" style="border-left-color:{cat_color};">
        <span style="background:{cat_color};color:white;border-radius:6px;padding:2px 8px;font-size:0.8rem;">{news['category']}</span>
        <h4 style="margin:0.5rem 0 0.3rem;">{news['title']}</h4>
        <p style="margin:0;color:#555;">{news['content']}</p>
        </div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════
# PAGE 21: রোগের ঝুঁকি স্কোর
# ═══════════════════════════════════════════════════════════════════
elif page == "risk_score":
    st.markdown("## ⚠️ রোগের ঝুঁকি স্কোর")
    st.markdown("আপনার তথ্য ও উপসর্গের ভিত্তিতে বিভিন্ন রোগের ঝুঁকি মূল্যায়ন করুন।")

    col1, col2 = st.columns(2)
    with col1:
        rs_age = st.number_input("বয়স:", 10, 100, 40)
        rs_bp_s = st.number_input("সিস্টোলিক BP:", 60, 250, 120)
        rs_sugar = st.number_input("সুগার (mg/dL):", 60, 500, 100)
        rs_smoke = st.checkbox("ধূমপান করেন?")
    with col2:
        rs_weight = st.number_input("ওজন (কেজি):", 30.0, 200.0, 70.0)
        rs_height = st.number_input("উচ্চতা (সেমি):", 100.0, 220.0, 165.0)
        rs_family = st.checkbox("পরিবারে হৃদরোগ বা ডায়াবেটিসের ইতিহাস?")
        rs_exercise = st.checkbox("নিয়মিত ব্যায়াম করেন না?")

    rs_symptoms = st.multiselect("বর্তমান উপসর্গ:", [
        "বুকে ব্যথা","শ্বাসকষ্ট","মাথাব্যথা","মাথা ঘোরা","বেশি তৃষ্ণা",
        "ঘন প্রস্রাব","ক্লান্তি","ওজন হ্রাস","দৃষ্টি ঝাপসা","পা ফোলা"
    ])

    if st.button("⚠️ ঝুঁকি মূল্যায়ন করুন", type="primary", use_container_width=True):
        rs_bmi = rs_weight / (rs_height/100)**2

        risks = {}
        # Heart disease risk
        heart_score = 0
        if rs_age > 45: heart_score += 2
        if rs_bp_s >= 140: heart_score += 3
        if rs_smoke: heart_score += 3
        if rs_family: heart_score += 2
        if rs_bmi >= 30: heart_score += 2
        if "বুকে ব্যথা" in rs_symptoms: heart_score += 4
        if "শ্বাসকষ্ট" in rs_symptoms: heart_score += 2
        risks["❤️ হৃদরোগ"] = min(100, heart_score * 7)

        # Diabetes risk
        diab_score = 0
        if rs_age > 40: diab_score += 2
        if rs_sugar > 126: diab_score += 5
        elif rs_sugar > 100: diab_score += 2
        if rs_family: diab_score += 2
        if rs_bmi >= 30: diab_score += 3
        if "বেশি তৃষ্ণা" in rs_symptoms: diab_score += 3
        if "ঘন প্রস্রাব" in rs_symptoms: diab_score += 3
        risks["🍬 ডায়াবেটিস"] = min(100, diab_score * 6)

        # Stroke risk
        stroke_score = 0
        if rs_bp_s >= 140: stroke_score += 4
        if rs_age > 55: stroke_score += 2
        if rs_smoke: stroke_score += 3
        if "মাথাব্যথা" in rs_symptoms: stroke_score += 2
        if "দৃষ্টি ঝাপসা" in rs_symptoms: stroke_score += 2
        risks["🧠 স্ট্রোক"] = min(100, stroke_score * 7)

        # Kidney risk
        kidney_score = 0
        if rs_bp_s >= 140: kidney_score += 3
        if rs_sugar > 126: kidney_score += 3
        if "পা ফোলা" in rs_symptoms: kidney_score += 3
        if "ঘন প্রস্রাব" in rs_symptoms: kidney_score += 2
        risks["🫘 কিডনি রোগ"] = min(100, kidney_score * 7)

        st.markdown("### 📊 ঝুঁকির মাত্রা:")
        for disease, score in risks.items():
            if score >= 60: risk_label = "🔴 উচ্চ ঝুঁকি"; box = "danger-box"
            elif score >= 30: risk_label = "🟡 মাঝারি ঝুঁকি"; box = "warning-box"
            else: risk_label = "🟢 কম ঝুঁকি"; box = "success-box"

            st.markdown(f"""<div class="{box}">
            <strong>{disease}:</strong> {risk_label} ({score}%)
            </div>""", unsafe_allow_html=True)
            st.progress(score/100)

# ─── Footer ──────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style="text-align:center;padding:1rem;background:linear-gradient(135deg,#1a1a2e,#0f3460);
border-radius:12px;color:white;margin-top:1rem;">
    <strong>🏥 স্বাস্থ্য সঙ্গী ১.০</strong><br>
    <small>Created by Kaliagonj Naziraton High School (Soundarjya)</small><br>
    <small style="color:rgba(255,255,255,0.6);">⚠️ এটি শুধু প্রাথমিক স্বাস্থ্য পরামর্শের জন্য তৈরি। এটি ডাক্তারের বিকল্প নয়।</small>
</div>
""", unsafe_allow_html=True)
