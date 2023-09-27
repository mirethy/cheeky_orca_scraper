import requests
from bs4 import BeautifulSoup
import os
import csv
import pandas as pd
import numpy

# TODO: finish adding attributes, discription, date posted, and link
# TODO: Pair all the info to each company
# TODO: Put them into excel

titles = []
company_names = []
company_locations = []
estimate_salaries = []

#requests
r = requests.get(f"WEBSITE URL")
print(r.status_code) #keep till after changing link
response = r.content

#parse
soup = BeautifulSoup(response, "lxml")

#find job title
titles = soup.find_all("h2", class_="jobTitle")
for title in titles:
    print(title.text)

print()

#find company name
company_names = soup.find_all("span", class_="companyName")
for name in company_names:
    print(name.text)

print()
#find company location
company_locations = soup.find_all("div", class_="companyLocation")
for location in company_locations:
    print(location.text)

print()
#find estimate salary by indeed
estimate_salaries = soup.find_all("span", class_="estimated-salary")
for salary in estimate_salaries:
    print(salary.text)

#jobs = [titles, company_names, company_locations, estimate_salaries]
#numpy.rot90(jobs)

df = pd.DataFrame(titles)
df.to_csv('jobsTEST.csv')
