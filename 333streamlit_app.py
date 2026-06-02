import streamlit as st

# 페이지 기본 설정
st.set_page_config(page_title="수학 게임 대모험 메인", page_icon="🎲", layout="centered")

# CSS 스타일링 (데스크탑 & 모바일 반응형)
st.markdown("""
    <style>
    /* 1. 데스크탑 기본 스타일 */
    .main-title {
        font-size: 3rem;
        font-weight: bold;
        color: #156580;
        text-align: center;
        margin-bottom: 35px;
        margin-top: 15px;
        letter-spacing: 2px;
        white-space: nowrap; /* 데스크탑에서는 한 줄 유지 */
    }
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
    
    /* 숫자 패드 버튼 기본 높이/폰트 지정 */
    div[data-testid="stButton"] button {
        height: 60px;
        font-size: 1.5rem;
        font-weight: bold;
        border-radius: 15px;
    }

    /* 2. 모바일 대응 (화면 너비 600px 이하일 때 적용) */
    @media (max-width: 600px) {
        .main-title {
            font-size: 1.6rem !important; /* 폰트 크기 축소 */
            white-space: normal !important; /* 자동 줄바꿈 허용 */
            word-break: keep-all; /* 단어 단위로 줄바꿈 (가독성 향상) */
            margin-bottom: 20px !important;
        }
        .game-btn {
            width: 95% !important; /* 화면을 꽉 채우도록 넓이 확장 */
            font-size: 1.3rem !important; /* 폰트 크기 축소 */
            padding: 15px 0 !important; /* 위아래 여백 축소 */
            margin: 12px auto !important;
        }
        
        /* Streamlit 컬럼이 모바일에서 세로로 쌓이는 현상 방지 (3x3 배열 강제 유지) */
        div[data-testid="column"] {
            min-width: 0 !important; /* 최소 넓이 해제 */
        }
        div[data-testid="stHorizontalBlock"] {
            flex-wrap: nowrap !important; /* 컬럼들이 가로로 유지되도록 고정 */
            gap: 5px !important; /* 버튼 사이 간격 좁히기 */
        }
    }
    </style>
""", unsafe_allow_html=True)

# 메인 타이틀
st.markdown("<div class='main-title' style='white-space: nowrap;'>🥚신비의 수학 대모험 선택 화면🎲</div>", unsafe_allow_html=True)
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

st.divider() # 시각적 분리를 위한 선

# 3x3 숫자 버튼 배열 생성
st.write("🔢 **숫자 입력 패드**")

# 1부터 9까지 3x3 구조로 반복하여 버튼 생성
for i in range(0, 9, 3):
    cols = st.columns(3) # 3개의 컬럼 생성
    for j in range(3):
        num = i + j + 1
        with cols[j]:
            # use_container_width=True로 버튼이 컬럼 너비에 꽉 차게 설정
            if st.button(str(num), use_container_width=True):
                # 버튼을 클릭했을 때 동작할 코드를 아래에 작성하세요.
                st.toast(f"{num}번 버튼을 클릭했습니다!")
