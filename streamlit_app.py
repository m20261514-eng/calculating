import streamlit as st
import random
import time

# 1. 페이지 기본 설정
st.set_page_config(page_title="재미있는 역곱셈 구구단", page_icon="🎒", layout="centered")

# 어떤 기기(모바일/컴퓨터)에서든 가로로 길고 예쁜 계산기 격자를 유지하는 CSS
st.markdown("""
    <style>
    .stApp {
        background-color: #FFFDF0;
    }
    /* 문제 창 스타일 */
    .quiz-box {
        background-color: #FFFFFF;
        padding: 25px;
        border-radius: 25px;
        text-align: center;
        font-size: clamp(28px, 5vw, 42px); /* 화면 크기에 맞게 글자 크기 조절 */
        font-weight: bold;
        color: #4A4A4A;
        border: 5px solid #FFD93D;
        box-shadow: 0px 8px 0px #FFD93D;
        margin-bottom: 20px;
    }
    /* 빨간색 힌트 숫자 스타일 */
    .hint-num {
        color: #FF4B4B !important;
        font-weight: bold;
    }
    /* 계산기 버튼 스타일 (가로로 길고 시원한 형태) */
    .stButton>button {
        font-size: clamp(20px, 4vw, 28px) !important;
        border-radius: 15px !important;
        background-color: #FFD93D !important;
        color: #4A4A4A !important;
        height: 60px !important; /* 세로는 줄이고 가로는 꽉 차게 */
        width: 100% !important;
        border: none !important;
        box-shadow: 0px 5px 0px #E6C229 !important;
        font-weight: bold !important;
        transition: all 0.1s ease;
        margin-bottom: 10px;
    }
    .stButton>button:active {
        box-shadow: 0px 1px 0px #E6C229 !important;
        transform: translateY(4px);
    }
    /* 전광판 대시보드 스타일 */
    .dashboard-box {
        background-color: #E3FAFC;
        padding: 12px 20px;
        border-radius: 15px;
        border: 2px solid #10B981;
        font-size: clamp(16px, 3.5vw, 22px);
        font-weight: bold;
        color: #099268;
        display: flex;
        justify-content: space-between;
        margin-bottom: 15px;
    }
    /* 내 도감 스타일 */
    .collection-box {
        background-color: #F8F9FA;
        padding: 10px;
        border-radius: 10px;
        font-size: 15px;
        color: #495057;
        border: 1px dashed #CED4DA;
    }
    </style>
""", unsafe_allow_html=True)

# 2. 세션 상태(Session State) 초기화
if 'gold' not in st.session_state:
    st.session_state.score = 0
    st.session_state.total = 0
    st.session_state.gold = 0          
    st.session_state.last_earned = 0   
    st.session_state.inputs = []
    st.session_state.status = "playing" # playing, hint, success, fail
    st.session_state.collection = []   
    st.session_state.egg_result = ""   
    
    # 첫 문제 생성
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

# 3. 타이틀
st.title("🎒 역곱셈 구구단 계산기 🎮")

# 4. 대시보드 (점수 & 골드)
st.markdown(f"""
<div class='dashboard-box'>
    <span>⭐ 맞춘 문제: {st.session_state.score} / {st.session_state.total}</span>
    <span>💰 내 골드: {st.session_state.gold} G</span>
</div>
""", unsafe_allow_html=True)

# 5. 신비의 알뽑기 상점
with st.expander("🥚 ✨ [신비의 알뽑기 상점 열기] ✨", expanded=False):
    st.subheader("신비의 알을 깨워보세요!")
    if st.button("🔮 신비의 알뽑기 시작! (100 G)", use_container_width=True):
        if st.session_state.gold >= 100:
            st.session_state.gold -= 100
            animals = [
                "🍼 아기 오리", "🐥 아기 병아리", "🐹 아기 햄스터", "🐰 하얀 토끼", 
                "🦊 불꽃 여우", "🐼 대나무 판다", "🐱 우주 고양이", "🐶 날개 강아지", 
                "🦄 무지개 유니콘", "🐲 황금 아기용", "🦁 꼬마 사자왕" 
            ]
            picked = random.choice(animals)
            if picked not in st.session_state.collection:
                st.session_state.collection.append(picked)
            st.session_state.egg_result = f"🎉 대박! 알에서 [ {picked} ]이(가) 태어났어요! 🎉"
            st.balloons()
        else:
            st.session_state.egg_result = "❌ 골드가 부족해요! 문제를 더 풀어서 골드를 모아오세요!"
        st.rerun()
        
    if st.session_state.egg_result:
        if "🎉" in st.session_state.egg_result:
            st.success(st.session_state.egg_result)
        else:
            st.error(st.session_state.egg_result)
            
    st.write("---")
    st.write("🎒 **내가 모은 동물 도감**")
    if st.session_state.collection:
        st.markdown(f"<div class='collection-box'>{' | '.join(st.session_state.collection)}</div>", unsafe_allow_html=True)
    else:
        st.caption("아직 모은 동물이 없어요. 첫 번째 알을 뽑아보세요!")

st.write("---")

# 6. 문제 화면 표시
if st.session_state.status == "playing":
    p1 = str(st.session_state.inputs[0]) if len(st.session_state.inputs) > 0 else " ? "
    p2 = str(st.session_state.inputs[1]) if len(st.session_state.inputs) > 1 else " ? "
    st.markdown(f"<div class='quiz-box'>{st.session_state.target_product} = [ {p1} ] × [ {p2} ]</div>", unsafe_allow_html=True)

elif st.session_state.status == "hint":
    p1 = f"<span class='hint-num'>{st.session_state.factor1}</span>"
    p2 = str(st.session_state.inputs[1]) if len(st.session_state.inputs) > 1 else " ? "
    st.markdown(f"<div class='quiz-box'>{st.session_state.target_product} = [ {p1} ] × [ {p2} ]</div>", unsafe_allow_html=True)

else: # 정답/오답 연출 시 완전한 식 보여주기
    st.markdown(f"<div class='quiz-box'>{st.session_state.target_product} = [ {st.session_state.factor1} ] × [ {st.session_state.factor2} ]</div>", unsafe_allow_html=True)


# 7. 결과 연출 및 자동 다음 문제 전환 로직
if st.session_state.status in ["success", "fail"]:
    if st.session_state.status == "success":
        st.success(f"🎉 **정답이에요! 참 잘했어요!** (+{st.session_state.last_earned} 골드 획득! 💰)")
        st.balloons() # 맞추면 폭죽 팡팡!
    elif st.session_state.status == "fail":
        st.error(f"😢 **아쉬워요!** 정답은 {st.session_state.factor1} × {st.session_state.factor2} = {st.session_state.target_product} 이었어요.")
    
    # 2초 동안 결과를 보여준 뒤 자동으로 다음 문제 출제
    st.caption("⏳ 잠시 후 다음 문제가 자동으로 나옵니다...")
    time.sleep(2.2)
    next_question()
    st.rerun()


# 8. 계산기 숫자 버튼 레이아웃 (가로 그리드 적용)
if st.session_state.status in ["playing", "hint"]:
    if st.session_state.status == "playing":
        st.write("👇 **곱할 두 숫자를 순서대로 눌러주세요!**")
    else:
        st.warning(f"💡 **힌트 찬스!** 첫 번째 숫자는 빨간색 **{st.session_state.factor1}** 이에요. 곱해서 {st.session_state.target_product}가 되는 나머지 숫자를 누르세요!")
    
    # 4열 가로 격자 구성 (컴퓨터/모바일 모두 한 줄에 4개씩 균등 배치)
    col1, col2, col3, col4 = st.columns(4)
    buttons = [2, 3, 4, 5, 6, 7, 8, 9]
    
    for i, num in enumerate(buttons):
        current_col = [col1, col2, col3, col4][i % 4]
        with current_col:
            if st.button(str(num), key=f"btn_{num}", use_container_width=True):
                st.session_state.inputs.append(num)
                
                # [일반 모드 결과 판정]
                if st.session_state.status == "playing":
                    if len(st.session_state.inputs) == 2:
                        ans1, ans2 = st.session_state.inputs
                        if ans1 * ans2 == st.session_state.target_product:
                            st.session_state.status = "success"
                            st.session_state.score += 1
                            st.session_state.last_earned = random.randint(8, 13)
                            st.session_state.gold += st.session_state.last_earned
                        else:
                            st.session_state.status = "hint"
                            st.session_state.inputs = [st.session_state.factor1]
                        st.session_state.total += 1
                        st.rerun()
                
                # [힌트 모드 결과 판정]
                elif st.session_state.status == "hint":
                    if len(st.session_state.inputs) == 2:
                        ans1, ans2 = st.session_state.inputs
                        if ans1 * ans2 == st.session_state.target_product:
                            st.session_state.status = "success"
                            st.session_state.score += 1
                            st.session_state.last_earned = random.randint(8, 13)
                            st.session_state.gold += st.session_state.last_earned
                        else:
                            st.session_state.status = "fail"
                        st.session_state.total += 1
                        st.rerun()
