import streamlit as st
import random
import time

# 1. 페이지 설정
st.set_page_config(page_title="신비의 알 역곱셈 퀘스트", page_icon="🥚", layout="centered")

# CSS: 부르르 떨리는 애니메이션 및 기기별 최적화 디자인
st.markdown("""
    <style>
    .stApp { background-color: #FFFDF0; color: #222222; }
    
    .quiz-box {
        background: white;
        padding: 25px;
        border-radius: 25px;
        text-align: center;
        font-size: 42px;
        font-weight: bold;
        color: #222222; /* 더 진한 검정 */
        border: 5px solid #FFD93D;
        box-shadow: 0px 8px 0px #FFD93D;
        margin-bottom: 25px;
    }
    .hint-num { color: #FF4B4B !important; font-weight: bold; }
    @keyframes vibrate {
        0% { transform: translate(0); }
        20% { transform: translate(-5px, 5px); }
        40% { transform: translate(-5px, -5px); }
        60% { transform: translate(5px, 5px); }
        80% { transform: translate(5px, -5px); }
        100% { transform: translate(0); }
    }
    .egg-shaking {
        font-size: 150px; text-align: center;
        display: block; margin: 20px auto;
        animation: vibrate 0.15s linear infinite;
        color: #444444;
        text-shadow: 1px 1px 6px #FFD93D44;
    }
    .reveal-card {
        background: white; border-radius: 30px; padding: 40px;
        text-align: center; border: 5px solid #FFD93D;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1); margin: 20px 0;
        color: #222222;
    }
    .animal-icon { font-size: 100px; margin-bottom: 10px; }
    .animal-name { font-size: 38px; font-weight: bold; color: #1C2833; }

    .dashboard {
        background: #E3FAFC;
        padding: 15px;
        border-radius: 20px;
        border: 2px solid #10B981;
        font-size: 20px;
        font-weight: bold;
        color: #12615C; /* 더 진한 남색/녹색 */
        display: flex; justify-content: space-between;
        margin-bottom: 20px;
        text-shadow: 0 1px 0 #fff;
    }

    /* 버튼 */
    .stButton>button {
        font-size: 30px !important;
        border-radius: 15px !important;
        background-color: #FFD93D !important;
        color: #222222 !important; /* 진하게 */
        height: 60px !important;
        width: 100% !important;
        box-shadow: 0px 5px 0px #E6C229 !important;
        font-weight: bold !important;
        transition: all 0.1s ease;
        border: 2px solid #C0A100 !important;
        text-shadow: 0 1px 0 #fff8;
    }
    .stButton>button:active { transform: translateY(3px); }
    div[data-testid="stBlock"] button:contains("지우기") {
        background-color: #FF9233 !important;
        color: #fff !important;
        box-shadow: 0px 5px 0px #DD6B11 !important;
        border: 2px solid #B96009 !important;
    }

    @media (max-width: 768px) { /* 모바일·패드 대응 */
        .quiz-box, .reveal-card, .animal-name, .dashboard {
            font-size: 5vw !important; /* 화면너비 기준 상대크기 */
        }
        .stButton>button {
            font-size: 5vw !important;
            height: 48px !important;
        }
        .animal-icon { font-size: 12vw; }
    }
    </style>
""", unsafe_allow_html=True)

# 2. 세션 상태 초기화
if 'gold' not in st.session_state:
    st.session_state.score, st.session_state.total, st.session_state.gold = 0, 0, 0
    st.session_state.inputs, st.session_state.status = [], "playing"
    st.session_state.collection = []
    st.session_state.gacha_step = "idle" # idle, shaking, revealed
    st.session_state.revealed_animal = None
    
    # 첫 문제 생성
    st.session_state.factor1 = random.randint(2, 9)
    st.session_state.factor2 = random.randint(2, 9)
    st.session_state.target_product = st.session_state.factor1 * st.session_state.factor2

def next_question():
    st.session_state.factor1 = random.randint(2, 9)
    st.session_state.factor2 = random.randint(2, 9)
    st.session_state.target_product = st.session_state.factor1 * st.session_state.factor2
    st.session_state.inputs, st.session_state.status = [], "playing"

# 3. 동물 데이터 (사용자 요청 리스트)
animals_data = {
    "일반": ["🍼 아기오리", "🐥 병아리", "🐹 햄스터", "🐰 토끼", "🦔 도치"],
    "희귀": ["🦊 불꽃여우", "🐱 우주고양이", "🦄 페가수스", "🐼 푸바오", "🐨 코알라", "🐺 은빛 늑대"],
    "전설": ["🐲 황금용", "🦄 레인보우 유니콘", "🦁 사자왕", "🐋 거대 고래", "🦊 구미호"]
}

# 4. 상점 가챠 로직
def start_gacha():
    if st.session_state.gold >= 100:
        st.session_state.gold -= 100
        st.session_state.gacha_step = "shaking"
        
        # 등급 결정 (일반 70%, 희귀 25%, 전설 5%)
        rand = random.random()
        if rand < 0.7: tier = "일반"
        elif rand < 0.95: tier = "희귀"
        else: tier = "전설"
        
        st.session_state.revealed_animal = (tier, random.choice(animals_data[tier]))
        if st.session_state.revealed_animal[1] not in st.session_state.collection:
            st.session_state.collection.append(st.session_state.revealed_animal[1])
    else:
        st.error("골드가 부족해요! 문제를 더 풀어서 골드를 모으세요!")

# --- 메인 화면 레이아웃 ---
st.title("🎒 신비의 알 역곱셈 퀘스트 🎮")

# 상단 대시보드
st.markdown(f"<div class='dashboard'><span>⭐ 점수: {st.session_state.score}</span><span>💰 골드: {st.session_state.gold} G</span></div>", unsafe_allow_html=True)

# 5. 알 부화 연출 화면
if st.session_state.gacha_step == "shaking":
    st.markdown("<span class='egg-shaking'>🥚</span>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>알이 부르르~ 깨지려고 해요!</h3>", unsafe_allow_html=True)
    time.sleep(2.5) # 2.5초간 흔들기
    st.session_state.gacha_step = "revealed"
    st.rerun()

elif st.session_state.gacha_step == "revealed":
    tier, animal = st.session_state.revealed_animal
    st.markdown("<div class='reveal-card'>", unsafe_allow_html=True)
    
    # 등급별 특수 효과
    if tier == "전설": st.balloons()
    elif tier == "희귀": st.snow()
    
    # 동물 정보 출력
    st.markdown(f"<div class='animal-icon'>{animal.split()[0]}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='animal-name'>[{tier}] {animal.split()[-1]}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    if st.button("확인 (도감에 저장!)", use_container_width=True):
        st.session_state.gacha_step = "idle"
        st.rerun()

# 6. 기본 게임 모드 (알 부화 중이 아닐 때)
if st.session_state.gacha_step == "idle":
    with st.expander("🥚 [신비의 알뽑기 상점 열기]", expanded=False):
        st.write("100골드로 새로운 동물을 깨워보세요!")
        st.button("🔮 알뽑기 시작!", on_click=start_gacha, use_container_width=True)
        if st.session_state.collection:
            st.write(f"내 도감: {' | '.join(st.session_state.collection)}")

    st.write("---")

    # 문제 화면 (실시간 숫자 반영)
    p1 = str(st.session_state.inputs[0]) if len(st.session_state.inputs) >= 1 else " ? "
    p2 = str(st.session_state.inputs[1]) if len(st.session_state.inputs) >= 2 else " ? "
    
    if st.session_state.status == "hint":
        p1 = f"<span class='hint-num'>{st.session_state.factor1}</span>"

    st.markdown(f"<div class='quiz-box'>{st.session_state.target_product} = [ {p1} ] × [ {p2} ]</div>", unsafe_allow_html=True)

    # 3x3 키패드 및 지우기
    if st.session_state.status in ["playing", "hint"]:
        keys = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        for row in keys:
            cols = st.columns(3)
            for i, val in enumerate(row):
                if cols[i].button(str(val), key=f"key_{val}", use_container_width=True):
                    if len(st.session_state.inputs) < 2:
                        st.session_state.inputs.append(val)
                        st.rerun()

        if st.button("⌫ 지우기", use_container_width=True):
            if len(st.session_state.inputs) > 0:
                if st.session_state.status == "playing" or (st.session_state.status == "hint" and len(st.session_state.inputs) == 2):
                    st.session_state.inputs.pop()
                    st.rerun()

    # 정답 검증 로직 (자동 넘어가기 포함)
    if len(st.session_state.inputs) == 2:
        time.sleep(0.5) # 숫자를 잠시 확인
        ans1, ans2 = st.session_state.inputs
        if ans1 * ans2 == st.session_state.target_product:
            st.success(f"✅ 정답! {random.randint(8, 13)} 골드를 얻었습니다! 💰")
            st.session_state.score += 1
            st.session_state.gold += random.randint(8, 13)
            st.session_state.total += 1
            time.sleep(1.8)
            next_question()
            st.rerun()
        else:
            if st.session_state.status == "playing":
                st.session_state.status = "hint"
                st.session_state.inputs = [st.session_state.factor1]
            else:
                st.session_state.inputs = [st.session_state.factor1]
            st.rerun()
