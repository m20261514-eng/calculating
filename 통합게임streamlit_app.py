import streamlit as st

# 페이지 기본 설정
st.set_page_config(page_title="수학 게임 대모험 메인", page_icon="🎲", layout="centered")

# CSS 스타일링 (데스크탑 & 모바일 반응형)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');
    
    /* 전체 배경 그라데이션 */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #FFFFFF 0%, #FFD93D 100%);
    }
    
    [data-testid="stMain"] {
        background: linear-gradient(135deg, #FFFFFF 0%, #FFD93D 100%);
    }
    
    /* 크로마틱 어버레이션 애니메이션 (마젠타와 시안 분리) */
    @keyframes chromatic-aberration {
        0%, 100% {
            text-shadow: 
                -2px 0 #FF00FF,
                2px 0 #00FFFF,
                0 0 30px rgba(0, 0, 0, 0.5);
        }
        50% {
            text-shadow: 
                -3px 0 #FF00FF,
                3px 0 #00FFFF,
                0 0 30px rgba(0, 0, 0, 0.5);
        }
    }
    
    /* 부드러운 호흡 애니메이션 (숨 쉬듯 위아래 움직임) */
    @keyframes breathe {
        0%, 100% {
            transform: translateY(0px);
        }
        50% {
            transform: translateY(-15px);
        }
    }
    
    /* 1. 데스크탑 기본 스타일 */
    .main-title {
        font-family: 'Press Start 2P', cursive;
        font-size: 3.5rem;
        font-weight: 700;
        color: #000000;
        text-align: center;
        margin-bottom: 35px;
        margin-top: 15px;
        letter-spacing: 2px;
        white-space: nowrap;
        animation: chromatic-aberration 2s ease-in-out infinite, breathe 3s ease-in-out infinite;
        display: inline-block;
        width: 100%;
        image-rendering: pixelated;
        image-rendering: crisp-edges;
    }
    
    .guide-text {
        color: #156580 !important;
        font-weight: bold;
        text-align: center;
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
            font-size: 1.8rem !important;
            white-space: nowrap !important;
            word-break: keep-all;
            margin-bottom: 20px !important;
            letter-spacing: 1px;
        }
        .game-btn {
            width: 95% !important;
            font-size: 1.3rem !important;
            padding: 15px 0 !important;
            margin: 12px auto !important;
        }
        
        /* Streamlit 컬럼이 모바일에서 세로로 쌓이는 현상 방지 (3x3 배열 강제 유지) */
        div[data-testid="column"] {
            min-width: 0 !important;
        }
        div[data-testid="stHorizontalBlock"] {
            flex-wrap: nowrap !important;
            gap: 5px !important;
        }
    }
    </style>
""", unsafe_allow_html=True)

# 메인 타이틀
st.markdown("<div class='main-title'>🥚수학 게임 대모험🎲</div>", unsafe_allow_html=True)
st.markdown("<div class='guide-text'>원하는 게임을 선택하세요!</div>", unsafe_allow_html=True)

# 역곱셈 게임 버튼
st.markdown(
    '<a class="game-btn" href="https://calculating-fvke79kvlkq4td4zybopf5.streamlit.app/" target="_blank">⚔️ 역곱셈 게임 바로가기</a>',
    unsafe_allow_html=True
)

# 나눗셈 게임 버튼
st.markdown(
    '<a class="game-btn" href="https://calculating-ey8jg4rdgte9d6knxsvrdw.streamlit.app/" target="_blank">🏹 나눗셈 게임 바로가기</a>',
    unsafe_allow_html=True
)

st.info("새 창(탭)에서 열립니다.")
