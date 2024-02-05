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

    payload = {
        "text": " ".join(["Программист", language]),
        "area": "1",
        "per_page": 100,
        "date_from": date_from.isoformat()[:10],
        "page": 0
    }

    vacancies = []

    hh_response = hh_get_vacancies(payload)
    pages = hh_response.get("pages")
    page = 0

    while page <= pages:
        response = hh_get_vacancies(payload)
        vacancies.extend(response.get("items"))
        page += 1

    salaries = [
        hh_predict_rub_salary(x) for x in vacancies if hh_predict_rub_salary(x)
    ]
    try:
        average_salary = count_average_salary(salaries)
    except ZeroDivisionError:
        average_salary = 0

    return {
        language: {
            "vacancies_found": hh_response.get("found"),
            "vacancies_processed": len(salaries),
            "average_salary": average_salary
        }
    }


if __name__ == "__main__":
    print(hh_collect_stats())
