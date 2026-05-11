import streamlit as st
from openai import OpenAI
import datetime

# 페이지 설정 (가장 상단에 위치)
st.set_page_config(page_title="따뜻한 운세 가이드", page_icon="🌟", layout="centered")

# --- 커스텀 CSS 디자인 스타일 정의 ---
# st.markdown을 사용해 앱 전체에 세련된 디자인을 입힙니다.
st.markdown("""
<style>
    /* 전체 앱 배경색 */
    .stApp {
        background-color: #fdfaf5; /* 따뜻하고 포근한 아이보리 톤 */
    }

    /* 사이드바 스타일 */
    .css-163utfm, .ekf09p01 {
        background-color: #f6efe0 !important; /* 약간 더 짙은 베이지 톤 */
    }

    /* 제목 스타일 */
    .main-title {
        font-family: 'Do Hyeon', sans-serif;
        color: #4a3e2a; /* 짙은 브라운 톤 */
        font-size: 3rem;
        text-align: center;
        margin-bottom: 0px;
        padding-bottom: 0px;
    }

    /* 서브 제목 (날짜) 스타일 */
    .sub-title {
        font-family: 'Gowun Dodum', sans-serif;
        color: #6e5c46;
        text-align: center;
        font-size: 1.2rem;
        margin-top: 0px;
        margin-bottom: 20px;
    }

    /* 카드 형태의 컨테이너 디자인 (가이드 텍스트용) */
    .info-card {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        color: #5d5d5d;
        margin-bottom: 25px;
        border-left: 5px solid #d4a373; /* 포인트 컬러 */
    }

    /* 채팅 메시지 디자인 커스터마이징 */
    .stChatMessage {
        border-radius: 15px !important;
        padding: 15px !important;
        margin-bottom: 10px !important;
    }
    
    /* 사용자 메시지 */
    .stChatMessage[data-testid="stChatMessageUser"] {
        background-color: #e6f3ff !important; /* 연한 파란색 */
    }
    
    /* 어시스턴트(봇) 메시지 */
    .stChatMessage[data-testid="stChatMessageAssistant"] {
        background-color: white !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }

    /* API 입력 필드 라벨 스타일 */
    .css-1fcdmub {
        color: #4a3e2a !important;
        font-weight: bold;
    }

</style>
""", unsafe_allow_stdio=True)

# 구글 폰트 로드 (optional)
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Do+Hyeon&family=Gowun+Dodum&display=swap" rel="stylesheet">
""", unsafe_allow_stdio=True)

# --- 메인 화면 UI 구성 ---

# 제목과 오늘 날짜
st.markdown('<h1 class="main-title">🌟 마음 운세 상담소</h1>', unsafe_allow_stdio=True)
st.markdown(f'<p class="sub-title">우주의 기운이 당신을 향하는 날, **{datetime.date.today().strftime("%Y년 %m월 %d일")}**</p>', unsafe_allow_stdio=True)

# 포근한 디자인의 안내 카드
st.markdown("""
<div class="info-card">
    안녕하세요! 당신의 마음과 우주의 흐름을 읽어주는 'AI 운세 가이드'입니다. <br>
    생년월일이나 이름, 혹은 지금 느끼는 기분과 고민을 다정하게 말씀해 주세요. <br>
    당신의 하루가 긍정적인 에너지로 가득하도록 따뜻한 조언과 행운의 팁을 전해드립니다.
</div>
""", unsafe_allow_stdio=True)

# API 키 입력 (스타일은 CSS로 조정)
openai_api_key = st.text_input("상담소의 비밀키(API 키)를 입력해 주세요", type="password")

if not openai_api_key:
    # 예쁜 경고 메시지 스타일
    st.info("오늘의 운세와 따뜻한 조언을 받으려면 비밀키를 입력해 주세요.", icon="🗝️")
else:
    client = OpenAI(api_key=openai_api_key)

    # 대화 기록 유지 및 시스템 페르소나 설정 (내용 유지)
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "system", 
                "content": "당신은 따뜻하고 공감 능력이 뛰어난 '마음 및 운세 가이드'입니다. "
                           "사용자의 고민, 이름, 생년월일 등을 들으면 "
                           "오늘의 전체적인 기운의 흐름, 마음가짐에 대한 조언, "
                           "그리고 소소한 행운의 요소(색상, 장소 등)를 다정하게 이야기해 주세요. "
                           "격려와 위안을 주는 것이 가장 중요한 임무입니다."
            }
        ]

    # 채팅 메시지 표시 (시스템 메시지 제외)
    # 자동으로 스타일이 적용된 chat_message를 사용합니다.
    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # 채팅 입력창
    if prompt := st.chat_input("당신의 마음 상태나 궁금한 점을 편안하게 적어주세요..."):

        # 사용자 입력 저장 및 표시
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # AI 답변 생성
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )

        # 실시간 답변 출력 및 저장
        with st.chat_message("assistant"):
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})

# --- 사이드바 UI 구성 (디자인 추가) ---
with st.sidebar:
    st.markdown('<h2 style="color:#4a3e2a; text-align:center;">🍀 오늘의 행운</h2>', unsafe_allow_stdio=True)
    st.markdown("""
    <div style="background-color: white; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
        <b>🎨 행운의 색상:</b><br>
        <span style="color:#6e5c46;">가이드에게 물어보세요!</span><br><br>
        <b>🌳 행운의 장소:</b><br>
        <span style="color:#6e5c46;">따뜻한 햇살이 드는 곳</span><br><br>
        <b>✨ 오늘의 명언:</b><br>
        <i style="color:#888;">"당신은 존재하는 자체로 충분히 빛납니다."</i>
    </div>
    """, unsafe_allow_stdio=True)
    st.divider()
    st.caption("※ 이 상담은 재미와 긍정적인 에너지를 위한 것이며, 전문적인 사주 풀이가 아닙니다.")
