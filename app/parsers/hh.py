import requests
from bs4 import BeautifulSoup
from datetime import datetime


BASE_URL = "https://hh.kz/search/vacancy"

HEADERS = {
    "User-Agent": "jobtracker-bot/1.0 (+https://example.com)"
}


def fetch_vacancies_for_filter(filter_obj, pages: int = 1):
    results = []
    for page in range(pages):
        params = {"text": filter_obj.keyword, "page": page}
        if getattr(filter_obj, "location", None):
            params["area"] = filter_obj.location

        r = requests.get(BASE_URL, params=params, headers=HEADERS, timeout=10)
        if r.status_code != 200:
            break

        soup = BeautifulSoup(r.text, "html.parser")
        cards = soup.find_all("div", {"data-qa": "vacancy-serp__vacancy"})
        if not cards:
            cards = soup.find_all("div", class_="vacancy-serp-item")

        for c in cards:
            title_el = c.find("a", {"data-qa": "vacancy-serp__vacancy-title"}) or c.find("a")
            title = title_el.get_text(strip=True) if title_el else None
            url = title_el["href"] if title_el and title_el.has_attr("href") else None

            company_el = c.find("a", {"data-qa": "vacancy-serp__vacancy-employer"})
            company = company_el.get_text(strip=True) if company_el else None

            loc_el = c.find("span", {"data-qa": "vacancy-serp__vacancy-address"})
            location = loc_el.get_text(strip=True) if loc_el else None

            salary_el = c.find("span", {"data-qa": "vacancy-serp__vacancy-compensation"})
            salary = salary_el.get_text(strip=True) if salary_el else None

            results.append({
                "title": title,
                "company": company,
                "location": location,
                "salary": salary,
                "url": url,
                "source": "hh.ru",
                "created_at": datetime.utcnow(),
            })
    return results
