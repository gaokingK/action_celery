from celery import Celery

app = Celery("celery_main",
             broker="amqp://localhost",
             backend='redis://localhost',
             # include=["tasks"],
             )

app.conf.update(
    result_expires=3600,
    imports=["tasks",
             "wingman"],
    # task_routes={
    #     "tasks.add": {"queue": "hipri"}
    # },
)


if __name__ == '__main__':
    app.start()
