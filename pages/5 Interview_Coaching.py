import streamlit as st
import interview_config
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

st.set_page_config(layout="wide")

llm = interview_config.client
banner_css = """
    <style>
    @import url('https://fonts.googleapis.com/css?family=Montserrat:400,700');
    @import url('https://fonts.googleapis.com/css?family=Lato:300');
    header {
        background-color: #87BAB8;
        color: white;
        text-align: center;
        padding: 10px 0 20px;
        width: 100%;
    }
    header h1 {
        text-align: center;
        text-transform: uppercase;
        color: white;
        font-size: 65px;
        font-weight: 400;
        letter-spacing: 3px;
        line-height: 0.8;
        padding-top: 50px;
        font-family: "Montserrat", sans-serif;
    }
    header h1 span {
        text-transform: uppercase;
        letter-spacing: 7px;
        font-size: 25px;
        line-height: 1;
    }
    header p {
        padding-top: 30px;
    }
    .wrapper {
        justify-content: center;
        padding: 15px;
    }

    .header-card {
        border-radius: 20px;
        box-shadow: 10px 10px 10px 0px rgba(255,255,255,0.05), -3px -3px 3px 0px rgba(255,255,255,0.1);
    
        padding: 0px 20px 0px 20px;
        justify-content: center;
        align-items: center;
    }

    .header-title {
        font-family: "Montserrat", sans-serif;
        font-size: 18px;
        font-weight: 600;
        color: white;
        letter-spacing: 1px;
        margin-bottom: 5px;
    }

    .header-text {
        font-family: "Montserrat", sans-serif;
        font-size: 16px;
        color: #F8F8FF;
        margin-bottom: 10px;
        padding-bottom: 10px;
        text-align: center;
    }
    </style>
    """

banner_html = """
    <header>
        <h1>Interview Coaching<br> <span>[ Get Immediate Feedback ]</span></h1>
    
    </header>
    """

st.html(banner_css + banner_html)
st.markdown(
    """
<style>
    .st-emotion-cache-1c7y2kd {
        flex-direction: row-reverse;
        text-align: right;
    }
    
</style>
""",
    unsafe_allow_html=True,
)



prompt_template = """You are an expert in conducting career interviews. You use a mixture of questions designed to delve deep into a candidates 
thought processes, past experiences, ability to think quickly, personality, adaptability, and creativity. 
You will not respond to harmful or inappropriate questions or content. You are a professional and act like an expert.
Your goal is to provide detailed feedback that will help the candidate improve their interview performance.
You will provide feedback to the candidate at the end of your interview.
After the end of the interview, you will ask the candidate if they want to continue with another question until the candidate says they are finished.
In the chat history you are 'assistant' and the human is 'user'
The chat history before the last question is:
{chat_history}
And the last question is:
{question}
"""
prompt = PromptTemplate(
                        input_variables=['chat_history', 'question'],
                        template=prompt_template,
                        )
#Create the chain for LangChain
chain = prompt | llm | StrOutputParser()
st.session_state.model_set = True

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Hi, I'm your interview coach today. Please introduce yourself and we can get started."}]

message_container = st.container(height=550, border=True)

### Write Message History
for msg in st.session_state.messages:
    if msg["role"] == "user":
       with message_container:
            st.chat_message(msg["role"], avatar="🙋").markdown(msg["content"])
    else:
      with message_container:
            st.chat_message(msg["role"], avatar="🧑‍💼").markdown(msg["content"])

## Generator for Streaming Tokens
def generate_response(question):
    response = chain.invoke({'chat_history':st.session_state['messages'],
                             'question':question})
    return (response)

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    with message_container:

        st.chat_message("user", avatar="🙋").markdown(prompt)
    response = generate_response(prompt)
    with message_container:
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.chat_message("assistant", avatar="🧑‍💼").markdown(response)
