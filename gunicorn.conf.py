import os

bind = "0.0.0.0:8000"
workers = int(os.environ.get("WEB_CONCURRENCY", 3))
timeout = 120
accesslog = "-"
errorlog = "-"
loglevel = "info"
