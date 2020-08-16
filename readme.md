### 天天基金净值爬取



#### 项目重点

1. Scrapy框架爬取
2. 重写下载中间件
3. 搭建UA池以及IP代理池



#### 项目结构

├── readme.md

└── spider_tianFund

  ├── scrapy.cfg

  └── spider_tianFund

​    ├── __init__.py

​    ├── __pycache__

​    │  ├── __init__.cpython-36.pyc

​    │  ├── items.cpython-36.pyc

​    │  ├── middlewares.cpython-36.pyc

​    │  ├── pipelines.cpython-36.pyc

​    │  └── settings.cpython-36.pyc

​    ├── items.py

​    ├── middlewares.py

​    ├── pipelines.py

​    ├── settings.py

​    └── spiders

​      ├── Fund.py

​      ├── __init__.py

​      └── __pycache__

​        ├── Fund.cpython-36.pyc

​        └── __init__.cpython-36.pyc