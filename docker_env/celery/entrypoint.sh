#!/bin/sh
celery -A application.celery beat --loglevel=info   
celery -A application.celery worker -c 10 -P gevent --loglevel=info