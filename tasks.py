import time
from celery import Celery


app = Celery('tasks',
             backend='redis://localhost',
             broker="amqp://localhost")


@app.task
def add(x, y):
    time.sleep(5)
    res = x + y
    print("ok....")
    assert res > 5
    return res

