# Run project
#### For build and up project use:
    make start
#### For start tests in docker container use:
    python runtests.py
#### For build docker image run:
    make build
#### For up docker container run:
    make up
#### For down docker container run:
    make down


# Задание:
Реализуйте web-приложение для простого учета посещенных ссылок.
Приложение должно удовлетворять следующим требованиям.
- Приложение написано на языке Python версии ~> 3.7.
- Приложение предоставляет JSON API по HTTP.
- Приложение предоставляет два HTTP ресурса.
### Ресурс загрузки посещений:
#### Запрос 1
     POST /visited_links
     
     {
         "links": [
            "https://ya.ru",
            "https://ya.ru?q=123",
            "funbox.ru",
            "https://stackoverflow.com/questions/11828270/how-to-exit-the-vim-editor"
        ] 
     }

#### Ответ 1
    {
        "status": "ok"
    }

### Ресурс получения статистики:
#### Запрос 2
    GET /visited_domains?from=1545221231&to=1545217638
#### Ответ 2
    {
        "domains": [
            "ya.ru",
            "funbox.ru",
            "stackoverflow.com"
        ],
        "status": "ok"
    }

- Первый ресурс служит для передачи в сервис массива ссылок в POST-запросе. Временем их посещения считается время получения запроса сервисом.
- Второй ресурс служит для получения GET-запросом списка уникальных доменов, посещенных за переданный интервал времени.
- Поле status ответа служит для передачи любых возникающих при обработке запроса ошибок.
- Для хранения данных сервис должен использовать БД Redis.
- Код должен быть покрыт тестами.
- Инструкции по запуску должны находиться в файле README.
