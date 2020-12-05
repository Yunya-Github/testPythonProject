
from celery import Celery

# 加载django环境
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "luffyapi.settings.dev")
django.setup()

broker='redis://127.0.0.1:6379/1'  #broker任务队列
backend='redis://127.0.0.1:6379/2'   # 结构存储，执行完的结果存在这

app=Celery(__name__,broker=broker,backend=backend,include=['celery_task.home_task',])


# 执行定时任务
# 时区
app.conf.timezone = 'Asia/Shanghai'
# 是否使用UTC
app.conf.enable_utc = False

# 任务的定时配置
from datetime import timedelta
from celery.schedules import crontab
app.conf.beat_schedule = {
    'add-task': {
        'task': 'celery_task.home_task.banner_update',
        'schedule': timedelta(seconds=30),
        # 'schedule': crontab(hour=8, day_of_week=1),  # 每周一早八点
        # 'args': (300, 150),
    }
}

# 一定要启动beat
# celery beat -A celery_task -l info