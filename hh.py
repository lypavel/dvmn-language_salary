from datetime import datetime, timedelta

import requests as rq

from salary_tools import predict_salary, count_average_salary


def hh_get_vacancies(payload: dict) -> dict:
    api_url = "https://api.hh.ru/vacancies"

    response = rq.get(api_url, params=payload)
    response.raise_for_status()

    return response.json()


def hh_predict_rub_salary(vacancy: dict) -> int | None:
    salary = vacancy.get("salary")
    if not salary:
        return None

    currency = salary.get("currency")
    if currency != "RUR":
        return None

    salary_from = salary.get("from")
    salary_to = salary.get("to")

    return predict_salary(salary_from, salary_to)


def hh_collect_stats(language: str = "") -> dict:
    date_from = datetime.now() - timedelta(days=30)

    town_id = "1"  # Moscow id
    vacancies_per_page = 100
    page = 0
    pages = 1

    payload = {
        "text": " ".join(["Программист", language]),
        "area": town_id,
        "per_page": vacancies_per_page,
        "date_from": date_from.isoformat()[:10],
        "page": page
    }

    vacancies = []

    while page < pages:
        response = hh_get_vacancies(payload)
        vacancies.extend(response.get("items"))

        vacancies_found = response.get("found")
        page += 1
        pages = response.get("pages", 1)

        payload.update({"page": page})

    salaries = []
    for vacancy in vacancies:
        salary = hh_predict_rub_salary(vacancy)
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
