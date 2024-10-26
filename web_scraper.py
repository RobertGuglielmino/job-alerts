import time
import requests
from bs4 import BeautifulSoup
import schedule
import time

from job_boards import JOB_LINKS
from job_titles import BAD_NAMES, GOOD_NAMES
from notifiers import notifyDesktop

# https://medium.com/@beckernick/faster-web-scraping-in-python-e3fba2ebb541


def scrape(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    jobList = []
    htmlTags = ['p', 'div', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']
    # TODO multiple tags besides p
    for a in soup.findAll('a'):
        if a.p and checkTitle(a.p.text):
            print(a['href'])
            jobList.append(a['href'])
        if a.h3 and checkTitle(a.h3.text):
            print(a['href'])
            jobList.append(a['href'])

    return jobList

def checkTitle(title):
    for name in GOOD_NAMES:
        if name not in title:
            return False
    for name in BAD_NAMES:
        if name in title:
            return False
    # TODO check if in list already
    return True


def checkJobs():
    start_time = time.time()
    newJobs = []

    for job in JOB_LINKS:
        newJobs = scrape(job)

    for w in newJobs:
        notifyDesktop(w)

    print("--- %s seconds ---" % (time.time() - start_time))

def main():
    schedule.every(30).minutes.do(checkJobs)

    while True:
        schedule.run_pending()
        time.sleep(1)  # Check for scheduled tasks every second

if __name__ == '__main__':
    # main()
    checkJobs()