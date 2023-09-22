# https://www.blog.datahut.co/post/scrape-indeed-using-selenium-and-beautifulsoup
#from webbrowser import Chrome

from bs4 import BeautifulSoup #Parses and pulls out data from HTML and XML files
from lxml import etree as et #Processes HTML and XML files
from csv import writer
# GPT tweak to specify binary locations 
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
# tweak end
from selenium import webdriver #WebDriver that basically acts as an automated browser via API requests
from webdriver_manager.chrome import ChromeDriverManager #Needed library for selenium to use chrome
# GPT Tweak 
from selenium.webdriver.common.keys import Keys
# tweak end
import time #will allow the ability to set sleep time per request so server doesn't flag as DDOS


# define job and location search keywords
job_search_keyword = ['researcher', 'phd', 'deep learning']
location_search_keyword = ['Amsterdam', 'Zurich', 'Berlin']

# define base and pagination URLs
base_url = 'https://www.nl.indeed.com'
pagination_url = 'https://www.nl.indeed.com/jobs?q={}&l={}&radius=35&start={}'

#init Chrome webdriver using ChromeDriverManager so Selenium can be used (path mentioned otherwise selenium won't find it in pipenv)
options = Options()
options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

#open initial URL
driver.get("https://www.nl.indeed.com/q-researcher-jobs.html?vjk=823cd7ee3c203ac3")

# function to get DOM from given URL above (each combo from the list above returns a unique URL)
def get_dom(url):
   driver.get(url)
   page_content = driver.page_source
   product_soup = BeautifulSoup(page_content, 'html.parser')
   dom = et.HTML(str(product_soup))
   return dom


#With URLs set and getter function created, now we extract elements from the DOM. May need to update over time


# functions to extract job link
def get_job_link(job):
   try:
       job_link = job.xpath('./descendant::h2/a/@href')[0]
   except Exception as e:
       job_link = 'Not available'
   return job_link

# functions to extract job title
def get_job_title(job):
   try:
       job_title = job.xpath('./descendant::h2/a/span/text()')[0]
   except Exception as e:
       job_title = 'Not available'
   return job_title

# functions to extract the company name
def get_company_name(job):
   try:
       company_name = job.xpath('./descendant::span[@class="companyName"]/text()')[0]
   except Exception as e:
       company_name = 'Not available'
   return company_name

# functions to extract the company location
def get_company_location(job):
   try:
       company_location = job.xpath('./descendant::div[@class="companyLocation"]/text()')[0]
   except Exception as e:
       company_location = 'Not available'
   return company_location

# functions to extract salary information
def get_salary(job):
   try:
       salary = job.xpath('./descendant::span[@class="estimated-salary"]/span/text()')
   except Exception as e:
       salary = 'Not available'
   if len(salary) == 0:
       try:
           salary = job.xpath('./descendant::div[@class="metadata salary-snippet-container"]/div/text()')[0]
       except Exception as e:
           salary = 'Not available'
   else:
       salary = salary[0]
   return salary

# functions to extract job type
def get_job_type(job):
   try:
       job_type = job.xpath('./descendant::div[@class="metadata"]/div/text()')[0]
   except Exception as e:
       job_type = 'Not available'
   return job_type

# functions to extract job rating
def get_rating(job):
   try:
       rating = job.xpath('./descendant::span[@class="ratingNumber"]/span/text()')[0]
   except Exception as e:
       rating = 'Not available'
   return rating

# functions to extract job description
def get_job_desc(job):
   try:
       job_desc = job.xpath('./descendant::div[@class="job-snippet"]/ul/li/text()')
   except Exception as e:
       job_desc = ['Not available']
   if job_desc:
       job_desc = ",".join(job_desc)
   else:
       job_desc = 'Not available'
   return job_desc


# Extraction complete, now we export using f stream to CSV


# Open a CSV file to write the job listings data
with open('indeed_jobs1.csv', 'w', newline='', encoding='utf-8') as f:
   theWriter = writer(f)
   heading = ['job_link', 'job_title', 'company_name', 'company_location', 'salary', 'job_type', 'rating', 'job_description', 'searched_job', 'searched_location']
   theWriter.writerow(heading)
   for job_keyword in job_search_keyword:
       for location_keyword in location_search_keyword:
           all_jobs = []
           for page_no in range(0, 100, 10):
               url = pagination_url.format(job_keyword, location_keyword, page_no)
               page_dom = get_dom(url)
               jobs = page_dom.xpath('//div[@class="job_seen_beacon"]')
               all_jobs = all_jobs + jobs
           for job in all_jobs:
               job_link = base_url + get_job_link(job)
               time.sleep(20)
               job_title = get_job_title(job)
               time.sleep(20)
               company_name = get_company_name(job)
               time.sleep(20)
               company_location = get_company_location(job)
               time.sleep(20)
               salary = get_salary(job)
               time.sleep(20)
               job_type = get_job_type(job)
               time.sleep(20)
               rating = get_rating(job)
               time.sleep(20)
               job_desc = get_job_desc(job)
               time.sleep(20)
               record = [job_link, job_title, company_name, company_location, salary, job_type, rating, job_desc, job_keyword, location_keyword]
               print(record) #check to see what's actually being pulled for debugging
               theWriter.writerow(record)

# Closing the web browser
driver.quit()