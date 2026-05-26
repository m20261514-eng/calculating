import streamlit as st
import random
import time

# 1. 페이지 설정 및 애니메이션 효과 CSS
st.set_page_config(page_title="신비의 알 역곱셈 게임", page_icon="🥚", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #FFFDF0; }
    /* 문제창 */
    .quiz-box {
        background: white; padding: 25px; border-radius: 25px;
        text-align: center; font-size: 40px; font-weight: bold;
        color: #4A4A4A; border: 5px solid #FFD93D;
        box-shadow: 0px 8px 0px #FFD93D; margin-bottom: 20px;
    }
    .hint-num { color: #FF4B4B !important; }
    
    /* 3x3 키패드 버튼 */
    .stButton>button {
        font-size: 28px !important; border-radius: 15px !important;
        background-color: #FFD93D !important; color: #4A4A4A !important;
        height: 70px !important; width: 100% !important;
        box-shadow: 0px 6px 0px #E6C229 !important; font-weight: bold !important;
    }
    
    /* 등급별 광채 효과 */
    .rare-glow {
        color: #00D2FF; font-size: 30px; font-weight: bold;
        text-shadow: 0 0 10px #00D2FF, 0 0 20px #00D2FF;
        animation: pulse 1.5s infinite;
    }
    .legend-glow {
        color: #FFD700; font-size: 35px; font-weight: bold;
        text-shadow: 0 0 15px #FFD700, 0 0 30px #FFA500;
        animation: shake 0.5s infinite;
    }
    @keyframes pulse { 0% { opacity: 0.7; } 50% { opacity: 1; } 100% { opacity: 0.7; } }
    @keyframes shake { 0% { transform: translate(1px, 1px); } 10% { transform: translate(-1px, -2px); } }
    
    .dashboard-box {
        background: #E3FAFC; padding: 15px; border-radius: 15px;
        border: 2px solid #10B981; font-size: 20px; font-weight: bold;
        color: #099268; display: flex; justify-content: space-between;
    }
    </style>
""", unsafe_allow_html=True)

# 2. 세션 초기화
if 'gold' not in st.session_state:
    st.session_state.score, st.session_state.total, st.session_state.gold = 0, 0, 0
    st.session_state.inputs, st.session_state.status = [], "playing"
    st.session_state.collection = []
    st.session_state.factor1 = random.randint(2, 9)
    st.session_state.factor2 = random.randint(2, 9)
    st.session_state.target_product = st.session_state.factor1 * st.session_state.factor2

def next_question():
    st.session_state.factor1, st.session_state.factor2 = random.randint(2, 9), random.randint(2, 9)
    st.session_state.target_product = st.session_state.factor1 * st.session_state.factor2
    st.session_state.inputs, st.session_state.status = [], "playing"

# 3. 대시보드
st.title("🎒 신비의 알: 역곱셈 퀘스트 🎮")
st.markdown(f"<div class='dashboard-box'><span>⭐ 맞춘 문제: {st.session_state.score}</span><span>💰 골드: {st.session_state.gold} G</span></div>", unsafe_allow_html=True)

# 4. 뽑기 시스템
with st.expander("🥚 [신비의 알뽑기 상점]", expanded=False):
    if st.button("🔮 알뽑기 (100 G)", use_container_width=True):
        if st.session_state.gold >= 100:
            st.session_state.gold -= 100
            rand = random.random()
            if rand < 0.7: # 일반 (70%)
                grade, animal = "일반", random.choice(["🍼 아기오리", "🐥 병아리", "🐹 햄스터"])
                st.info(f"🥚 알이 깨졌어요! [{animal}]이 나왔습니다.")
            elif rand < 0.95: # 희귀 (25%)
                grade, animal = "희귀", random.choice(["🦊 불꽃여우", "🐱 우주고양이", "🦄 페가수스"])
                st.snow()
                st.markdown(f"<div class='rare-glow'>✨ 희귀 등급 발견! [{animal}] ✨</div>", unsafe_allow_html=True)
            else: # 전설 (5%)
                grade, animal = "전설", random.choice(["🐲 황금용", "🦄 유니콘", "🦁 사자왕"])
                st.balloons()
                st.markdown(f"<div class='legend-glow'>👑 전설의 탄생! [{animal}] 👑</div>", unsafe_allow_html=True)
            if animal not in st.session_state.collection: st.session_state.collection.append(animal)
        else: st.error("골드가 부족해요!")

# 5. 문제 출력
p1 = str(st.session_state.inputs[0]) if len(st.session_state.inputs) > 0 else " ? "
p2 = str(st.session_state.inputs[1]) if len(st.session_state.inputs) > 1 else " ? "
if st.session_state.status == "hint": p1 = f"<span class='hint-num'>{st.session_state.factor1}</span>"
st.markdown(f"<div class='quiz-box'>{st.session_state.target_product} = [ {p1} ] × [ {p2} ]</div>", unsafe_allow_html=True)

# 6. 휴대폰 스타일 3x3 키패드
if st.session_state.status in ["playing", "hint"]:
    rows = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    for row in rows:
        cols = st.columns(3)
        for i, num in enumerate(row):
            if cols[i].button(str(num), key=f"k_{num}"):
                st.session_state.inputs.append(num)
                if len(st.session_state.inputs) == 2:
                    if st.session_state.inputs[0] * st.session_state.inputs[1] == st.session_state.target_product:
                        st.session_state.status = "success"
                        st.session_state.score += 1
                        st.session_state.gold += random.randint(8, 13)
                    else:
                        st.session_state.status = "hint"
                        st.session_state.inputs = [st.session_state.factor1]
                    st.rerun()

if st.session_state.status == "success":
    st.success("✅ 정답! 자동으로 다음 문제로 넘어갑니다...")
    time.sleep(1.5); next_question(); st.rerun()
