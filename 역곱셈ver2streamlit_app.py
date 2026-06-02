import streamlit as st
import random
import time

# 1. 페이지 설정
st.set_page_config(page_title="신비의 알 역곱셈 퀘스트", page_icon="🥚", layout="centered")

# CSS (모바일에서도 3x3 키패드 구조를 완벽하게 유지하도록 대폭 수정)
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
        color: #222222;
        border: 5px solid #FFD93D;
        box-shadow: 0px 8px 0px #FFD93D;
        margin-bottom: 25px;
        margin-top: 0 !important;
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
        color: #12615C;
        display: flex; justify-content: space-between;
        margin-bottom: 20px;
        text-shadow: 0 1px 0 #fff;
    }
    
    /* 기본 버튼 디자인 */
    .stButton>button {
        font-size: 30px !important;
        border-radius: 15px !important;
        background-color: #FFD93D !important;
        color: #222222 !important;
        height: 65px !important;
        width: 100% !important;
        box-shadow: 0px 5px 0px #E6C229 !important;
        font-weight: bold !important;
        transition: all 0.1s ease;
        border: 2px solid #C0A100 !important;
        text-shadow: 0 1px 0 #fff8;
    }
    .stButton>button:active { transform: translateY(3px); }
    
    /* 지우기 버튼 전용 스타일 지정 (구조적 선택자 활용) */
    div.keypad-container + div .stButton>button {
        background-color: #FF9233 !important;
        color: #fff !important;
        box-shadow: 0px 5px 0px #DD6B11 !important;
        border: 2px solid #B96009 !important;
        text-shadow: none !important;
        margin-top: 10px;
    }

    /* 🔥 [핵심] 모바일 화면에서 st.columns가 세로로 깨지는 현상 방지 */
    @media (max-width: 768px) {
        h1 {
            font-size: 5.5vw !important;
            line-height: 1.2 !important;
            white-space: normal !important;
            word-wrap: break-word !important;
        }
        .quiz-box, .reveal-card, .animal-name, .dashboard {
            font-size: 5vw !important;
        }
        .stButton>button {
            font-size: 6vw !important;
            height: 55px !important;
        }
        .animal-icon { font-size: 12vw; }
        
        /* 키패드가 있는 가로 블록들을 강제로 row 방향 고정 */
        div[data-testid="stHorizontalBlock"] {
            display: flex !important;
            flex-direction: row !important;
            flex-wrap: nowrap !important;
            gap: 8px !important;
        }
        div[data-testid="stHorizontalBlock"] > div {
            width: 33.33% !important;
            min-width: 0 !important;
        }
    }
    </style>
""", unsafe_allow_html=True)

# 2. 세션 상태 초기화
if 'gold' not in st.session_state:
    st.session_state.score, st.session_state.total, st.session_state.gold = 0, 0, 0
    st.session_state.inputs, st.session_state.status = [], "playing"
    st.session_state.collection = []
    st.session_state.gacha_step = "idle"
    st.session_state.revealed_animal = None
    st.session_state.factor1 = random.randint(2, 9)
    st.session_state.factor2 = random.randint(2, 9)
    st.session_state.target_product = st.session_state.factor1 * st.session_state.factor2

if 'is_answered' not in st.session_state:
    st.session_state.is_answered = False 

def next_question():
    st.session_state.factor1 = random.randint(2, 9)
    st.session_state.factor2 = random.randint(2, 9)
    st.session_state.target_product = st.session_state.factor1 * st.session_state.factor2
    st.session_state.inputs, st.session_state.status = [], "playing"
    st.session_state.is_answered = False 

# 실시간 연타 방지를 위한 백엔드 콜백 함수 정의
def press_key(val):
    if st.session_state.is_answered:
        return  
    if len(st.session_state.inputs) < 2:
        st.session_state.inputs.append(val)
        if len(st.session_state.inputs) == 2:
            st.session_state.is_answered = True

def press_delete():
    if st.session_state.is_answered:
        return  
    if len(st.session_state.inputs) > 0:
        if st.session_state.status == "playing" or (st.session_state.status == "hint" and len(st.session_state.inputs) == 2):
            st.session_state.inputs.pop()

# 3. 동물 데이터
animals_data = {
    "일반": ["🐿️ 다람쥐", "🐥 병아리", "🐹 햄스터", "🐰 토끼", "🦔 도치", "🐭 생쥐"],
    "희귀": ["🦊🔥 불꽃여우", "🐱✨ 우주고양이", "🐧❄️ 아기 펭귄", "🐼 푸바오", "🐨 코알라", "🐺 은빛 늑대", "🦫 카피바라", "🐿️🌰 볼빵빵 다람쥐"],
    "전설": ["🐲 황금용", "🌈🦄 레인보우 유니콘", "🦁👑 사자왕", "🏆🐯 위대한 호랑이", "🦅 바람의 독수리"]
}

# 4. 상점 가챠 로직
def start_gacha():
    if st.session_state.gold >= 100:
        st.session_state.gold -= 100
        st.session_state.gacha_step = "shaking"
        rand = random.random()
        if rand < 0.8: tier = "일반"
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

# 5. 알 부화 연출
if st.session_state.gacha_step == "shaking":
    st.markdown("<span class='egg-shaking'>🥚</span>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>알이 부르르~ 깨지려고 해요!</h3>", unsafe_allow_html=True)
    time.sleep(2.5)
    st.session_state.gacha_step = "revealed"
    st.rerun()
elif st.session_state.gacha_step == "revealed":
    tier, animal = st.session_state.revealed_animal
    st.markdown("<div class='reveal-card'>", unsafe_allow_html=True)
    if tier == "전설": st.balloons()
    elif tier == "희귀": st.snow()
    st.markdown(f"<div class='animal-icon'>{animal.split()[0]}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='animal-name'>[{tier}] {animal.split()[-1]}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    if st.button("확인 (도감에 저장!)", use_container_width=True):
        st.session_state.gacha_step = "idle"
        st.rerun()

# 6. 기본 게임 모드
if st.session_state.gacha_step == "idle":
    # 상점 expander
    with st.expander("🥚 [신비의 알뽑기 상점 열기]", expanded=False):
        st.write("100골드로 새로운 동물을 깨워보세요!")
        st.button("🔮 알뽑기 시작!", on_click=start_gacha, use_container_width=True)
        if st.session_state.collection:
            st.write(f"내 도감: {' | '.join(st.session_state.collection)}")

    # 문제 칸 (expander 아래 바로 표시)
    p1 = str(st.session_state.inputs[0]) if len(st.session_state.inputs) >= 1 else " ? "
    p2 = str(st.session_state.inputs[1]) if len(st.session_state.inputs) >= 2 else " ? "
    if st.session_state.status == "hint":
        p1 = f"<span class='hint-num'>{st.session_state.factor1}</span>"
    st.markdown(f"<div class='quiz-box'>{st.session_state.target_product} = [ {p1} ] × [ {p2} ]</div>", unsafe_allow_html=True)

    # 키패드 영역 (HTML 마커로 감싸 스타일 타겟팅 명확화)
    if st.session_state.status in ["playing", "hint"]:
        st.markdown('<div class="keypad-container"></div>', unsafe_allow_html=True)
        
        keypad = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        for row in keypad:
            cols = st.columns(3, gap="small")
            for i, val in enumerate(row):
                cols[i].button(str(val), key=f"key_{val}", use_container_width=True, 
                               disabled=st.session_state.is_answered, 
                               on_click=press_key, args=(val,))
        
        # 마지막 줄 - 지우기 버튼 (3x3 배열 아래에 딱 맞춤 크기로 배치)
        st.button("⌫ 지우기", key="del_btn", use_container_width=True, 
                  disabled=st.session_state.is_answered, 
                  on_click=press_delete)

    # 정답 검증
    if len(st.session_state.inputs) == 2 and st.session_state.is_answered:
        time.sleep(0.5)
        ans1, ans2 = st.session_state.inputs
        
        if ans1 * ans2 == st.session_state.target_product:
            get_gold = random.randint(8, 13)
            st.success(f"✅ 정답! {get_gold} 골드를 얻었습니다! 💰")
            st.session_state.score += 1
            st.session_state.gold += get_gold
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
            
            st.session_state.is_answered = False 
            st.rerun()
