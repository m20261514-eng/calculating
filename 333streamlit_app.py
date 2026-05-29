import streamlit as st

st.set_page_config(page_title="수학 게임 대모험 메인", page_icon="🎲", layout="centered")

st.markdown("""
    <style>
    .game-btn {
        display: block;
        width: 80%;
        margin: 20px auto;
        padding: 30px 0;
        font-size: 2rem;
        font-weight: bold;
        border-radius: 20px;
        box-shadow: 0 8px 0 #FFD93D55;
        background: linear-gradient(90deg,#FFF9C6 50%, #BDF6F6 100%);
        color: #2D2D2D !important;
        border: 4px solid #FFD93D;
        text-align: center;
        text-decoration: none;
        transition: 0.13s transform;
    }
    .game-btn:hover { background: #FFE77C; transform: scale(1.04); }
    .main-title {
        font-size: 3rem;
        font-weight: bold;
        color: #156580;
        text-align: center;
        margin-bottom: 35px;
        margin-top: 15px;
        letter-spacing: 2px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='main-title'>🥚 신비의 수학 대모험 선택 화면 🎲</div>", unsafe_allow_html=True)
st.write("원하는 게임을 선택하세요!")

# 역곱셈 게임 버튼
st.markdown(
    '<a class="game-btn" href="https://calculating-yxucv2tj5bz24odkjqygyr.streamlit.app/" target="_blank">⚔️ 역곱셈 게임 바로가기</a>',
    unsafe_allow_html=True
)

# 나눗셈 게임 버튼
st.markdown(
    '<a class="game-btn" href="https://calculating-fk7wjtmwlzqymtkt7efr94.streamlit.app/" target="_blank">🏹 나눗셈 게임 바로가기</a>',
    unsafe_allow_html=True
)

st.info("새 창(탭)에서 열립니다. 두 게임 모두 종료 후에는 이 페이지로 다시 돌아오세요!")
