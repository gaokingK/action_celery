task_serializer = 'json'
accept_content = ['json']  # Ignore other content
result_serializer = 'json'
timezone = 'Europe/Oslo'  # 设置时区
imports = ["tasks"]  # 配置导入的模块,和include一样 导入有任务的模块, worker响应对应的任务

# concurrency为同时处理任务的进程数量, 默认为当前cpu核数, 如果是高I/O,可以增加并发数量
com = 'celery worker -c num'
