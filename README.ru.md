# sbp-observability-lab (русская версия)

Лаборатория наблюдаемости для интеграций с СБП. Содержит:
- парсеры логов (NGINX/JSON/CSV);
- лёгкий HTTP-прокси для подсчёта запросов;
- Prometheus-экспортер и готовые Grafana-дашборды;
- AI-слой для человеко-читаемых отчётов.

## Быстрый старт

1. Установите зависимости и пакет:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

2. Запустите экспортер:

```bash
sbp-observability run-exporter --port 8000
```

3. Импортируйте дашборды из `grafana/dashboards` в Grafana.

4. Для генерации отчёта:

```bash
sbp-observability generate-weekly-report examples/logs/sbp_gateway_json_sample.log
```

## Безопасность и ограничения

- В репозитории только синтетические примеры.
- Нельзя хранить реальные платежные данные, ПДн, ключи/сертификаты.
- Интеграция с боем выполняется на риск пользователя с учётом требований закона и договоров.
