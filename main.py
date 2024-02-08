import os

import requests as rq
from dotenv import load_dotenv
from terminaltables import AsciiTable

from hh import hh_collect_stats
from sj import sj_collect_stats


def format_stats_output(stats: dict, title: str = None) -> str:
    table_content = [
        ["Язык программирования", "Вакансий найдено",
         "Вакансий обработано", "Средняя зарплата"],
    ]

    for language, vacancies in stats.items():
        table_content.append([
            language,
            vacancies.get("vacancies_found"),
            vacancies.get("vacancies_processed"),
            vacancies.get("average_salary")
        ])

    table = AsciiTable(table_content, title=title)

    return table.table


def main() -> None:
    load_dotenv()

    languages = [
        "python",
        "java",
        "js",
        "ruby",
        "php",
        "c++",
        "c#",
        "go",
        "1c"
    ]

    sj_secret_key = os.environ.get("SJ_SECRET_KEY")

    hh_stats = {}
    sj_stats = {}

    for language in languages:
        try:
            hh_stats.update(hh_collect_stats(language))
            sj_stats.update(sj_collect_stats(sj_secret_key, language))
        except rq.exceptions.HTTPError as http_error:
            print(f"Ошибка соединения с сервером:\n{http_error}")

    print(format_stats_output(hh_stats, title="HeadHunter Moscow"), end="\n\n")
    print(format_stats_output(sj_stats, title="Superjob Moscow"))


if __name__ == "__main__":
    main()
