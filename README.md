# ACDS_ai_chat

This is the repo of ai chat engine in ACDS system.

Template configuration `config.cfg`:

```python
LOGGER_FORMAT = '[%(asctime)s] [%(name)s] [%(levelname)s]  %(message)s'
LOGGER_LEVEL = 20     ## CRITICAL=50, ERROR=40, WARNING=30, INFO=20, DEBUG=10, NOTSET=0

DATABASE = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "password",
    "database": "acds_chat",
}
```
