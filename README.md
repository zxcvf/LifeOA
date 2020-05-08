# LIFEOA

> A lightweight open source OA system
>
> by django-rest-framework 




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
```