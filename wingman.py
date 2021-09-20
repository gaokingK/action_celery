import time

from celery_main import app
#
# """
# 任务注册后，使用原有的函数名还能正常调用函数吗？ 是可以的
# """
# @app.task
# def func1(param1):
#     print("param is [%s]" % param1)
#     time.sleep(3)
#     return param1

"""
打破链式操作是什么意思呢、按着教程上的代码运行一下试试
在对象中和在函数中有区别吗？

from celery import current_app

@current_app.task
def func1(param1):
    print("param is [%s]" % param1)
    time.sleep(3)
    return param1

class Scheduler(object):
    def __init__(self):
        self.app = app  # 这样也是可以的，可能是不提倡
s = Scheduler()
"""


"""
被绑定的任务的第一个参数总是任务实例?
这个任务怎么调用呢? 
为什么这个task能导入,却不能@task装饰任务呢?
"""
from celery_main import app
from celery import task
@app.task(band=True)
def func1(self, x, y):
    print(self.request.id)
