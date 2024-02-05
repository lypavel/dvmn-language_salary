import requests as rq
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

    hh_stats = {}
    sj_stats = {}

    for language in languages:
        try:
            hh_stats.update(hh_collect_stats(language))
            sj_stats.update(sj_collect_stats(language))
        except rq.exceptions.HTTPError as http_error:
            print(f"Ошибка соединения с сервером: {http_error}")

    print(format_stats_output(hh_stats, title="HeadHunter Moscow"), end="\n\n")
    print(format_stats_output(sj_stats, title="Superjob Moscow"))


if __name__ == "__main__":
    main()
