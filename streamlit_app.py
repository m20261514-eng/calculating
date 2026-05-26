import streamlit as st
import random

# 1. 페이지 기본 설정 및 귀여운 테마 스타일 적용
st.set_page_config(page_title="재미있는 역곱셈 구구단", page_icon="🎒", layout="centered")

# 계산기 느낌의 귀여운 CSS 스타일 정의 (빨간색 힌트 스타일 추가)
st.markdown("""
    <style>
    .stApp {
        background-color: #FFFDF0;
    }
    /* 문제 창 스타일 */
    .quiz-box {
        background-color: #FFFFFF;
        padding: 30px;
        border-radius: 25px;
        text-align: center;
        font-size: 40px;
        font-weight: bold;
        color: #4A4A4A;
        border: 5px solid #FFD93D;
        box-shadow: 0px 8px 0px #FFD93D;
        margin-bottom: 25px;
    }
    /* 빨간색 힌트 숫자 스타일 */
    .hint-num {
        color: #FF4B4B !important;
        font-weight: bold;
    }
    /* 계산기 버튼 스타일 명세 */
    .stButton>button {
        font-size: 28px !important;
        border-radius: 20px !important;
        background-color: #FFD93D !important;
        color: #4A4A4A !important;
        height: 70px !important;
        width: 100% !important;
        border: none !important;
        box-shadow: 0px 6px 0px #E6C229 !important;
        font-weight: bold !important;
        transition: all 0.1s ease;
    }
    .stButton>button:active {
        box-shadow: 0px 1px 0px #E6C229 !important;
        transform: translateY(5px);
    }
    .score-box {
        font-size: 20px;
        font-weight: bold;
        color: #6C5CE7;
        text-align: right;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# 2. 세션 상태(Session State) 초기화
if 'initialized' not in st.session_state:
    st.session_state.initialized = True
    st.session_state.score = 0
    st.session_state.total = 0
    st.session_state.inputs = []
    st.session_state.status = "playing"  # playing, hint, success, fail
    
    # 비밀 정답 숫자 2개 저장 (2단 ~ 9단)
    st.session_state.factor1 = random.randint(2, 9)
    st.session_state.factor2 = random.randint(2, 9)
    st.session_state.target_product = st.session_state.factor1 * st.session_state.factor2

# 새로운 문제를 출제하는 함수
def next_question():
    st.session_state.factor1 = random.randint(2, 9)
    st.session_state.factor2 = random.randint(2, 9)
    st.session_state.target_product = st.session_state.factor1 * st.session_state.factor2
    st.session_state.inputs = []
    st.session_state.status = "playing"

# 3. 상단 타이틀 및 가이드
st.title("🎒 귀여운 숫자 나라! 역곱셈 게임 🎮")
st.write("정답 숫자를 만들기 위해 어떤 두 수를 곱해야 할지 계산기 버튼을 눌러 맞춰보세요!")

# 점수 표시
st.markdown(f"<div class='score-box'>⭐ 맞춘 문제: {st.session_state.score} / {st.session_state.total}</div>", unsafe_allow_html=True)
st.write("---")

# 4. 상태별 문제 화면 표시 (힌트 모드일 때 첫 번째 숫자를 빨간색으로 변경)
if st.session_state.status == "playing":
    p1 = str(st.session_state.inputs[0]) if len(st.session_state.inputs) > 0 else " ? "
    p2 = str(st.session_state.inputs[1]) if len(st.session_state.inputs) > 1 else " ? "
    st.markdown(f"<div class='quiz-box'>{st.session_state.target_product} = [ {p1} ] × [ {p2} ]</div>", unsafe_allow_html=True)

elif st.session_state.status == "hint":
    # 첫 번째 칸에 정답인 factor1을 빨간색 글씨로 강제 노출
    p1 = f"<span class='hint-num'>{st.session_state.factor1}</span>"
    p2 = str(st.session_state.inputs[1]) if len(st.session_state.inputs) > 1 else " ? "
    st.markdown(f"<div class='quiz-box'>{st.session_state.target_product} = [ {p1} ] × [ {p2} ]</div>", unsafe_allow_html=True)

else:  # 정답 확인(success) 또는 완전 오답(fail) 상태
    p1 = str(st.session_state.inputs[0]) if len(st.session_state.inputs) > 0 else "?"
    p2 = str(st.session_state.inputs[1]) if len(st.session_state.inputs) > 1 else "?"
    st.markdown(f"<div class='quiz-box'>{st.session_state.target_product} = [ {p1} ] × [ {p2} ]</div>", unsafe_allow_html=True)


# 5. 계산기 숫자 버튼 및 정답 검증 로직
if st.session_state.status in ["playing", "hint"]:
    if st.session_state.status == "playing":
        st.write("👇 **곱할 두 숫자를 순서대로 눌러주세요!**")
    else:
        st.warning(f"💡 **틀렸지만 괜찮아요! 힌트 찬스!** 첫 번째 숫자는 빨간색 **{st.session_state.factor
