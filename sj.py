import os
from datetime import datetime, timedelta

import requests as rq
from dotenv import load_dotenv

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


def sj_collect_stats(language: str = "") -> dict:
    load_dotenv()

    sj_secret_key = os.environ["SJ_SECRET_KEY"]

    date_from = datetime.now() - timedelta(days=30)

    payload = {
        "town": 4,
        "catalogues": 48,
        "keyword": language,
        "count": 100,
        "date_published_from": date_from.timestamp()
    }

    sj_response = sj_get_vacancies(sj_secret_key, payload)
    vacancies = sj_response.get("objects")

    salaries = [
        sj_predict_rub_salary(x) for x in vacancies if sj_predict_rub_salary(x)
    ]

    try:
        average_salary = count_average_salary(salaries)
    except ZeroDivisionError:
        average_salary = 0

    return {
        language: {
            "vacancies_found": sj_response.get("total"),
            "vacancies_processed": len(salaries),
            "average_salary": average_salary
        }
    }


if __name__ == "__main__":
    print(sj_collect_stats())
