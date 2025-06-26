# Async FastAPI + Redis

##  Описание

Проект реализует асинхронный REST API с использованием FastAPI и Redis.  
Функциональность включает:
- POST `/process_data/` — приём произвольного JSON, запрос к внешнему API `https://catfact.ninja/fact` и возврат объединённого ответа.
- GET `/process_data/history/` — просмотр последних записей истории запросов и ответов из Redis.

---

## Запуск проекта

### 1. Собрать и запустить:

```bash
docker-compose up --build
```

### 2. Остановить и удалить контейнеры:

```bash
docker-compose down
```

---
## 📚 Документация API
Открыть Swagger: [http://localhost:8080/docs](http://localhost:8080/docs)

