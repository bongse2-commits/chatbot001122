import streamlit as st
from openai import OpenAI

# 페이지 설정
st.set_page_config(page_title="운명연애 사주 AI", page_icon="🔮")

# 제목 및 앱 설명
st.title("🔮 AI 연애 사주 상담소")
st.write(
    "당신의 타고난 연애운과 인연의 실타래를 풀어드립니다. "
    "**생년월일시**와 궁금한 내용을 말씀해 주세요. (예: 95년 5월 10일생 여자, 언제쯤 연인이 생길까요?)"
)

# API 키 입력
openai_api_key = st.text_input("OpenAI API 키를 입력하세요", type="password")

if not openai_api_key:
    st.info("상담을 시작하려면 OpenAI API 키를 입력해 주세요.", icon="🗝️")
else:
    client = OpenAI(api_key=openai_api_key)

    # 대화 기록 유지 및 시스템 페르소나 설정
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "system", 
                "content": "당신은 신비롭고 통찰력 있는 명리학자이자 연애 상담가입니다. "
                           "사용자의 생년월일을 바탕으로 사주팔자의 오행 원리를 활용해 연애운을 풀이해 줍니다. "
                           "말투는 부드럽고 따뜻하며, '운명의 기운이 느껴지네요', '사주에 도화살의 기운이 있군요' 등 "
                           "명리학적인 표현을 섞어서 신뢰감 있게 답변해 주세요. "
                           "마지막에는 항상 따뜻한 응원의 한마디를 덧붙여 주세요."
            }
        ]

    # 채팅 메시지 표시 (시스템 메시지 제외)
    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # 채팅 입력창
    if prompt := st.chat_input("당신의 사주 정보와 고민을 남겨주세요..."):

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
            # 연애 사주 느낌을 주기 위해 보라색 배경 등의 스타일을 활용할 수 있습니다.
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})

# 사이드바에 연애운 상승 팁 추가
with st.sidebar:
    st.header("✨ 연애운 상승 가이드")
    st.markdown("""
    - **행운의 색상:** 오늘 당신의 기운을 돋워줄 색상을 물어보세요.
    - **인연의 방향:** 어느 방향에서 귀인이 나타날지 확인해 보세요.
    - **마음가짐:** 사주는 흐름일 뿐, 가장 중요한 것은 당신의 용기입니다.
    """)
    st.divider()
    st.caption("※ 본 상담은 인공지능이 풀이하는 재미용 사주입니다.")
