import streamlit as st
from openai import OpenAI

# 페이지 설정 (웹 브라우저 탭 이름 및 아이콘)
st.set_page_config(page_title="트래블 가이드 AI", page_icon="✈️")

# 제목 및 앱 설명
st.title("✈️ AI 여행 가이드")
st.write(
    "어디로 떠나고 싶으신가요? 목적지 추천부터 맛집, 현지 꿀팁까지 "
    "당신만의 맞춤형 여행 계획을 도와드립니다."
)

# API 키 입력 (비밀번호 형식)
openai_api_key = st.text_input("OpenAI API 키를 입력하세요", type="password")

if not openai_api_key:
    st.info("여행 상담을 시작하려면 OpenAI API 키를 입력해 주세요.", icon="🗝️")
else:
    client = OpenAI(api_key=openai_api_key)

    # 대화 기록 유지
    if "messages" not in st.session_state:
        # 여행 전문가라는 '페르소나'를 부여하는 시스템 메시지를 처음에 삽입합니다.
        st.session_state.messages = [
            {
                "role": "system", 
                "content": "당신은 열정적이고 해박한 지식을 가진 전문 여행 가이드입니다. "
                           "사용자가 여행지를 물어보면 해당 지역의 날씨, 맛집, 가볼 만한 곳, "
                           "그리고 현지 에티켓을 포함하여 친절하게 답변해 주세요."
            }
        ]

    # 기존 메시지 표시 (시스템 메시지는 화면에 보이지 않게 처리)
    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # 채팅 입력창
    if prompt := st.chat_input("예: 3박 4일 일본 오사카 여행 일정 짜줘!"):

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

# 사이드바에 여행 팁 추가 (선택 사항)
with st.sidebar:
    st.header("🧳 여행 준비 팁")
    st.markdown("""
    - **환율 확인:** 출발 전 환전은 필수!
    - **날씨 체크:** 목적지의 계절 정보를 확인하세요.
    - **예약 확인:** 숙소와 항공권 바우처를 챙기세요.
    """)
