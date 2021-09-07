import time
from celery_main import Celery


app = Celery('hello_celery',
             backend='redis://localhost',  # 配置后端, 为了使用任务调用后返回的对象获取任务的结果
             broker="amqp://localhost")

# 从配置文件中加载配置
# app.config_from_object("celeryconfig")
# 加载配置更常用的方式
app.conf.update(
    task_serializer='json',
    accept_content=['json'],  # Ignore other content
    result_serializer='json',
    timezone='Europe/Oslo',
    enable_utc=True,
    # 设置任务执行速率
    # 也可以在运行时新起终端运行命令控制 celery -A tasks control rate_limit tasks.add 10/m
    task_annotations={
        'tasks.add': {'rate_limit': '10/m'}
    },
    task_ignore_result=False,  # 为True会导致res.status一直是pending
)


@app.task
def add(x, y):
    time.sleep(5)
    res = x + y
    print("ok......")
    assert res > 5
    return res

# 先执行worker celery -A hello_celery worker --loglevel=info # hello_celery 是文件名
# 调用任务 add.delay(args) 会将所有参数都作为add的入参
# 任务add 会被worker处理
# 如果配置了后端, 调用任务会返回一个AsyncResult 实例, 这个实例的方法get()/status/ready()/
# 如果后端使用资源进行了资源存储,必须针对调用任务返回的每一个实例调用get()或者forget(), 进行释放资源
