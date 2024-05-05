
import docx2txt
import PyPDF2 as pdf
import os
import config as cfg
import streamlit as st
from streamlit_extras.metric_cards import style_metric_cards
from streamlit_extras.stylable_container import stylable_container
from dotenv import load_dotenv
st.set_page_config(page_title="End to End Career Search Assistant", page_icon=":job:", layout="wide")
load_dotenv()

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
        <h1>Upload Your Resume <br> <span>[ Step One ]</span></h1>
    
    </header>
    """
st.html(banner_html + banner_css)
def extract_text(uploaded_file):
    if uploaded_file is not None:
        _, file_extension = os.path.splitext(uploaded_file.name)

        if file_extension == ".pdf":
            pdf_reader = pdf.PdfReader(uploaded_file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            return text
        elif file_extension == ".docx":
            text = docx2txt.process(uploaded_file)
            return text
        else:
            raise ValueError("Unsupported file type")
        
def process_resume(text):
    seen_keywords = set()
    for _ in range(10):
        model = cfg.client
        response = model.chat.completions.create(
            messages = [
                {
                    "role": "system",
                    "content": "You are a HR professional and expert in career advancement. \
                        Using the uploaded resume, create a narrowly focused job search of 2 to 3WORDS for the user that focuses on their strengths and experience. \
                        Your expected output is only a search phrase to be used in a job search with no other text included.\
                        Do not provide explanations or any text beyond a search phrase.\
                        Output Format Examples:\
                        - Artificial Intelligence  \
                        - Machine Learning  \
                        - Data Science  \
                            "
            
            f"Resume: {text}"
                }
            ],
            model = "llama3:latest"
        )
        keyword = response.choices[0].message.content
        if keyword not in seen_keywords:
            seen_keywords.add(keyword)
            yield keyword        

def main():
    a, b, c, d, e = st.columns(5)
    a.metric(label="Upload Your Resume", value="Step 1")
    b.metric(label="Search Jobs", value="Step 2")
    c.metric(label="Get Custom Resume", value="Step 3")
    d.metric(label="Get Custom Cover Letter", value="Step 4")
    e.metric(label="Get Interview Coaching", value="Step 5")
    style_metric_cards(box_shadow=True, border_left_color="#A9E9E6")
    st.divider()

    submit = False
    keywords = []
    col1, col2 = st.columns(2)
    with col1:
        with st.form(key="submit_form"):
            uploaded_file=st.file_uploader("Upload Your Resume",type=[".pdf", ".docx"],help="Please upload your resume")
            if uploaded_file is not None:
                st.write("File Uploaded Successfully")
            with stylable_container(
            key="teal_button",
            css_styles="""
                button {
                    background-color: #A9E9E6;
                    color: black;
                    border-radius: 20px;
                    padding: 10px 20px;
                }
                """,
            ):
                submit = st.form_submit_button("Generate Keywords")
        if submit and uploaded_file is None:
            st.error("Please upload your resume to start the process.")
        if submit and uploaded_file is not None:
            text = "resume: " + extract_text(uploaded_file)
            st.session_state['resume_text'] = text
            keywords = process_resume(text)
    with col2:
        with st.form(key="keyword_form"):
            st.subheader("Suggested Keywords from Your Skillset: ")
            with st.spinner("Generating Keywords..."):
                st.divider()
                
                for i, keyword in enumerate(keywords):
                    st.markdown(f"{i+1}. {keyword}")
            with stylable_container(
            key="teal_button",
            css_styles="""
                button {
                    background-color: #A9E9E6;
                    color: black;
                    border-radius: 20px;
                    padding: 10px 20px;
                }
                """,
            ):        
                job_search_btn = st.form_submit_button("Go To Step 2: Search Jobs")
           
            if job_search_btn:
                st.switch_page("pages/2 Step_2_Search_For_Jobs.py")
                



if __name__ == '__main__':
    main()