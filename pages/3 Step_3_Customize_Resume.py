import streamlit as st
import config as cfg
import streamlit_scrollable_textbox as stx
from streamlit_extras.metric_cards import style_metric_cards


st.markdown("""
<style>
    [data-testid=stSidebar] {
        background-color: #E5F8F7;
    }
</style>
""", unsafe_allow_html=True)
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
        <h1>Customize Resume<br> <span>[ Step Three ]</span></h1>
    
    </header>
    """
st.html(banner_html + banner_css)
a, b, c, d, e = st.columns(5)
a.metric(label="Upload Your Resume", value="Step 1")
b.metric(label="Search Jobs", value="Step 2")
c.metric(label="Get Custom Resume", value="Step 3")
d.metric(label="Get Custom Cover Letter", value="Step 4")
e.metric(label="Get Interview Coaching", value="Step 5")
style_metric_cards(box_shadow=True, border_left_color="#A9E9E6")
st.divider()
client = cfg.client

def parse_job_desc(resume_text, job_description):
    with st.spinner("Generating Custom Resume..."):
        response = client.chat.completions.create(
            
            messages=[
                {
                    "role": "system",
                    "content": "You are a career expert and a job description expert. \
                                You have been provided with a job description and must parse the most relevant information from it and summarize.\
                                Your output should include the key desired skills for the position and any requirements."
                },
                {
                    "role": "user",
                    "content": job_description
                }
            ],
            model="llama3:latest",
        )
        summarized_description = response.choices[0].message.content
        resume(resume_text, summarized_description)

def resume(resume_text, job_description):
    print(job_description)
    try:
        
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a career and resume expert, extensively trained in ATS and STAR resume formats. \
                                Rewrite the resume using ATS format to make the user the top candidate for this jobs. \
                                You should analyze the requirements and useable skills, then create a new resume based on these. \
                                Your final output is a formatted resume for the user. Do not provide any other text output except a new resume.1\
                                Return the results with markdown, bullets, and clean formatting. \
                                Use STAR format for past job experience updates where possible. \
                                Do not make up any companies, skills, or experience. Only reword or revise existing information to match the keywords.",
                },

                {
                    "role": "user",
                    "content": f"Resume to Rewrite: {resume_text}",
                },
                {
                    "role": "user",
                    "content": f"Job Description:\n{job_description}",  # Use selected_job directly
                },
            ],
            model="llama3:latest",
        )
    except Exception as e:
        print(f"Error: {e}")
        return None

    if not response.choices:
        print("No choices were returned by the model.")
        return None
    print("response: ", response)
    final_resume = response.choices[0].message.content

    stx.scrollableTextbox(final_resume, height=1200)

if 'resume_text' not in st.session_state or 'job_description' not in st.session_state:
    st.error("Please Complete Step 1 and Step 2 to get a custom cover letter.")
else:
    parse_job_desc(resume_text = st.session_state['resume_text'], job_description= st.session_state['job_description'])