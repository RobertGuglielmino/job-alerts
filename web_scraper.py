import ssl
import time
import requests
from bs4 import BeautifulSoup
# Import smtplib for the actual sending function
import smtplib
from plyer import notification

# Import the email modules we'll need
from email.message import EmailMessage

from job_titles import BAD_NAMES, GOOD_NAMES

# https://medium.com/@beckernick/faster-web-scraping-in-python-e3fba2ebb541



# import concurrent.futures

# MAX_THREADS = 30

# def download_url(url):
#     print(url)
#     resp = requests.get(url)
#     title = ''.join(x for x in url if x.isalpha()) + "html"
    
#     with open(title, "wb") as fh:
#         fh.write(resp.content)
        
#     time.sleep(0.25)
    
# def download_stories(story_urls):
#     threads = min(MAX_THREADS, len(story_urls))
    
#     with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
#         executor.map(download_url, story_urls)

# def main(story_urls):
#     t0 = time.time()
#     download_stories(story_urls)
#     t1 = time.time()
#     print(f"{t1-t0} seconds to download {len(story_urls)} stories.")

JOB_LINKS = ['https://job-boards.greenhouse.io/growtherapy?offices%5B%5D=4011317005']

def scrape(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    jobList = []
    
    for a in soup.findAll('a'):
        if a.p and checkTitle(a.p.text):
            print(a['href'])
            jobList.append(a['href'])


    notification.notify(
        title='this is crazy',
        message='This is a notification message.',
        app_name='My App',
        timeout=10  # Duration in seconds
    )

    # message = EmailMessage()
    # message.set_content('https://job-boards.greenhouse.io/growtherapy?offices%5B%5D=4011317005')

    # # me == the sender's email address
    # # you == the recipient's email address
    # message['Subject'] = f'job time'
    # message['From'] = "robert.gugliel@gmail.com"
    # message['To'] = "robert.gugliel@gmail.com"

    # # Create secure SSL/TLS context
    # context = ssl.create_default_context()

    # try:
    #     # For Gmail
    #     server = smtplib.SMTP('smtp.gmail.com', 587)
    #     server.set_debuglevel(1)  # Enable debug output
        
    #     print("Connecting to server...")
    #     server.starttls(context=context)  # Enable TLS with secure context
        
    #     print("Logging in...")
    #     server.login("robert.gugliel@gmail.com", PASSWORD)
        
    #     print("Sending email...")
    #     server.send_message(message)
    #     print("Email sent successfully!")
        
    # except smtplib.SMTPAuthenticationError:
    #     print("Authentication failed. Please check your email and password.")
    #     print("If using Gmail, make sure you're using an App Password.")
    # except ConnectionRefusedError:
    #     print("Connection refused. Please check:")
    #     print("1. Your internet connection")
    #     print("2. Firewall settings")
    #     print("3. Antivirus settings")
    # except smtplib.SMTPException as e:
    #     print(f"SMTP error occurred: {e}")
    # except Exception as e:
    #     print(f"An error occurred: {e}")
    # finally:
    #     try:
    #         server.quit()
    #     except:
    #         pass


def checkTitle(title):
    for name in GOOD_NAMES:
        if name not in title:
            return False
    for name in BAD_NAMES:
        if name in title:
            return False
    return True

if __name__ == '__main__':
    url = 'https://job-boards.greenhouse.io/growtherapy?offices%5B%5D=4011317005'
    start_time = time.time()

    for job in JOB_LINKS:
        scrape(job)
    print("--- %s seconds ---" % (time.time() - start_time))