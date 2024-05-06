
from jobspy import scrape_jobs
import config as cfg


def get_jobs(query):
    jobs = scrape_jobs(
        site_name=["ADD SITES"],
        search_term=query,
        location="Remote",
        is_remote=True,
        results_wanted=20,
        hours_old=168,
        country_indeed='USA',
        hyperlinks=True
    )

    jobs.to_csv('jobs.csv', index=False)
    jobs = jobs.assign(
        Link=jobs['job_url_direct'],
        Job_Title=jobs['title'],
        Company=jobs['company'],
        Salary_Range=jobs.apply(lambda row: f"{row['min_amount']} - {row['max_amount']}", axis=1),
        Description=jobs['description'].replace('\*\*|###', '', regex=True)
    )
    jobs = jobs[['Link', 'Job_Title', 'Company', 'Salary_Range', 'Description']]
    
    return jobs
