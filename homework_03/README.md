### Домашнее задание "Docker контейнер c веб-приложением"

#### Запуск
Для запуска необходимо собрать образ, затем запустить его
```
docker build -t homework_03 .
docker run -d homework_03
docker start {container_id}
```