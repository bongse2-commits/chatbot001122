import streamlit as st
from openai import OpenAI

# 제목 및 앱 설명 설정
st.title("💬 챗봇")
st.write(
    "이 앱은 OpenAI의 GPT-3.5 모델을 사용하여 답변을 생성하는 간단한 챗봇입니다. "
    "앱을 사용하려면 [여기](https://platform.openai.com/account/api-keys)에서 발급받은 OpenAI API 키가 필요합니다. "
    "이 앱을 직접 만드는 방법이 궁금하시다면 [튜토리얼](https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps)을 확인해 보세요."
)

# `st.text_input`을 사용하여 사용자로부터 OpenAI API 키를 입력받습니다.
# 참고: API 키를 `./.streamlit/secrets.toml`에 저장하고 `st.secrets`로 불러오는 방식도 가능합니다.
openai_api_key = st.text_input("OpenAI API 키를 입력하세요", type="password")

if not openai_api_key:
    st.info("계속하려면 OpenAI API 키를 입력해 주세요.", icon="🗝️")
else:
    # OpenAI 클라이언트를 생성합니다.
    client = OpenAI(api_key=openai_api_key)

    # 대화 기록을 저장하기 위한 세션 상태(session state) 변수를 생성합니다.
    # 이 변수는 앱이 다시 실행되더라도 대화 내용을 유지해 줍니다.
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # `st.chat_message`를 사용하여 기존 대화 내용을 화면에 표시합니다.
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 채팅 입력창을 생성합니다. 화면 하단에 자동으로 표시됩니다.
    if prompt := st.chat_input("궁금한 점을 물어보세요!"):

        # 사용자가 입력한 메시지를 세션 상태에 저장하고 화면에 표시합니다.
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # OpenAI API를 사용하여 답변을 생성합니다.
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )

        # `st.write_stream`을 사용하여 답변이 생성되는 과정을 실시간으로 보여주고, 
        # 최종 답변을 세션 상태에 저장합니다.
        with st.chat_message("assistant"):
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})
