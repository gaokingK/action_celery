### 结构
```angular2html
├── celeryconfig.py 从里面加载celery配置, 包括配置项的介绍
├── Readme.md
├── requestments.txt
├── hello_celery.py   上手celery
├── tasks.py 进阶使用
├── celery_main.py 进阶使用
└── wingman.py 作为容纳测试代码的文件

```
## [celery 上手](https://www.celerycn.io/ru-men/celery-chu-ci-shi-yong)
1. 安装celery
2. 写app，进行任务绑定（如果app和任务不在同一个py文件中，应该在app设置中导入任务所在模块）
## [celery 进阶](https://www.celerycn.io/ru-men/celery-jin-jie-shi-yong)

## 其他
1. #### 注册表 可以通过app.tasks查看
1. #### 任务注册的方式
    app.task装饰器进行任务注册, 会将任务注册到任务注册表中
1. #### 任务调用
   task_name.apply_async
   task_name.delay
1. #### 过滤配置，当打印配置时，过滤掉敏感信息
1. #### 时区
   内部和消息中的所有的时间和日期使用的都是 UTC 时区；当职程（Worker）收到消息时，例如倒计时设置，会将 UTC 时间转换为本地时间
1. #### 签名signature
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
1. CELERY_TRACE_APP 是干什么的，应用实例链被打破又是怎么一回事
1. 怎么看队列有哪些
1. 怎么通过id来查询任务的状态
1. 如果代码修改了,必须重启celery吗?看来好像是这样的
2. 进行资源释放了没有
3. ctrl+c退出的时候会把任务处理完了再退出, 但是会按好几次才能退出,可能是有几层
4. 配置项写错也不会报错
5. ##### 任务的status一直是pending的原因:
- 可能是app.task_ignore_result=True
6. celery app 这种文件的命名
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

## doc index 中文文档简单看了下， 用户指南做个记录，以后好找些, 看的过程中大概看一遍,理解的细看,不理解的就不强求
### 应用
- 主名称
    创建celery实例时定义的名字，可以用app.main 查看;
    进行任务注册后的任务名字
- 配置
    进行任务配置的几种方式
- 过滤配置
    当打印配置时，过滤掉敏感信息
- 懒加载
    没看懂，懒加载明明是调用的时候才运行，看它的解释也是这样的，结果就调用了一下就说展示了，elevated是代表什么我也不知道，反正就是一头雾水
- 打破链式操作 chain
    如果celery实例在一个py中，而用app的在另外一个py，把这个app给传递过去（传递的方式可以还是导入）再使用，这种用法就是app chain；
    from celery.app import current_app, app_or_default 来导入当前app，而不是从app定义的py中导入
     CELERY_TRACE_APP 这个环境变量说是可以在应用实例链被打破时抛出一个异常：不知道怎样才能打破
  - API 的发展
    介绍了调用任务的方式，从不用注册就可以任意调用，然后又是自定义TASK类然后在类中绑定任务，最后说这种模式会造成
    使用除pickle之外的序列化器非常困难，并且该功能在2.0中被删除，被任务装饰器取代
- 抽象任务
    怎么重写TASK类
    为什么要重写呢？重写了有什么用呢，示例中没看出来
  
### 任务
任务是由可调用对象创建出来的类, 任务承担两个角色, 任务被调用时候发送消息以及当worker收到这个消息时的行为
每一个任务类都有唯一的名称,消息中引用这个名称,并且被worker用来找到对应的执行函数
worker确认消息之前,不会从任务队列中删除该消息, worker被kill后,订阅的消息会传递到其他worker
默认行为是在worker执行处理消息之前确认消息
如果执行任务的子进程终止(通过调用sys.exit()的任务或通过信号)，即使启用了acks_late，职程（Worker）也会确认消息 原因是:
    我们假设系统管理员故意终止任务，不希望任务自动重启;
    重新分配任务失败的任务可能导致高频率的循环。

- 基础
    创建任务使用app.task装饰器; 设置选项:app.task(serializer='json')
    share_task 装饰器是干什么的?
    绑定的任务? bind bind 参数表示该函数绑是一个绑定方法，可以通过访问任务类型实例中的属性和方法
    装饰器的base参数可以指定继承的任务基类
- 任务名字
    在装饰器中使用name指定名字,默认的名字是模块名.函数名,最好的做法是将模块名称.自定义的名字
    任务的.name可以获得名字 如果add.name
    相对导入和自动命名兼容不是很好, 生成的名称不会匹配，可能会出现 NotRegistered 错误信息
    导入语句的写法会造成任务名字的不同,不想看
    app.gen_task_name() 进行修改默认的所有任务名称
- 任务请求
    app.Task.request 包含与当前执行任务相关的信息和状态。
    如任务id/status等
  
- 日志
    - 日志相关
    - 参数校验
        可以在装饰器中设置typing=False来关闭参数校验
      
    - 隐藏参数中的敏感信息
        可以重写位置参数和关键字参数在日志中的表现方式
      
- 重试
    app.Task.retry() 重新执行
    会发送与原始任务相同的ID发送一条消息，将该消息发送到原始任务的对列中
    当任务被重试时，也会被记录为一个任务状态，便于通过 result 实例来跟踪任务
    自定义重试延迟         
    自动重试已知异常 只重试某些特定的异常
  
- 选型列表 
    在任务装饰器里的配置选项
  
- 状态
    Celery 可以跟踪任务当前的状态信息。状态信息包含成功任务的结果，或执行失败任务的异常信息
    描述了一些状态
    结果后端:
        RPC 结果后端: 它实际上不存储信息, 只是作为消息发送,所以信息只能检索一次, 而且只能有启动任务的机器检索,
        俩个不同的进程获取的结果不同。但却适合需要实时状态更新信息的情况;可以使用 result_persistent 配置将结果信息转换为持久消息。
        数据库结果后端: 方便, 但使用数据库轮询获取任务状态信息会导致数据库压力很大，应该设置轮询的间隔时间;
        有些数据库使用默认的事务隔离级别，不适合轮询表以进行更改
    自定义状态
    创建可处理的异常
        使用 Pickle 作为序列化器时，引发不可拾取异常的任务将无法正常工作
  
- Semipredicates
    worker将任务包装到一个函数中,函数中记录了任务的最终状态。有许多异常向该函数发出信号，用于更改处理任务返回的方式。
    Ignore 信号的作用
    retry信号的作用
  
- 自定义任务类
    可以自定义任务类,
    这些任务类不会为每一个请求实例化,而是作为全局变量在任务注册表中注册,每一个进城只会调用一次init, 
    这种自定义类的使用场景如:资源缓存
    Handlers
        after_return 等函数,在任务完成或者某些状态后由worker调用
  
- 如何工作
    任务注册表
        所有定义的任务都在注册表中。注册表中包含任务名称和它们的任务类, 可以通过app.tasks查看 前面是任务名,后面是任务类
    任务被发送时, 实际的任务代码并没有被发送, 发送的其实是任务的名字, worker收到消息时, 会在任务注册表中查找任务名称并执行代码
    这意味着worker 和 客户端的代码应该相同
  
- 最佳实践 介绍一些最优配置
    存储结果会浪费资源和时间, 如果不关心任务结果, 可以在装饰器中设置ignore_result=True, 还有其他层面的配置忽略结果
    避免启动同步子任务 (是不是同步启动子任务?)
        因为让一个任务等待另外一个任务的结果是十分低效的,并且在工作池耗尽的时候,可能会导致死锁
        给出了解决办法: 将不同任务的signature进行链接，组成任务链来达成目的
        默认情况下，Celery不允许您在任务中运行同步子任务, 非要运行的时候可以加个参数
  
- 性能和策略
    颗粒度
        小颗粒度能增加并发量, 并且能够避免阻塞worker处理其他等待的任务
        但是颗粒度如果过小, 反而有很多坏处
        The book <<Art of Concurrency>> has a section dedicated to the topic of task granularity
    data locality
        最好的情况是数据就在内存中, 而如果处理的数据需要传输, 会降低处理效率
        如果数据需要很远的传输, 更好的办法是在那个地方再运行一个worker, 如果这不可行, 至少应该缓存经常使用的数据,或者预加载要处理的数据
        worker 之间共享数据的最简单办法是使用分布式缓存系统 like memcached
        The paper Distributed Computing Economics by Jim Gray is an excellent introduction to the topic of data locality.
    state
        由于 Celery 是一个分布式系统，你无法知道任务将在哪个进程或哪台机器上执行。 您甚至无法知道任务是否会及时运行。
        这意味着自从请求任务以来世界观可能已经改变，因此任务负责确保世界是它应该的样子；而不是调用者
        The ancient async sayings tells us that “asserting the world is the responsibility of the task”. 
        Another gotcha is Django model objects. They shouldn’t be passed on as arguments to tasks. 
        It’s almost always better to re-fetch the object from the database when the task is running instead, as 
        using old data may lead to race conditions.
    Database transactions
        django.db.transaction.atomic is decorator, that will commit the transaction when the view returns, or 
        roll back if the view raises an exception.
        ```python
  
        @transaction.atomic
        def create_article(request):
            article = Article.objects.create()
            expand_abbreviations.delay(article.pk)
            return HttpResponseRedirect('/articles/')
        # solution
            on_commit(lambda: expand_abbreviations.delay(article.pk))
        ```
        There’s a race condition if the task starts executing before the transaction has been committed; The 
        database object doesn’t exist yet!
        The solution is to use the on_commit callback to launch your Celery task once all transactions 
        have been committed successfully.

- Example
    让我们举一个真实的例子：一个博客，其中发布的评论需要过滤垃圾邮件。 创建评论时，垃圾邮件过滤器在后台运行，因此用户不必等待它完成。 
  
### diao