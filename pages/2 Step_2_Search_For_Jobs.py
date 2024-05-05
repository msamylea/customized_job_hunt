import streamlit as st
import config as cfg
import pull_joblist as pj
from streamlit_extras.metric_cards import style_metric_cards
import os
import time
from streamlit_extras.stylable_container import stylable_container
st.set_page_config(page_title="End to End Career Search Assistant", page_icon=":job:", layout="wide")

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
        <h1>Search For Jobs<br> <span>[ Step Two ]</span></h1>
    
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
def search_for_jobs():

    col1, col2 = st.columns(2)
    with col1:
        with st.form(key="joblists"):
            search_term = st.text_input("Search Term", key="search_term")
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
                if st.form_submit_button("Search Jobs"):
                    if search_term:  # changed this line
                        st.session_state['jobs'] = pj.get_jobs(search_term)
                        if 'jobs' in st.session_state:
                            for idx, (_, job) in enumerate(st.session_state['jobs'].iterrows()):
                                job = job.to_dict()
                                with st.expander(str(job["Company"]) + " -- " + str(job["Job_Title"])):
                                    st.markdown(job["Description"])
                                    st.markdown(f"[Read more]({job['Link']})")
                        st.session_state['job_titles'] = st.session_state['jobs']['Job_Title'].tolist()
                    else:
                        st.error("Please enter a search term.")
        with col2:
            job_titles = st.session_state.get('job_titles', [])
            with st.form(key="job_selection"):
                if 'selected_job' not in st.session_state:
                    st.session_state['selected_job'] = job_titles[0] if job_titles else None
                st.selectbox(options=job_titles, label="Select Job", key='selected_job')
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
                    job_submit = st.form_submit_button("Get Resume for this Job")

                    if job_submit and 'jobs' in st.session_state:
                        st.session_state['job_description'] = st.session_state['jobs'][st.session_state['jobs']['Job_Title'] == st.session_state['selected_job']]['Description'].values[0]
                        st.switch_page("pages/3 Step_3_Customize_Resume.py")
                
session_id = str(time.time()) if 'session_id' not in st.session_state else st.session_state['session_id']

# If the session ID has changed, clear the session state
if session_id != st.session_state.get('session_id', ''):
    st.session_state.clear()

# Update the session ID in the session state
st.session_state['session_id'] = session_id

# # Initialize 'resume_text' if it does not exist
# if 'resume_text' not in st.session_state:
#     st.session_state['resume_text'] = ''

# Now you can safely access 'resume_text'
if 'resume_text' not in st.session_state:
    st.error("Please Complete Step 1 to Perform a Job Search.")
else:
    resume = st.session_state['resume_text']
    search_for_jobs()
