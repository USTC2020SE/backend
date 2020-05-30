# README

## 部署

* 前提环境

  |         服务          |     版本     |
  | :-------------------: | :----------: |
  |        Python         |  3.7或更高   |
  |         MySQL         |  8.0或更高   |
  | Django REST framework | 3.11.0或更高 |
  |     django-filter     |    2.2.0     |
  |       drf-yasg        |    1.17.1    |

1. MySQL配置

   请将 MySQL 的 root 用户密码设置为 root ，并运行以下指令以完成数据库的创建：

   ```mysql
   drop database backend; -- 如果您的数据库中已有名为'backend'的数据库，请备份数据并运行此语句
   create database backend;
   ```

2. 安装所有依赖
   
   请使用如下语句根据 requirements.txt 来安装所有依赖。（请注意：该依赖文件中可能含有目前阶段并不使用，但项目后续需要使用的条目）
   
   如果您没有使用 Virtualenv，推荐在 venv/ 下创建您的环境。本项目使用 Python 3。
   
   ```bash
   pip install -r requirements.txt
   ```
   
   > 在安装依赖 mysqlclient 时，您可能需要执行如下操作：
     ```bash
     sudo apt install default-libmysqlclient-dev
     ```
     否则可能会遇到无法找到 `mysql_config` 的错误。
   
3. Django REST framework 配置

   请在项目根目录下运行以下语句，完成 Django REST framework的配置：

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   python manage.py runserver
   ```

至此，项目配置完毕。

## 端口列表

请在`/docs/`端口查看所有端口的使用说明。对于模型属性的说明，可以查看模型文件中的注释。

## 说明

目前的后端拥有几个基本表格和对应表格上原始的CRUD操作。要使用并修改后端，请了解以下操作：

- 如何修改模型定义并实现各式各样的约束
- 如何调用端口对数据进行CRUD操作
- 如何重写序列化器下的方法以满足数据修改的要求
- 如何重写视图下的方法以满足调用端口的要求
- 如何修改路由以修改访问视图的方式

您可能需要参阅以下文档：

[Django文档](https://docs.djangoproject.com/en/3.0/)

[DRF文档](https://www.django-rest-framework.org/)

[django-filter文档](https://django-filter.readthedocs.io/en/stable/index.html)