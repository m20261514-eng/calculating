import streamlit as st
import random
import time

# 1. 페이지 설정
st.set_page_config(page_title="신비의 알 수학 퀘스트", page_icon="🎮", layout="centered")

# --- 공동 CSS 디자인 (대시보드, 퀴즈박스, 키패드 등) ---
st.markdown("""
    <style>
    .stApp { background-color: #FFFDF0; color: #222222; }
    .menu-title { text-align: center; font-size: 36px; font-weight: bold; margin-bottom: 30px; color: #2C3E50; }
    .quiz-box {
        background: white; padding: 25px; border-radius: 25px; text-align: center;
        font-size: 42px; font-weight: bold; color: #222222;
        border: 5px solid #FFD93D; box-shadow: 0px 8px 0px #FFD93D; margin-bottom: 25px;
    }
    .hint-box {
        color: #FF4B4B !important; font-size: 32px !important; font-weight: bold; text-align: center;
        margin-top: 15px; margin-bottom: 20px; background-color: #FFEBEB; padding: 15px;
        border-radius: 15px; border: 3px dashed #FF4B4B; box-shadow: 0px 4px 0px #FFC1C1;
    }
    @keyframes vibrate {
        0% { transform: translate(0); }
        20% { transform: translate(-5px, 5px); }
        40% { transform: translate(-5px, -5px); }
        60% { transform: translate(5px, 5px); }
        80% { transform: translate(5px, -5px); }
        100% { transform: translate(0); }
    }
    .egg-shaking {
        font-size: 150px; text-align: center; display: block; margin: 20px auto;
        animation: vibrate 0.15s linear infinite; color: #444444; text-shadow: 1px 1px 6px #FFD93D44;
    }
    .reveal-card {
        background: white; border-radius: 30px; padding: 40px; text-align: center;
        border: 5px solid #FFD93D; box-shadow: 0 10px 30px rgba(0,0,0,0.1); margin: 20px 0; color: #222222;
    }
    .animal-icon { font-size: 100px; margin-bottom: 10px; }
    .animal-name { font-size: 38px; font-weight: bold; color: #1C2833; }
    .dashboard {
        background: #E3FAFC; padding: 15px; border-radius: 20px; border: 2px solid #10B981;
        font-size: 20px; font-weight: bold; color: #12615C; display: flex; justify-content: space-between;
        margin-bottom: 20px; text-shadow: 0 1px 0 #fff;
    }
    .stButton>button {
        font-size: 28px !important; border-radius: 15px !important; background-color: #FFD93D !important;
        color: #222222 !important; height: 60px !important; width: 100% !important;
        box-shadow: 0px 5px 0px #E6C229 !important; font-weight: bold !important;
        transition: all 0.1s ease; border: 2px solid #C0A100 !important; text-shadow: 0 1px 0 #fff8;
    }
    .stButton>button:active { transform: translateY(3px); }
    div[data-testid="stBlock"] button:contains("지우기") {
        background-color: #FF9233 !important; color: #fff !important;
        box-shadow: 0px 5px 0px #DD6B11 !important; border: 2px solid #B96009 !important;
    }
    div[data-testid="stBlock"] button:contains("처음 화면으로") {
        background-color: #A5A5A5 !important; color: #fff !important;
        box-shadow: 0px 5px 0px #7A7A7A !important; border: 2px solid #636363 !important;
        font-size: 20px !important; height: 45px !important;
    }
    .streamlit-keypad-row { display: flex !important; flex-direction: row !important; justify-content: center !important; gap: 10px !important; margin-bottom: 10px; width: 100%; }
    @media (max-width: 768px) {
        .quiz-box, .reveal-card, .animal-name, .dashboard, .hint-box { font-size: 5vw !important; }
        .stButton>button { font-size: 5vw !important; height: 48px !important; }
        .animal-icon { font-size: 12vw; }
        .streamlit-keypad-row button { min-width: 27vw !important; font-size: 6vw !important; }
    }
    </style>
""", unsafe_allow_html=True)

# 2. 전역 세션 상태 초기화 (골드 및 도감 공유)
if 'page' not in st.session_state:
    st.session_state.page = "menu" # 현재 보고 있는 페이지 (menu / multiply / divide)
if 'gold' not in st.session_state:
    st.session_state.score, st.session_state.gold = 0, 0
    st.session_state.collection = []
    st.session_state.gacha_step = "idle"
    st.session_state.revealed_animal = None

# 공통 동물 데이터 (이전 요청하셨던 곤충/해양 생물 데이터 적용)
animals_data = {
    "일반": ["🦋 나비", "🐝 꿀벌", "🐞 무당벌레", "🐌 달팽i", "🐜 개미"],
    "희귀": ["🐸 궁금한 개구리", "🦑 오징어징어", "🦐 안녕하새우", "🐡 뾰족 복어", "🐢 조용한 거북이"],
    "전설": ["🐳 물 뿜는 거대 고래", "🌈🐠 레인보우 열대어", "🦈 아기상어", "💎🐟 보석 물고기", "Rex 🦖 티라노"]
}

# 공통 가챠 시스템 함수
def start_gacha():
    if st.session_state.gold >= 100:
        st.session_state.gold -= 100
        st.session_state.gacha_step = "shaking"
        rand = random.random()
        if rand < 0.7: tier = "일반"
        elif rand < 0.95: tier = "희귀"
        else: tier = "전설"
        st.session_state.revealed_animal = (tier, random.choice(animals_data[tier]))
        if st.session_state.revealed_animal[1] not in st.session_state.collection:
            st.session_state.collection.append(st.session_state.revealed_animal[1])
    else:
        st.error("골드가 부족해요! 문제를 더 풀어서 골드를 모으세요!")

# 문제 출제 함수들
def make_multiply_question():
    st.session_state.m_f1 = random.randint(2, 9)
    st.session_state.m_f2 = random.randint(2, 9)
    st.session_state.m_target = st.session_state.m_f1 * st.session_state.m_f2
    st.session_state.inputs = []
    st.session_state.status = "playing"
    st.session_state.is_answered = False

def make_divide_question():
    divisor = random.randint(2, 9)
    answer = random.randint(2, 9)
    st.session_state.d_divisor = divisor
    st.session_state.d_correct = answer
    st.session_state.d_dividend = divisor * answer
    st.session_state.inputs = []
    st.session_state.status = "playing"
    st.session_state.is_answered = False


# =========================================================================
# 🏠 [화면 1] 메인 메뉴 화면
# =========================================================================
if st.session_state.page == "menu":
    st.markdown("<div class='menu-title'>🥚 신비의 알 수학 대모험 🎮</div>", unsafe_allow_html=True)
    st.write("오늘 도전할 수학 퀘스트를 선택해 주세요!")
    
    col1, col2 = st.columns(2, gap="medium")
    
    with col1:
        st.subheader("⚔️ 역곱셈 퀘스트")
        st.write("결과를 보고 원래 곱했던 두 숫자를 찾아라!")
        if st.button("역곱셈 시작하기 ➡️", key="go_mult"):
            make_multiply_question()
            st.session_state.page = "multiply"
            st.rerun()
            
    with col2:
        st.subheader("🏹 나눗셈 퀘스트")
        st.write("나눗셈의 비밀을 풀고 구구단 힌트를 얻자!")
        if st.button("나눗셈 시작하기 ➡️", key="go_div"):
            make_divide_question()
            st.session_state.page = "divide"
            st.rerun()

    st.write("---")
    if st.session_state.collection:
        st.info(f"현재 보유 중인 도감: {' | '.join(st.session_state.collection)}")
    else:
        st.text("아직 수집한 동물이 없어요. 문제를 풀어 골드를 모아보세요!")


# =========================================================================
# ⚔️ [화면 2] 역곱셈 게임 화면
# =========================================================================
elif st.session_state.page == "multiply":
    st.title("⚔️ 역곱셈 퀘스트 모드")
    if st.button("⬅️ 처음 화면으로", key="back_to_menu_m"):
        st.session_state.page = "menu"
        st.rerun()
        
    st.markdown(f"<div class='dashboard'><span>⭐ 점수: {st.session_state.score}</span><span>💰 골드: {st.session_state.gold} G</span></div>", unsafe_allow_html=True)

    # 알 부화 연출 구역
    if st.session_state.gacha_step == "shaking":
        st.markdown("<span class='egg-shaking'>🥚</span>", unsafe_allow_html=True)
        time.sleep(2.0)
        st.session_state.gacha_step = "revealed"; st.rerun()
    elif st.session_state.gacha_step == "revealed":
        tier, animal = st.session_state.revealed_animal
        st.markdown(f"<div class='reveal-card'><div class='animal-icon'>{animal.split()[0]}</div><div class='animal-name'>[{tier}] {animal.split()[-1]}</div></div>", unsafe_allow_html=True)
        if st.button("도감에 저장하기", use_container_width=True):
            st.session_state.gacha_step = "idle"; st.rerun()

    # 기본 게임 구역
    if st.session_state.gacha_step == "idle":
        with st.expander("🥚 [알뽑기 상점]", expanded=False):
            st.button("🔮 알뽑기 (100G)", on_click=start_gacha, key="btn_g_m")
        
        # 입력값 시각화
        p1 = str(st.session_state.inputs[0]) if len(st.session_state.inputs) >= 1 else " ? "
        p2 = str(st.session_state.inputs[1]) if len(st.session_state.inputs) >= 2 else " ? "
        st.markdown(f"<div class='quiz-box'>{st.session_state.m_target} = [ {p1} ] × [ {p2} ]</div>", unsafe_allow_html=True)

        # 키패드 콜백 처리용 함수 정의
        def p_key_m(v):
            if st.session_state.is_answered or len(st.session_state.inputs) >= 2: return
            st.session_state.inputs.append(v)
            if len(st.session_state.inputs) == 2: st.session_state.is_answered = True

        # 키패드 그리기
        if st.session_state.status == "playing":
            for row in [[1,2,3],[4,5,6],[7,8,9]]:
                cols = st.columns(3, gap="small")
                for i, val in enumerate(row):
                    cols[i].button(str(val), key=f"m_{val}", use_container_width=True, on_click=p_key_m, args=(val,))
            st.markdown('<div class="streamlit-keypad-row">', unsafe_allow_html=True)
            if st.button("⌫ 지우기", key="m_del"): 
                if len(st.session_state.inputs)>0: st.session_state.inputs.pop()
            st.markdown("</div>", unsafe_allow_html=True)

        # 정답 검증
        if len(st.session_state.inputs) == 2 and st.session_state.is_answered:
            time.sleep(0.4)
            if st.session_state.inputs[0] * st.session_state.inputs[1] == st.session_state.m_target:
                g = random.randint(8, 13)
                st.success(f"✅ 정답입니다! (+{g}G)")
                st.session_state.score += 1; st.session_state.gold += g
                time.sleep(1.5); make_multiply_question(); st.rerun()
            else:
                st.error("❌ 틀렸습니다! 다시 생각해 보세요.")
                time.sleep(1.5)
                st.session_state.inputs = []; st.session_state.is_answered = False; st.rerun()


# =========================================================================
# 🏹 [화면 3] 나눗셈 게임 화면 (구구단 힌트 기능 포함)
# =========================================================================
elif st.session_state.page == "divide":
    st.title("🏹 나눗셈 퀘스트 모드")
    if st.button("⬅️ 처음 화면으로", key="back_to_menu_d"):
        st.session_state.page = "menu"
        st.rerun()

    st.markdown(f"<div class='dashboard'><span>⭐ 점수: {st.session_state.score}</span><span>💰 골드: {st.session_state.gold} G</span></div>", unsafe_allow_html=True)

    # 알 부화 연출 구역
    if st.session_state.gacha_step == "shaking":
        st.markdown("<span class='egg-shaking'>🥚</span>", unsafe_allow_html=True)
        time.sleep(2.0)
        st.session_state.gacha_step = "revealed"; st.rerun()
    elif st.session_state.gacha_step == "revealed":
        tier, animal = st.session_state.revealed_animal
        st.markdown(f"<div class='reveal-card'><div class='animal-icon'>{animal.split()[0]}</div><div class='animal-name'>[{tier}] {animal.split()[-1]}</div></div>", unsafe_allow_html=True)
        if st.button("도감에 저장하기", use_container_width=True):
            st.session_state.gacha_step = "idle"; st.rerun()

    # 기본 게임 구역
    if st.session_state.gacha_step == "idle":
        with st.expander("🥚 [알뽑기 상점]", expanded=False):
            st.button("🔮 알뽑기 (100G)", on_click=start_gacha, key="btn_g_d")

        p_ans = str(st.session_state.inputs[0]) if len(st.session_state.inputs) >= 1 else " ? "
        st.markdown(f"<div class='quiz-box'>{st.session_state.d_dividend} ÷ {st.session_state.d_divisor} = [ {p_ans} ]</div>", unsafe_allow_html=True)

        # 💡 오답일 때만 작동하는 구구단 연계 힌트 박스
        if st.session_state.status == "hint":
            st.markdown(f"<div class='hint-box'>💡 구구단 힌트: {st.session_state.d_divisor} × {st.session_state.d_correct} = {st.session_state.d_dividend}</div>", unsafe_allow_html=True)
            st.error("❌ 틀렸습니다! 곱셈 관계를 생각하며 다시 풀어보세요.")
            time.sleep(2.8)
            st.session_state.inputs = []; st.session_state.status = "playing"; st.session_state.is_answered = False; st.rerun()

        # 키패드 콜백 처리용 함수 정의
        def p_key_d(v):
            if st.session_state.is_answered: return
            st.session_state.inputs.append(v)
            st.session_state.is_answered = True

        # 키패드 그리기
        if st.session_state.status == "playing":
            for row in [[1,2,3],[4,5,6],[7,8,9]]:
                cols = st.columns(3, gap="small")
                for i, val in enumerate(row):
                    cols[i].button(str(val), key=f"d_{val}", use_container_width=True, on_click=p_key_d, args=(val,))
            st.markdown('<div class="streamlit-keypad-row">', unsafe_allow_html=True)
            if st.button("⌫ 지우기", key="d_del"): 
                if len(st.session_state.inputs)>0: st.session_state.inputs.pop()
            st.markdown("</div>", unsafe_allow_html=True)

        # 정답 검증 (1개 누르면 즉시 작동)
        if len(st.session_state.inputs) == 1 and st.session_state.is_answered and st.session_state.status == "playing":
            time.sleep(0.4)
            if st.session_state.inputs[0] == st.session_state.d_correct:
                g = random.randint(8, 13)
                st.success(f"✅ 정답입니다! (+{g}G)")
                st.session_state.score += 1; st.session_state.gold += g
                time.sleep(1.5); make_divide_question(); st.rerun()
            else:
                st.session_state.status = "hint"
                st.rerun()
