import requests
from bs4 import BeautifulSoup

l=[]
o={}


target_url = "https://api.scrapingdog.com/scrape?api_key=650d6342dacdc855c236466f&url=https://nl.indeed.com/jobs?q=researcher&l=Amsterdam&from=searchOnHP&vjk=cc167a106a46f6b9&dynamic=false"
head= {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Connection": "keep-alive",
    "Accept-Language": "en-US,en;q=0.9,lt;q=0.8,et;q=0.7,de;q=0.6",
}

resp = requests.get(target_url, headers=head)
print(resp.status_code)
soup = BeautifulSoup(resp.text, 'html.parser')

allData = soup.find("ul",{"class":"jobsearch-ResultsList css-0"})

alllitags = allData.find_all("div",{"class":"cardOutline"})
print(len(alllitags))
for i in range(0,len(alllitags)):
    try:
        o["name-of-the-job"]=alllitags[i].find("a",{"class":"jcs-JobTitle css-jspxzf eu4oa1w0"}).text
    except:
        o["name-of-the-job"]=None

    try:
        o["name-of-the-company"]=alllitags[i].find("div",{"class":"companyInfo"}).find("span",{"class":"companyName"}).text
    except:
        o["name-of-the-company"]=None


    try:
        o["salary"]=alllitags[i].find("div",{"class":"salary-snippet-container"}).text
    except:
        o["salary"]=None

    try:
        o["job-details"]=alllitags[i].find("div",{"class":"metadata taxoAttributes-container"}).find("ul").text
    except:
        o["job-details"]=None

    l.append(o)
    o={}


print(l)