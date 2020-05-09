# LIFEOA

> A lightweight open source OA system
>
> by django-rest-framework 


API接口文档 {host}/swagger/

`LifeOA/settings_local.py`
``` 
DEBUG = True  # 是否开启DEBUG模式，本地开发可开启，正式环境则关闭
CSRF_ENABLE = False  # 是否开启CSRF验证，本地开发可开启，正式环境则关闭

DATABASES = {
    'default': {
        'ENGINE': '',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '3306',
        'OPTIONS': {
            'charset': 'utf8mb4',
        },
    }
}

META_MSG = {
    'name': 'life-OA',
    'version': 'v0.0.1',
    'powered-by': 'life.li'
}

EMAIL_HOST = ''  # 发送邮件配置项
EMAIL_PWD = ''
EMAIL_SERVER = ''
EMAIL_PORT = ''


REDIS = ''  # celery使用的redis连接
```


本地启动服务

`python manage.py runserver`

本地启动celery

`celery -A LifeOA worker -l info --pool=solo`

