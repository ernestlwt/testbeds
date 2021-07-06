from flask import current_app
from celery import Celery
import time


celery = Celery(__name__,
        backend='redis://localhost:6379/0',
        broker='redis://localhost:6379/0')

@celery.task
def print_hello():
    time.sleep(5)
    print("hello")
    return "hello"

