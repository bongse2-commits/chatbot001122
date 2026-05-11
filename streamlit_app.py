import streamlit as st
from openai import OpenAI
import datetime

# 페이지 설정
st.set_page_config(page_title="오늘의 운세 가이드", page_icon="🌟")

# 제목 및 앱 설명
st.title("🌟 AI 마음 운세 상담소")
st.write(
    f"오늘은 **{datetime.date.today().strftime('%Y년 %m월 %d일')}**입니다. "
    "오늘 당신을 감싸고 있는 기운은 어떤지, 어떤 마음가짐이 행운을 불러올지 확인해 보세요."
)

# API 키 입력
openai_api_key = st.text_input("OpenAI API 키를 입력하세요", type="password")

if not openai_api_key:
    st.info("오늘의 운세를 확인하려면 OpenAI API 키를 입력해 주세요.", icon="🗝️")
else:
    client = OpenAI(api_key=openai_api_key)

    # 대화 기록 유지 및 시스템 페르소나 설정
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "system", 
                "content": "당신은 긍정적인 에너지를 전달하는 '운세 및 마음 가이드'입니다. "
                           "사용자가 이름이나 생년월일, 혹은 현재의 기분을 말하면 "
                           "오늘의 전체적인 운의 흐름, 행운의 아이템(색상, 음식 등), "
                           "그리고 마음을 다스리는 조언을 다정하게 들려주세요. "
                           "과학적 근거보다는 심리적인 위안과 긍정적인 동기부여에 집중하세요."
            }
        ]

    # 채팅 메시지 표시 (시스템 메시지 제외)
    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # 채팅 입력창
    if prompt := st.chat_input("이름이나 현재 기분, 혹은 궁금한 점을 적어주세요!"):

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

# 사이드바에 행운 요소 추가
with st.sidebar:
    st.header("🍀 오늘의 행운 포인트")
    st.markdown("""
    - **오늘의 색상:** 🎨 AI에게 물어보세요!
    - **행운의 장소:** 🌳 공원, 카페, 혹은 서재?
    - **오늘의 명언:** *"당신이 걷는 모든 길이 꽃길이 될 거예요."*
    """)
    st.divider()
    st.caption("※ 본 서비스는 긍정적인 하루를 위한 심리 상담용이며, 결과에 너무 의존하기보다 가벼운 마음으로 즐겨주세요.")
