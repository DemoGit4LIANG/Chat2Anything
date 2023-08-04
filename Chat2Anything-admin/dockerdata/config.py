import logging
from urllib.parse import quote_plus as urlquote

from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore


class BaseConfig:
    DEBUG = True
    HOST = '127.0.0.1'
    PORT = 5000

    SUPERADMIN = 'system'

    SYSTEM_NAME = 'Pear Admin'
    # 主题面板的链接列表配置
    SYSTEM_PANEL_LINKS = [
        {
            "icon": "layui-icon layui-icon-auz",
            "title": "官方网站",
            "href": "http://www.pearadmin.com"
        },
        {
            "icon": "layui-icon layui-icon-auz",
            "title": "开发文档",
            "href": "http://www.pearadmin.com"
        },
        {
            "icon": "layui-icon layui-icon-auz",
            "title": "开源地址",
            "href": "https://gitee.com/Jmysy/Pear-Admin-Layui"
        }
    ]

    UPLOADED_PHOTOS_DEST = 'static/upload'
    UPLOADED_FILES_ALLOW = ['gif', 'jpg']
    UPLOADS_AUTOSERVE = True

    # JSON配置
    JSON_AS_ASCII = False

    SECRET_KEY = "pear-system-flask"

    # redis配置
    REDIS_HOST = "127.0.0.1"
    REDIS_PORT = 6379

    # mysql 配置
    MYSQL_USERNAME = "root"
    MYSQL_PASSWORD = "123456"
    MYSQL_HOST = "172.10.1.31"
    MYSQL_PORT = 3306
    MYSQL_DATABASE = "PearAdminFlask"

    # mysql 数据库的配置信息
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{MYSQL_USERNAME}:{urlquote(MYSQL_PASSWORD)}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}?charset=utf8mb4"

    # 默认日志等级
    LOG_LEVEL = logging.WARN
    #
    MAIL_SERVER = 'smtp.qq.com'
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_PORT = 465
    MAIL_USERNAME = '123@qq.com'
    MAIL_PASSWORD = 'XXXXX'  # 生成的授权码
    MAIL_DEFAULT_SENDER = MAIL_USERNAME

    # 設置 APSCHEDULER 參數
    SCHEDULER_API_ENABLED = False
    SCHEDULER_JOBSTORES: dict = {
        'default': SQLAlchemyJobStore(
            url=f'mysql+pymysql://{MYSQL_USERNAME}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}')
    }
    SCHEDULER_EXECUTORS: dict = {
        'default': ThreadPoolExecutor(20)
    }
    SCHEDULER_JOB_DEFAULTS: dict = {
        'coalesce': False,
        'max_instances': 3
    }

    # 插件配置
    PLUGIN_ENABLE_FOLDERS = ["helloworld"]

    # 配置多个数据库连接的连接串写法示例
    # HOSTNAME: 指数据库的IP地址、USERNAME：指数据库登录的用户名、PASSWORD：指数据库登录密码、PORT：指数据库开放的端口、DATABASE：指需要连接的数据库名称
    # MSSQL:    f"mssql+pymssql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=cp936"
    # MySQL:    f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8"
    # Oracle:   f"oracle+cx_oracle://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}"
    # SQLite    "sqlite:/// database.db"
    # Postgres f"postgresql+psycopg2://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}"
    # Oracle的第二种连接方式
    # dsnStr = cx_Oracle.makedsn({HOSTNAME}, 1521, service_name='orcl')
    # connect_str = "oracle://%s:%s@%s" % ('{USERNAME}', ' {PASSWORD}', dsnStr)

    #  在SQLALCHEMY_BINDS 中设置：'{数据库连接别名}': '{连接串}'
    # 最后在models的数据模型class中，在__tablename__前设置        __bind_key__ = '{数据库连接别名}'  即可，表示该数据模型不使用默认的数据库连接，改用“SQLALCHEMY_BINDS”中设置的其他数据库连接
    #  SQLALCHEMY_BINDS = {
    #    'testMySQL': 'mysql+pymysql://test:123456@192.168.1.1:3306/test?charset=utf8',
    #    'testMsSQL': 'mssql+pymssql://test:123456@192.168.1.1:1433/test?charset=cp936',
    #    'testOracle': 'oracle+cx_oracle://test:123456@192.168.1.1:1521/test',
    #    'testSQLite': 'sqlite:///database.db
    # }

