import streamlit as st
from openai import OpenAI
import datetime

# 페이지 설정
st.set_page_config(page_title="따뜻한 운세 가이드", page_icon="🌟", layout="centered")

# --- 커스텀 CSS 디자인 스타일 정의 (오타 수정됨) ---
st.markdown("""
<style>
    /* 전체 앱 배경색 */
    .stApp {
        background-color: #fdfaf5;
    }

    /* 제목 스타일 */
    .main-title {
        font-family: 'sans-serif';
        color: #4a3e2a;
        font-size: 2.5rem;
        text-align: center;
        font-weight: bold;
        margin-bottom: 0px;
    }

    /* 서브 제목 스타일 */
    .sub-title {
        color: #6e5c46;
        text-align: center;
        font-size: 1.1rem;
        margin-bottom: 20px;
    }

    /* 안내 카드 디자인 */
    .info-card {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        color: #5d5d5d;
        margin-bottom: 25px;
        border-left: 5px solid #d4a373;
    }
</style>
""", unsafe_allow_html=True) # <- 이 부분을 html로 수정했습니다.

# --- 메인 화면 UI 구성 ---

st.markdown('<h1 class="main-title">🌟 마음 운세 상담소</h1>', unsafe_allow_html=True)
st.markdown(f'<p class="sub-title">우주의 기운이 당신을 향하는 날, **{datetime.date.today().strftime("%Y년 %m월 %d일")}**</p>', unsafe_allow_html=True)

st.markdown("""
<div class="info-card">
    안녕하세요! 당신의 마음과 우주의 흐름을 읽어주는 'AI 운세 가이드'입니다. <br>
    생년월일이나 이름, 혹은 지금 느끼는 기분과 고민을 편안하게 말씀해 주세요.
</div>
""", unsafe_allow_html=True)

# API 키 입력
openai_api_key = st.text_input("상담소의 비밀키(API 키)를 입력해 주세요", type="password")

if not openai_api_key:
    st.info("오늘의 운세와 조언을 받으려면 OpenAI API 키를 입력해 주세요.", icon="🗝️")
else:
    client = OpenAI(api_key=openai_api_key)

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "system", 
                "content": "당신은 따뜻하고 공감 능력이 뛰어난 '운세 및 마음 가이드'입니다. 긍정적인 에너지를 전달하세요."
            }
        ]

    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    if prompt := st.chat_input("오늘 당신의 하루는 어떠신가요?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
            stream=True,
        )

        with st.chat_message("assistant"):
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})

# 사이드바
with st.sidebar:
    st.markdown('<h2 style="color:#4a3e2a; text-align:center;">🍀 행운 포인트</h2>', unsafe_allow_html=True)
    st.markdown("""
    <div style="background-color: white; padding: 15px; border-radius: 10px;">
        <b>🎨 행운의 색상:</b> AI에게 질문하기<br>
        <b>🌳 행운의 장소:</b> 햇살 가득한 창가<br>
    </div>
    """, unsafe_allow_html=True)
