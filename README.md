Описание: API для получения вопросов и ответов для викторины. Все вопросы взяты с API ```https://jservice.io/api/random```. Данный API представляет собой промежуточный слой, который сохраняет у себя в БД запрашиваемые вопросы.  
Для запуска данного приложения достаточно скачать репозиторий и, находясь в директории с ```docker-compose.yml``` файлом, запустить его командой в терминале ```docker-compose up -d```. Для остановки работы выполнить команду docker-compose down  
Приложение написано с применением асинхронного фреймворка FastAPI и AQLAlchemy   
Автоматическая документация по стандарту OpenAPI Specification будет доступна по url ```http://localhost/docs#/```   
Сам запрос делается на url ```http://localhost/quiz/<int>``` Где int- любое число больше 0  
Тип запроса только POST 
