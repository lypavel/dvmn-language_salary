def predict_salary(salary_from, salary_to) -> int:
    if not salary_from and salary_to:
        return salary_to * 0.8
    elif salary_from and not salary_to:
        return salary_from * 1.2
    else:
        return (salary_from + salary_to) / 2


def count_average_salary(salaries: list) -> int:
    return round(sum(salaries) / len(salaries))
