import multiprocessing
import os

bind = f"0.0.0.0:{os.getenv('PORT', '5001')}"
workers = int(os.getenv('WEB_CONCURRENCY', multiprocessing.cpu_count() * 2 + 1))
threads = int(os.getenv('PYTHON_MAX_THREADS', '2'))
worker_class = 'gthread'
worker_connections = 1000
timeout = int(os.getenv('WEB_TIMEOUT', '120'))
keepalive = 5

accesslog = '-'
errorlog = '-'
loglevel = os.getenv('LOG_LEVEL', 'info')
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" (%(L)ss)'
