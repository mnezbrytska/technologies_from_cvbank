import time

import matplotlib.pyplot as plt
import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

BASE_URL = "https://www.cvbankas.lt"
SEARCH_URL = f"{BASE_URL}/?keyw=python"

driver = webdriver.Chrome()


def fetch_vacancy_links():
    vacancy_links = []
    driver.get(SEARCH_URL)

    while True:
        soup = BeautifulSoup(driver.page_source, "html.parser")

        for job_card in soup.select(".list_article"):
            link_tag = job_card.select_one("a")
            if link_tag and "href" in link_tag.attrs:
                link = link_tag["href"]
                full_link = link if link.startswith("https") else BASE_URL + link
                vacancy_links.append(full_link)

        try:
            next_button = driver.find_element(By.CSS_SELECTOR, ".prev_next")
            if "disabled" in next_button.get_attribute("class"):
                break
            else:
                next_button.click()
                time.sleep(2)
        except Exception:
            break
    return vacancy_links


def parse_vacancy(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    title = soup.select_one(
        "h1[itemprop='title']"
    ).get_text(strip=True) if soup.select_one("h1[itemprop='title']") else "N/A"

    company_element = soup.select_one("div#jobad_location.txt_2")
    if company_element:
        company_name = " ".join(company_element.get_text(strip=True).split()[1:])
    else:
        company_name = 'N/A'

    location = soup.find(
        "span", itemprop="addressLocality"
    ).get_text(strip=True) if soup.find("span", itemprop="addressLocality"
                                        ) else "N/A"
    salary = soup.find(
        "span", class_="salary_amount"
    ).get_text(strip=True) if soup.find("span", class_="salary_amount"
                                        ) else "N/A"

    description = soup.select_one(
        "div", class_="jobad_txt"
    ).get_text(strip=True) if soup.select_one("div", class_="jobad_txt"
                                              ) else "N/A"

    return {
        "title": title,
        "salary": salary,
        "company": company_name,
        "location": location,
        "description": description,
        "url": url
    }


def scrape_cvbankas():
    vacancy_links = fetch_vacancy_links()
    vacancies = []

    for link in vacancy_links:
        print(f"vacancy: {link}")
        vacancy = parse_vacancy(link)
        vacancies.append(vacancy)
        time.sleep(1)

    df = pd.DataFrame(vacancies)
    df.to_csv("cvbankas_python_vacancies.csv", index=False)
    print("Information has been written to the file: cvbankas_python_vacancies.csv")


scrape_cvbankas()

driver.quit()

df = pd.read_csv("cvbankas_python_vacancies.csv")
urls = df["url"].tolist()

technologies = [
    "Python", "GIT", "SQL", "REST", "API", "docker", "AWS", "Linux",
    "Django", "Postgresql", "Artificial Intelligence", "JS", "Machine Learning",
    "react", "OOP", "Flask", "NoSQL", "networking", "webstack",
    "microservice", "MongoDB", "HTML", "CSS", "algorithms", "DRF",
    "FastAPI", "asyncio", "Graphql"
]

tech_counts = {tech: 0 for tech in technologies}


def get_job_description(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        description_tag = soup.select_one("div", class_="jobad_txt")
        return description_tag.get_text(strip=True) if description_tag else ""
    except Exception:
        return ""


for url in urls:
    description = get_job_description(url)
    if description:
        for tech in technologies:
            if tech.lower() in description.lower():
                tech_counts[tech] += 1
    time.sleep(1)

output_df = pd.DataFrame(list(tech_counts.items()), columns=["Technology", "Count"])
output_df.to_csv("tech_demand_counts.csv", index=False)
print("Results were written to: tech_demand_counts.csv")

plt.figure(figsize=(12, 6))
plt.bar(tech_counts.keys(), tech_counts.values())
plt.xticks(rotation=90)
plt.xlabel("Technologies")
plt.ylabel("Number of mentions")
plt.title("Popularity of technology in vacancies on the CVBankas website")
plt.show()
