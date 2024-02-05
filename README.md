# Сравнение вакансий программистов с сайтов [HeadHunter](https://hh.ru/) и [Superjob](https://www.superjob.ru/)

Скрипт, вычисляющий средние зарплаты программистов для разных языков программирования, путём анализа вакансий на сайтах [hh.ru](https://hh.ru/) и [superjob.ru](https://www.superjob.ru/)

## Установка

1. Установите [Python3](https://www.python.org/) и все необходимые зависимости с помощью

```
pip install -r requirements.txt
```

2. Получите `Secret key` для [Superjob API](https://api.superjob.ru/) и разместите его в файле `.env`, расположенном в одной директории с файлами скрипта следующим образом:

```
SJ_SECRET_KEY={secret_key}
```

`{secret_key}` - ваш Secret key для [Superjob API](https://api.superjob.ru/).

## Использование

Запустите скрипт с помощью

```
python3 main.py
```

<details>
  <summary>Пример вывода скрипта</summary>
  <img src="https://github.com/lypavel/dvmn-language_salary/assets/157053921/6ded61a0-8e55-4c47-aa45-606d4d82f229">
</details>

***
Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).
