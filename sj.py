from datetime import datetime, timedelta

import requests as rq

from salary_tools import predict_salary, count_average_salary


def sj_get_vacancies(secret_key: str, payload: dict = None) -> dict:
    api_url = "https://api.superjob.ru/2.0/vacancies/"

    headers = {
        "X-Api-App-Id": secret_key
    }

    response = rq.get(api_url, headers=headers, params=payload)
    response.raise_for_status()

    return response.json()


def sj_predict_rub_salary(vacancy: dict) -> int | None:
    currency = vacancy.get("currency")
    if currency != "rub":
        return

    salary_from = vacancy.get("payment_from")
    salary_to = vacancy.get("payment_to")

    if any([salary_from, salary_to]):
        return predict_salary(salary_from, salary_to)
    else:
        return None


def sj_collect_stats(sj_secret_key: str, language: str = "") -> dict:
    date_from = datetime.now() - timedelta(days=30)
    town_id = 4  # Moscow id
    search_category = 48  # id "Разработка, программирование"
    vacancies_per_page = 100
    page = 0
    more_vacancies_avaliable = True

    payload = {
        "town": town_id,
        "catalogues": search_category,
        "keyword": language,
        "count": vacancies_per_page,
        "date_published_from": date_from.timestamp(),
        "page": page
    }

    vacancies = []

    while more_vacancies_avaliable:
        response = sj_get_vacancies(sj_secret_key, payload)
        vacancies.extend(response.get("objects"))

        vacancies_found = response.get("total")
        page += 1
        more_vacancies_avaliable = response.get("more")

        payload["page"]: page

    salaries = []
    for vacancy in vacancies:
        salary = sj_predict_rub_salary(vacancy)
        if not salary:
            continue
        salaries.append(salary)

    try:
        average_salary = count_average_salary(salaries)
    except ZeroDivisionError:
        average_salary = 0

    return {
        language: {
            "vacancies_found": vacancies_found,
            "vacancies_processed": len(salaries),
            "average_salary": average_salary
        }
    }
