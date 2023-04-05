# Google-sheets-example
Приложение осуществляет мониторинг google sheets `https://docs.google.com/spreadsheets/d/1iuup5YG3dUID5KpTC8h0RTaULH2UeOQGs0MuQdq_08M/edit#gid=0` и записывает в базу данных. Доступ к web интерфейсу расположен по адресу `http://127.0.0.1:8000`. Также осуществляется отправка через телеграмм номеров заказов с истекшим сроком.

Перед запуском укажите в файле `.env` свой Телеграмм ID `TELEGRAM_ID=`. Укажите токен для телеграмм бота `TELEGRAM_TOKEN=` (либо можете использовать по умолчанию). Если вы будете использовать бот по умолчанию присоединитесь к нему в телеграмм `@GoogleSheetsExample_bot`.

Для запуска через докер используйте `docker-compose up --build postgres`. После готовности postgres `docker-compose up --build web`. При следующих запусках можно пользоваться одной командой `docker-compose up`.