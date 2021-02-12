# foodgram-project
Проект создан в качестве дипломного, при обучении в Яндекс.Практикум

- Сайт доступен по адресу [http://84.252.128.25/]

## Запуск и миграция базы данных
`docker-compose up`
    затем
`docker exec -it <CONTAINER ID> bash`
    затем
`python manage.py migrate`
`python3 manage.py shell`
    выполнить в открывшемся терминале:
`>>> from django.contrib.contenttypes.models import ContentType`
`>>> ContentType.objects.all().delete()`
`>>> quit()`
    затем
`python manage.py loaddata dump.json`

[http://84.252.128.25/]: http://84.252.128.25/
