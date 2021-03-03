import requests
from bs4 import BeautifulSoup

LIMIT = 50
URL = None

def setting_to_URL(word):
  global URL
  URL = f"https://www.indeed.com/jobs?q={word}&limit={LIMIT}"

def print_URL():
  print(URL)

def get_last_pages():

  result = requests.get(URL)

  soup = BeautifulSoup(result.text, "html.parser")

  pagination = soup.find("div", {"class":"pagination"})

  links = pagination.find_all('a')
  pages = []

  for link in links[:-1]:
     # link.string
    pages.append(int(link.find("span").string))

  max_page = pages[-1]
  return max_page

# print(f"start={n*50}")

def extract_job(html):
  title = html.find("h2", {"class": "title"}).find("a")["title"]
  company = html.find("span", {"class": "company"})
  if company is not None:
    company_anchor = company.find("a")
  else:
    company = None
  # delete None 1
  if company:
    if company_anchor is not None:
      company = (str(company_anchor.string))
    else:
      company = (str(company.string))
    company = company.strip()
  else:
    company = None
  # delete None 2
  location = html.find("div", {"class": "recJobLoc"})["data-rc-loc"]
  job_id = html["data-jk"]
  return {'title': title, 'company': company, 'location': location, "link": f"https://www.indeed.com/viewjob?jk={job_id}"}

def extract_jobs(last_page):
  jobs = []
  for page in range(last_page):
    print(f"Scrapping Indeed: Page: {page+1}")
    result = requests.get(f"{URL}&start={page*LIMIT}")
    soup = BeautifulSoup(result.text, "html.parser")
    results = soup.find_all("div", {"class": "jobsearch-SerpJobCard"})
    for result in results:
      job = extract_job(result)
      jobs.append(job)
  return jobs

def get_jobs(word):

  setting_to_URL(word)

  last_pages = get_last_pages()

  jobs = extract_jobs(last_pages)
  # jobs = extract_jobs(2)

  return jobs