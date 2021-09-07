import time

from celery_main import app


@app.task
def add(x, y):
    print("ok......")
    return x + y + y


@app.task
def mul(x, y):
    time.sleep(5)
    return x * y


@app.task
def xsum(numbers):
    return sum(numbers)
