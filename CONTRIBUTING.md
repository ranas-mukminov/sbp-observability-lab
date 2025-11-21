# Contributing to sbp-observability-lab

## Development flow

1. Следуем TDD: сначала пишем юнит-тесты в `tests/`, затем реализуем код.
2. Перед каждым пушем/PR запускаем:
   - `./scripts/lint.sh`
   - `./scripts/dev_run_all_tests.sh`
   - `./scripts/security_scan.sh`
3. Все найденные Codex Code Review замечания исправляем до merge.

## Codex Code Review

- В каждом PR должен быть запущен Codex review (автоматически или вручную).
- Для ручного запуска добавьте комментарий в PR:

```
@codex review
```

- Чтобы сфокусироваться на безопасности:

```
@codex review for security regressions
```

Codex-review не заменяет человеческий review, но является обязательным фильтром.
