import streamlit as st
import pandas as pd
import os
import time
from datetime import datetime, timedelta

# File path to store scores
data_file = 'scores.csv'

# Initialize or load existing data
def load_data():
    if os.path.exists(data_file):
        return pd.read_csv(data_file)
    else:
        df = pd.DataFrame(columns=['Team ID', 'Run 1', 'Run 2'])
        df.to_csv(data_file, index=False)
        return df

def save_data(df):
    df.to_csv(data_file, index=False)

def calculate_best_scores(df):
    df['Best Score'] = df[['Run 1', 'Run 2']].max(axis=1, skipna=True)
    df_sorted = df.sort_values(by='Best Score', ascending=False).reset_index(drop=True)
    return df_sorted

# Custom page style
st.set_page_config(page_title="Robot Competition Scoreboard", layout="wide")
st.markdown("""
    <style>
    html, body, .main {
        background: linear-gradient(135deg, #f9e2f4, #f7f3e9);
        font-family: 'Segoe UI', sans-serif;
        color: #3a2e2e;
    }
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        text-align: center;
    }
    h1 {
        color: #9d2873;
        font-size: 42px;
        font-weight: bold;
        margin-bottom: 1em;
    }
    h2, h3 {
        color: #bb5c0d;
    }
    .stButton>button {
        background-color: #9d2873 !important;
        color: white !important;
        border-radius: 8px;
        padding: 10px 24px;
        font-weight: 600;
        font-size: 16px;
        border: 2px solid #7c1a54;
    }
    a {
        color: #9d2873;
        font-weight: bold;
        text-decoration: none;
    }
    .stDataFrame, .css-1d391kg {
        border: 2px solid #a36b41;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    p, span, label, div, input, select {
        font-family: 'Segoe UI', sans-serif !important;
        font-size: 16px;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

query_params = st.query_params
page = query_params.get("page", "ranking")

df = load_data()

if page == "score":
    st.title("Nhập điểm")

    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        password = st.text_input("Nhập mật mã để truy cập:", type="password")
        if password == "11111":
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.stop()

    st.subheader("Đồng hồ đếm ngược 2 phút")
    if 'timer_end' not in st.session_state:
        st.session_state.timer_end = None
    if 'timer_running' not in st.session_state:
        st.session_state.timer_running = False

    col1, col2 = st.columns(2)
    with col1:
        if st.button("▶ Bắt đầu"):
            if not st.session_state.timer_running:
                st.session_state.timer_end = datetime.now() + timedelta(minutes=2)
                st.session_state.timer_running = True
    with col2:
        if st.button("🔁 Reset 2 phút"):
            st.session_state.timer_end = None
            st.session_state.timer_running = False

    if st.session_state.timer_running and st.session_state.timer_end:
        remaining = st.session_state.timer_end - datetime.now()
        if remaining.total_seconds() <= 0:
            st.success("⏱️ Hết giờ!")
            st.session_state.timer_running = False
            st.session_state.timer_end = None
        else:
            mins, secs = divmod(int(remaining.total_seconds()), 60)
            st.markdown(f"<h2 style='color:#d11b79;'>⏳ {mins:02d}:{secs:02d}</h2>", unsafe_allow_html=True)
            time.sleep(1)
            st.rerun()
    elif not st.session_state.timer_running:
        st.markdown("<h2 style='color:#888;'>⏳ 02:00</h2>", unsafe_allow_html=True)

    with st.form("score_form"):
        team_id = st.text_input("Team ID")
        run_number = st.selectbox("Lượt thi", ["Run 1", "Run 2"])

        score_plus = st.number_input("Điểm cộng", min_value=0, max_value=1000, step=1, value=0)
        score_minus = st.number_input("Điểm trừ", min_value=0, max_value=100, step=1, value=0)
        score = score_plus - score_minus
        st.markdown(f"###  Tổng điểm: `{score}`")

        submitted = st.form_submit_button("Gửi điểm")

        if submitted:
            if team_id == "":
                st.warning("Vui lòng nhập đầy đủ Team ID.")
            else:
                if team_id in df['Team ID'].values:
                    df.loc[df['Team ID'] == team_id, run_number] = score
                else:
                    new_row = {'Team ID': team_id, 'Run 1': None, 'Run 2': None}
                    new_row[run_number] = score
                    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                save_data(df)
                st.success(f"Đã lưu điểm cho đội {team_id}")


    st.markdown("---")
    st.subheader("Máy tính")
    a = st.number_input("Số A", value=0.0)
    b = st.number_input("Số B", value=0.0)
    operation = st.selectbox("Phép toán", ["+", "-", "*", "/"])

    if operation == "+":
        result = a + b
    elif operation == "-":
        result = a - b
    elif operation == "*":
        result = a * b
    elif operation == "/":
        result = a / b if b != 0 else "Không thể chia cho 0"

    st.write(f"Kết quả: `{result}`")

else:
    st.markdown("""
        <div style='text-align:right; font-size:16px; color:#555;'>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div style='text-align:center;'>
            <img src='https://i.imgur.com/UVCJpTu.png' width='160'>
            <h1>STICK'EM ROBOTIC COMEPETITION</h1>
            <p style='font-size:18px;'>Dưới đây là danh sách các đội thi được xếp hạng theo <strong>điểm cao nhất</strong> trong các lượt thi.<br>Chúc mừng những đội xuất sắc nhất! </p>
        </div>
    """, unsafe_allow_html=True)

    df_ranked = calculate_best_scores(df.copy())
    trophy_emojis = [" 🏆", " 🏆"]
    for i in range(min(2, len(df_ranked))):
        df_ranked.at[i, 'Team ID'] = str(df_ranked.at[i, 'Team ID']) + trophy_emojis[i]

    placeholder = st.empty()
    rows = df_ranked.shape[0]
    i = 0
    while True:
        display_df = pd.concat([df_ranked.iloc[i:], df_ranked.iloc[:i]])
        placeholder.dataframe(
            display_df[['Team ID', 'Run 1', 'Run 2', 'Best Score']].style.format({
                "Run 1": "{:.0f}", "Run 2": "{:.0f}", "Best Score": "{:.0f}"
            }),
            use_container_width=True
        )
        time.sleep(2)
        i = (i + 1) % rows
