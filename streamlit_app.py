import streamlit as st
import random

# 1. 페이지 기본 설정 및 귀여운 테마 스타일 적용
st.set_page_config(page_title="재미있는 역곱셈 구구단", page_icon="🎒", layout="centered")

# 계산기 느낌의 귀여운 CSS 스타일 정의
st.markdown("""
    <style>
    /* 전체 배경색 및 폰트 설정 */
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
        color: #FF6B6B;
        border: 5px solid #FFD93D;
        box-shadow: 0px 8px 0px #FFD93D;
        margin-bottom: 25px;
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
    /* 버튼을 눌렀을 때 쏙 들어가는 효과 */
    .stButton>button:active {
        box-shadow: 0px 1px 0px #E6C229 !important;
        transform: translateY(5px);
    }
    /* 점수판 스타일 */
    .score-box {
        font-size: 20px;
        font-weight: bold;
        color: #6C5CE7;
        text-align: right;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# 2. 세션 상태(Session State) 초기화 - 게임 데이터 유지
if 'initialized' not in st.session_state:
    st.session_state.initialized = True
    st.session_state.score = 0
    st.session_state.total = 0
    st.session_state.inputs = []
    st.session_state.status = "playing"  # playing, success, fail
    
    # 첫 문제 생성 (2단 ~ 9단 조합)
    a = random.randint(2, 9)
    b = random.randint(2, 9)
    st.session_state.target_product = a * b

# 새로운 문제를 출제하는 함수
def next_question():
    a = random.randint(2, 9)
    b = random.randint(2, 9)
    st.session_state.target_product = a * b
    st.session_state.inputs = []
    st.session_state.status = "playing"

# 3. 상단 타이틀 및 가이드
st.title("🎒 귀여운 숫자 나라! 역곱셈 게임 🎮")
st.write("정답 숫자를 만들기 위해 어떤 두 수를 곱해야 할지 계산기 버튼을 눌러 맞춰보세요!")

# 점수 표시
st.markdown(f"<div class='score-box'>⭐ 맞춘 문제: {st.session_state.score} / {st.session_state.total}</div>", unsafe_allow_html=True)
st.write("---")

# 4. 문제 화면 표시 (빈칸 채우기 형식)
p1 = str(st.session_state.inputs[0]) if len(st.session_state.inputs) > 0 else " ? "
p2 = str(st.session_state.inputs[1]) if len(st.session_state.inputs) > 1 else " ? "

st.markdown(f"<div class='quiz-box'>{st.session_state.target_product} = [ {p1} ] × [ {p2} ]</div>", unsafe_allow_html=True)

# 5. 계산기식 숫자 버튼 배치 (2부터 9까지)
if st.session_state.status == "playing":
    st.write("👇 **곱할 두 숫자를 순서대로 눌러주세요!**")
    
    # 4열씩 2줄로 배치 (2,3,4,5 / 6,7,8,9)
    col1, col2, col3, col4 = st.columns(4)
    buttons = [2, 3, 4, 5, 6, 7, 8, 9]
    
    for i, num in enumerate(buttons):
        # 인덱스에 따라 열 나누기
        current_col = [col1, col2, col3, col4][i % 4]
        with current_col:
            if st.button(str(num), key=f"btn_{num}"):
                st.session_state.inputs.append(num)
                
                # 숫자가 2개 모두 채워졌을 때 정답 검증
                if len(st.session_state.inputs) == 2:
                    ans1, ans2 = st.session_state.inputs
                    if ans1 * ans2 == st.session_state.target_product:
                        st.session_state.status = "success"
                        st.session_state.score += 1
                    else:
                        st.session_state.status = "fail"
                    st.session_state.total += 1
                st.rerun()

# 6. 정답/오답 결과 화면 및 다음 문제 제어
if st.session_state.status != "playing":
    ans1, ans2 = st.session_state.inputs
    
    if st.session_state.status == "success":
        st.success(f"🎉 **정답이에요! 참 잘했어요!** ({ans1} × {ans2} = {st.session_state.target_product})")
    elif st.session_state.status == "fail":
        st.error(f"😢 **아쉬워요!** 계산해 보니 {ans1} × {ans2} = {ans1 * ans2} 이 나왔어요.")
    
    # 다음 문제 버튼을 큼직하게 배치
    if st.button("다음 문제 풀기 ➡️", use_container_width=True):
        next_question()
        st.rerun()
        
    # 틀렸을 때는 다시 기회를 주는 버튼 제공
    if st.session_state.status == "fail":
        if st.button("🔄 이 문제 다시 도전하기", use_container_width=True):
            st.session_state.inputs = []
            st.session_state.status = "playing"
            st.rerun()
