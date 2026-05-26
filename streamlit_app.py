import streamlit as st
import random
import time

# 1. 페이지 설정
st.set_page_config(page_title="신비의 알 역곱셈 게임", page_icon="🥚", layout="centered")

# 디자인 & 애니메이션 효과 CSS (가로로 긴 버튼 스타일 적용)
st.markdown("""
    <style>
    .stApp { background-color: #FFFDF0; }
    
    /* 문제창 스타일 */
    .quiz-box {
        background: white; padding: 25px; border-radius: 25px;
        text-align: center; font-size: 42px; font-weight: bold;
        color: #4A4A4A; border: 5px solid #FFD93D;
        box-shadow: 0px 8px 0px #FFD93D; margin-bottom: 25px;
    }
    .hint-num { color: #FF4B4B !important; }
    
    /* 3x3 가로로 긴 직사각형 키패드 버튼 */
    .stButton>button {
        font-size: 30px !important; border-radius: 15px !important;
        background-color: #FFD93D !important; color: #4A4A4A !important;
        height: 55px !important; /* 세로를 줄여서 가로로 긴 직사각형 완성 */
        width: 100% !important;
        box-shadow: 0px 5px 0px #E6C229 !important; font-weight: bold !important;
        transition: all 0.1s ease; margin-bottom: 8px;
    }
    .stButton>button:active { transform: translateY(3px); box-shadow: 0px 2px 0px #E6C229 !important; }
    
    /* 지우기 버튼 전용 스타일 (주황색으로 포인트를 줘서 찾기 쉽게 함) */
    div[data-testid="stBlock"] button:contains("지우기") {
        background-color: #FF9233 !important;
        color: white !important;
        box-shadow: 0px 5px 0px #DD6B11 !important;
    }
    
    /* 등급별 화려한 효과 */
    .rare-glow {
        background: linear-gradient(90deg, #00D2FF, #3a7bd5);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        font-size: 35px; font-weight: bold; text-align: center;
        filter: drop-shadow(0 0 10px #00D2FF); animation: pulse 1s infinite;
    }
    .legend-glow {
        color: #FFD700; font-size: 45px; font-weight: bold; text-align: center;
        text-shadow: 0 0 20px #FFD700, 0 0 40px #FFA500;
        animation: shake 0.5s infinite;
    }
    @keyframes pulse { 0% { opacity: 0.7; } 50% { opacity: 1; } 100% { opacity: 0.7; } }
    @keyframes shake { 0% { transform: translate(1px, 1px); } 10% { transform: translate(-1px, -1px); } }
    
    .dashboard {
        background: #E3FAFC; padding: 15px; border-radius: 20px;
        border: 2px solid #10B981; font-size: 22px; font-weight: bold;
        color: #099268; display: flex; justify-content: space-between; margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# 2. 세션 상태 초기화
if 'gold' not in st.session_state:
    st.session_state.score, st.session_state.total, st.session_state.gold = 0, 0, 0
    st.session_state.inputs, st.session_state.status = [], "playing"
    st.session_state.collection = []
    st.session_state.factor1 = random.randint(2, 9)
    st.session_state.factor2 = random.randint(2, 9)
    st.session_state.target_product = st.session_state.factor1 * st.session_state.factor2
    st.session_state.egg_anim = ""

def next_question():
    st.session_state.factor1, st.session_state.factor2 = random.randint(2, 9), random.randint(2, 9)
    st.session_state.target_product = st.session_state.factor1 * st.session_state.factor2
    st.session_state.inputs, st.session_state.status = [], "playing"

# 3. 대시보드 및 상점
st.title("🎒 신비의 알 역곱셈 퀘스트 🎮")
st.markdown(f"<div class='dashboard'><span>⭐ 맞춘 문제: {st.session_state.score}</span><span>💰 골드: {st.session_state.gold} G</span></div>", unsafe_allow_html=True)

with st.expander("🥚 [신비의 알뽑기 상점]", expanded=False):
    if st.button("🔮 알뽑기 (100 G)", use_container_width=True):
        if st.session_state.gold >= 100:
            st.session_state.gold -= 100
            rand = random.random()
            if rand < 0.7:
                grade, animal = "일반", random.choice(["🍼 아기오리", "🐥 병아리", "🐹 햄스터", "🐰 토끼", "🦔 도치"])
                st.session_state.egg_anim = f"🥚 일반 등급: [{animal}]이 탄생했어요!"
            elif rand < 0.95:
                grade, animal = "희귀", random.choice(["🦊 불꽃여우", "🐱 우주고양이", "🦄 페가수스", "🐼 푸바오", "🐨 코알라", "🐺 은빛 늑대"])
                st.snow(); st.session_state.egg_anim = f"<div class='rare-glow'>✨ 희귀 등장! [{animal}] ✨</div>"
            else:
                grade, animal = "전설", random.choice(["🐲 황금용", "🦄 레인보우 유니콘", "🦁 사자왕", "🐋 거대 고래", "🦊 구미호"])
                st.balloons(); st.session_state.egg_anim = f"<div class='legend-glow'>👑 전설 강림! [{animal}] 👑</div>"
            if animal not in st.session_state.collection: st.session_state.collection.append(animal)
        else: st.error("골드가 부족해요! 문제를 더 풀어보세요.")
    if st.session_state.egg_anim: st.markdown(st.session_state.egg_anim, unsafe_allow_html=True)

st.write("---")

# 4. 문제 박스 (실시간 누른 숫자 반영 로직 통합)
p1 = " ? "
p2 = " ? "

if st.session_state.status == "playing":
    if len(st.session_state.inputs) >= 1:
        p1 = str(st.session_state.inputs[0])
    if len(st.session_state.inputs) >= 2:
        p2 = str(st.session_state.inputs[1])
elif st.session_state.status == "hint":
    # 힌트 모드일 때는 첫 글자가 무조건 빨간색 힌트 숫자로 고정
    p1 = f"<span class='hint-num'>{st.session_state.factor1}</span>"
    if len(st.session_state.inputs) >= 2:
        p2 = str(st.session_state.inputs[1])

st.markdown(f"<div class='quiz-box'>{st.session_state.target_product} = [ {p1} ] × [ {p2} ]</div>", unsafe_allow_html=True)


# 5. 스마트 3x3 키패드 + 하단 지우기 버튼
if st.session_state.status in ["playing", "hint"]:
    st.write("👇 **곱할 두 숫자를 순서대로 누르세요!**")
    
    # 1 ~ 9 배열 출력
    keys = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    for row in keys:
        cols = st.columns(3)
        for i, val in enumerate(row):
            if cols[i].button(str(val), key=f"key_{val}", use_container_width=True):
                # 숫자는 최대 2개까지만 쌓이도록 제한
                if len(st.session_state.inputs) < 2:
                    st.session_state.inputs.append(val)
                    st.rerun() # 실시간으로 상단 칸에 숫자가 보이도록 즉시 새로고침

    # 🛑 제일 하단에 가로로 꽉 찬 [지우기] 버튼 배치
    if st.button("⌫ 한 글자 지우기", use_container_width=True):
        if st.session_state.status == "playing":
            if len(st.session_state.inputs) > 0:
                st.session_state.inputs.pop() # 가장 마지막에 넣은 숫자 제거
                st.rerun()
        elif st.session_state.status == "hint":
            # 힌트 모드일 때는 두 번째 숫자(index 1)만 지울 수 있게 방어
            if len(st.session_state.inputs) == 2:
                st.session_state.inputs.pop()
                st.rerun()


# 6. 최종 정답 제출 검증 로직 (숫자 2개가 꽉 찼을 때만 작동)
if st.session_state.status in ["playing", "hint"] and len(st.session_state.inputs) == 2:
    # 연산 처리를 위해 잠깐 대기 조절 (학생이 숫자를 0.4초간 눈으로 확인한 후 정답 판정으로 넘어가게 설계)
    time.sleep(0.4)
    
    ans1, ans2 = st.session_state.inputs
    if ans1 * ans2 == st.session_state.target_product:
        st.session_state.status = "success"
        st.session_state.score += 1
        st.session_state.gold += random.randint(8, 13)
        st.rerun()
    else:
        if st.session_state.status == "playing":
            st.session_state.status = "hint"
            # 힌트 모드로 진입하면 첫 자리는 강제로 정답 숫자로 채워줌
            st.session_state.inputs = [st.session_state.factor1]
        else:
            # 힌트 상태에서도 틀리면 실패 처리 없이 숫자를 리셋하여 재시도 기회 제공
            st.session_state.inputs = [st.session_state.factor1]
        st.rerun()

# 7. 정답 연출 및 자동 다음 문제 전환
if st.session_state.status == "success":
    st.success("✅ 정답입니다! 멋져요! 잠시 후 다음 문제로 넘어갑니다...")
    time.sleep(1.8)
    next_question()
    st.rerun()
