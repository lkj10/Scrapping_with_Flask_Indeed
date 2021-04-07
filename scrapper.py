# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup

LIMIT = 50


def get_last_page(URL):
    result = requests.get(URL)
    soup = BeautifulSoup(result.text, "html.parser")
    pagination = soup.find("div", {"class": "pagination"})

    links = pagination.find_all('a')
    pages = []

    for link in links[:-1]:
        pages.append(int(link.string))

    max_page = pages[-1]
    return max_page


def extract_job(html):
    title = html.find("h2", {"class": "title"}).find("a")["title"]
    company = html.find("span", {"class": "company"})

    if company:
        company_anchor = company.find("a")
        if company_anchor is not None:
            company = str(company_anchor.string)
        else:
            company = str(company.string)
        company = company.strip()
    else:
        company = None

    location = html.find("div", {"class": "recJobLoc"})['data-rc-loc']
    job_id = html["data-jk"]

    return {'title': title,
            "company": company,
            "location": location,
            "link": f"https://www.indeed.com/viewjob?jk={job_id}&from=web&vjs=3"
            }


def extract_jobs(last_page, url):

    jobs = []
    for page in range(last_page):
        print(f"Scrapping page {page}")
        result = requests.get(f"{url}&start={page*LIMIT}")
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("div", {"class": "jobsearch-SerpJobCard"})
        for result in results:
            job = extract_job(result)
            jobs.append(job)
    return jobs


def get_jobs(word):
    URL = f"https://www.indeed.com/jobs?q={word}&limit={LIMIT}"
    last_page = get_last_page(URL)
    jobs = extract_jobs(last_page, URL)
    return jobs
