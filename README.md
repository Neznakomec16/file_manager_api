### Task

"Хранилище файлов с доступом по http"

Реализовать демон, который предоставит HTTP API для загрузки (upload) ,
скачивания (download) и удаления файлов.

Upload:
- получив файл от клиента, демон возвращает в отдельном поле http
response хэш загруженного файла
- демон сохраняет файл на диск в следующую структуру каталогов:
     store/ab/abcdef12345...
где "abcdef12345..." - имя файла, совпадающее с его хэшем.
/ab/  - подкаталог, состоящий из первых двух символов хэша файла.
Алгоритм хэширования - на ваш выбор.

Download:
Запрос на скачивание: клиент передаёт параметр - хэш файла. Демон ищет
файл в локальном хранилище и отдаёт его, если находит.

Delete:
Запрос на удаление: клиент передаёт параметр - хэш файла. Демон ищет
файл в локальном хранилище и удаляет его, если находит.


### Instalation 

Для установки предусмотрен Makefile

```
git clone https://github.com/Neznakomec16/file_manager_api && cd file_manager_api
make
```

Создание и получение токена

`make createsuperuser USERNAME='SOME_SUPERUSER' EMAIL='SOME_SUPERUSER@email.com'`

Чтобы получить доступ к админке 

`python3 manage.py changepassword SOME_SUPERUSER`


Для безопасности в среде окнужения следует определить `FILE_MANAGER_DJANGO_SECRET_KEY`

```
export FILE_MANAGER_DJANGO_SECRET_KEY="SOME_SECRET_KEY"
```

### Usage

Примеры использования API представлено в `mock/examples/requests.txt`