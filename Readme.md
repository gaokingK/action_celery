### 结构
```angular2html
├── celeryconfig.py 从里面加载celery配置, 包括配置项的介绍
├── Readme.md
├── requestments.txt
├── hello_celery.py   上手celery
├── tasks.py 进阶使用
└── celery_main.py 进阶使用

```
## [celery 上手](https://www.celerycn.io/ru-men/celery-chu-ci-shi-yong)
1. 安装celery
2.
## [celery 进阶](https://www.celerycn.io/ru-men/celery-jin-jie-shi-yong)

## 其他
1. #### 时区
   内部和消息中的所有的时间和日期使用的都是 UTC 时区；当职程（Worker）收到消息时，例如倒计时设置，会将 UTC 时间转换为本地时间
1. #### 签名
   类似于闭包.签名通过一种方式进行封装任务调用的参数以及执行选项，便于传递给他的函数，甚至通过序列化通过网络传送。
   ```
   res = add.signature((2, 2), countdown=10)
   res.apply_async() 可以用这个签名调用
   # 快捷方式 但这种支支持add的参数,其他的参数在调用时传入
   res = add.s(2,2)
   # 生成签名的时候可以不写函数的入参,在调用时在传入参数,如果如果定义签名时传入一个参数a, 调用时又传入一个参数b那么add接受的参数是(b,a)
   ```
1. #### 原语
   类似于python中的reduce/map/
1. #### AsyncResult的方法
   get();failed();successful();ready();status(state);
   对于大量的任务来说，保存返回内容不是非常有用的，所以该默认值是一个比较合理的。
   另外，结果后端不是用于监控任务以及职程（Worker），Celery 有专用的事务消息来进行监控.
1. #### queue
    - Queues 为职程（Worker）任务队列，可以告诉职程（Worker）同时从多个任务队列中进行消费。
      通常用于将任务消息路由到特定的职程（Worker）、提升服务质量、关注点分离、优先级排序的常用手段
    - 队列如果不存在，也是能起来的
    ```
    app.conf.update(
    task_routes = {
        "task_moude_path.func_name" : {"queue": "queue_name"}
       }
    )
    ```
    - 多个队列的时候，分配的权重是一样的
1. #### [celery 所需的brokers](https://www.celerycn.io/ru-men/zhong-jian-ren-brokers)
- RabbitMQ 和 Redis

1. #### 创建队列、对应的交换机、怎么为不同的task指派不同的队列、apply_async()

## 问题
1. 怎么看队列有哪些
1. 怎么通过id来查询任务的状态
1. 如果代码修改了,必须重启celery吗?看来好像是这样的
2. 进行资源释放了没有
3. ctrl+c退出的时候会把任务处理完了再退出, 但是会按好几次才能退出,可能是有几层
4. 配置项写错也不会报错
5. ##### 任务的status一直是pending的原因:
- 可能是app.task_ignore_result=True
6. celery 这种文件的命名
7. 初始化celery实例时的名字
8. ###### PermissionError: [Errno 13] Permission denied: '/var/run/celery'
    - ln -s /run/shm /dev/shm 没有用
    - mkdir -p /var/run/celery;chown -R huawei:huawei /var/run/celery
9. celery mutli 不存储有关worker的信息, 可以通过ps -ef |grep celery 来查看名字

## celery 命令的参数
1.  -A 后面接module; -app 参数可也指定运行的 Celery 应用程序实例，格式必须为 module.path:attribute
    会循环搜索包;
2. -Q queue_name1[,queue_name2] 指定任务队列 如果队列不存在，会创建

## apply_async参数
- queue: 指定任务放入的消息队列,如果这个消息队列没有定义,那么会没人消费,但不会报错
- countdown=10

## celery 监控
- `celery [-A celery_main ]inspect active [--destination=celery@example.com]` 查看当前处理的任务 
    主机名可以在任务起来的时候查看或者不加 des选项中选择一个
    -A 选项也是可选
- `celery status`  查看集群状态

## celery 优化
默认的配置适合大量的短任务和较少的长任务，没有针对吞吐量进行优化
- 如果使用的中间人是 RabbitMQ，可以将换成 librabbitmq 模块（通过 C 语言实现的AMQP客户端）
    `pip install librabbitmq`
