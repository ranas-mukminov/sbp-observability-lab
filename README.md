# sbp-observability-lab

## English (short)

SBP observability lab provides log parsers, lightweight proxy, Prometheus exporter, Grafana dashboards, and AI-generated reports for Russian Faster Payments System (SBP) integrations.

## Русский (подробно)

### Что это

Лаборатория наблюдаемости для интеграций с СБП: парсеры логов (NGINX/JSON/CSV), лёгкий HTTP-прокси, Prometheus-экспортер с метриками и готовые Grafana-дашборды. Weekly-отчёты на русском помогают бизнесу понимать, что происходит с платежами.

### Что умеет

- Считает latency/ошибки по банкам и каналам.
- Фиксирует всплески ошибок и таймаутов.
- Выдаёт «пятничный отчёт» в Markdown.

### Быстрый старт

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .

sbp-observability parse-logs examples/logs/sbp_gateway_nginx_sample.log --format nginx
sbp-observability run-exporter --port 8000
```

Импортируйте дашборды из каталога `grafana/dashboards` в вашу Grafana, настройте Prometheus на scrape `/metrics` вашего экспортера.

### Безопасность

- В примерах используются синтетические логи.
- Запрещено хранить реальные ПДн и реквизиты в репозитории.
- Рекомендуется анонимизировать поля до передачи в парсеры/экспортер.

## Профессиональные услуги – run-as-daemon.ru

Проект развивается инженером DevOps/DevSecOps с сайта [run-as-daemon.ru](https://run-as-daemon.ru).

Если вашей компании нужно:
- навести порядок в логах и метриках интеграций с СБП;
- понять, почему платежи иногда «висят» или массово отказываются;
- получить дашборды и отчёты «как в банке»,

вы можете заказать:
- аудит существующей интеграции СБП;
- внедрение стека наблюдаемости на базе этого репозитория (Prometheus + Grafana);
- настройку weekly-отчётов и SLA-мониторинга.

### Дисклеймер

Проект не является официальным продуктом Банка России, НСПК, банков или платёжных систем, не предоставляет платёжные услуги и не освобождает от обязанности соответствовать требованиям регуляторов.
