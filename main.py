from bs4 import BeautifulSoup
import requests
import pandas as pd
from email.message import EmailMessage
import ssl
import smtplib
import time


def send_mail(f_df_new, n_df_new):
    email_sender = 'azridoy19@gmail.com'
    email_password = 'uitsziyydszxuifi'

    email_reciever = 'azr1doyblogger@gmail.com'

    subject = 'BdJobs Notification'
    if len(f_df_new) > 0 and len(n_df_new) > 0:
        body = f"""
            These are the new featured jobs
            {f_df_new.to_string(index=False)}
            These are the new jobs
            {n_df_new.to_string(index=False)}
            """
    elif len(f_df_new) > 0 and len(n_df_new) == 0:
        body = f"""
                 These are the new featured jobs
                 {f_df_new.to_string(index=False)}
                 """
    elif len(f_df_new) == 0 and len(n_df_new) > 0:
        body = f"""
            These are the new jobs
            {n_df_new.to_string(index=False)}
            """
    else:
        body = f"""
                There is no new job
                    """


    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_reciever
    em['subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_reciever, em.as_string())


html_text = requests.get('https://jobs.bdjobs.com/jobsearch.asp?fcatId=8&icatId=').text
soup = BeautifulSoup(html_text, 'lxml')


# Creating dataframe for feautured jobs
f_job_list = []
f_jobs = soup.find_all('div', class_='col-sm-8 details')
for f_job in f_jobs:
    f_job_title = f_job.find('div', class_='title').text
    f_part = f_job.find('a').get('href')
    f_link = f'https://jobs.bdjobs.com/{f_part}'
    f_job_item = (f_job_title.strip(), f_link)
    f_job_list.append(f_job_item)

f_df = pd.DataFrame(f_job_list, columns=[' ', ' '])


# Creating dataframe for normal jobs
n_job_list = []
n_jobs = soup.find_all('div', class_='col-sm-9 col-sm-pull-9')
for n_job in n_jobs:
    n_job_title = n_job.find('div', class_='job-title-text').text
    n_part = n_job.find('a').get('href')
    n_link = f'https://jobs.bdjobs.com/{n_part}'
    n_job_item = (n_job_title.strip(), n_link)
    n_job_list.append(n_job_item)

n_df = pd.DataFrame(n_job_list, columns=[' ', ' '])

print(n_df)
print()
print(f_df)

time.sleep(86400)


# new featured jobs
f_job_list_new = []
f_jobs_new = soup.find_all('div', class_='col-sm-8 details')
for f_job in f_jobs_new:
    f_job_title = f_job.find('div', class_='title').text
    f_part = f_job.find('a').get('href')
    f_link = f'https://jobs.bdjobs.com/{f_part}'
    f_job_item = (f_job_title.strip(), f_link)
    f_job_list_new.append(f_job_item)

f_df1 = pd.DataFrame(f_job_list_new, columns=[' ', ' '])
frames_f = [f_df1, f_df]
f_df2 = pd.concat(frames_f, ignore_index=True)
f_duplicate = f_df2[f_df2.duplicated(subset=None, keep=False)]
f_index = len(f_duplicate.index)
if f_index > 0:
    i = f_duplicate.index[0]
    f_df_new = f_df2.iloc[:i]
else:
    f_df_new = f_df1

f_df = f_df1

# new normal jobs
n_job_list_new = []
n_jobs_new = soup.find_all('div', class_='col-sm-9 col-sm-pull-9')
for n_job in n_jobs_new:
    n_job_title = n_job.find('div', class_='job-title-text').text
    n_part = n_job.find('a').get('href')
    n_link = f'https://jobs.bdjobs.com/{n_part}'
    n_job_item = (n_job_title.strip(), n_link)
    n_job_list_new.append(n_job_item)

n_df4 = pd.DataFrame(n_job_list_new, columns=[' ', ' '])
frames_n = [n_df4, n_df]
n_df5 = pd.concat(frames_n, ignore_index=True)
n_duplicate = n_df5[n_df5.duplicated(subset=None, keep=False)]
n_index = len(n_duplicate.index)
if n_index > 0:
    i = n_duplicate.index[0]
    n_df_new = n_df5.iloc[:i]
else:
    n_df_new = n_df4

n_df = n_df4
send_mail(f_df_new, n_df_new)
time.sleep(86400)

















