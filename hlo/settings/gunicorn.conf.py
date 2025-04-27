import multiprocessing
wsgi_app = "hlo.wsgi:application"
bind = "0.0.0.0:8000"
workers = multiprocessing.cpu_count() * 2 + 1
accesslog = "-"
disable_redirect_access_to_syslog = True
errorlog = "-"
loglevel = "info"
