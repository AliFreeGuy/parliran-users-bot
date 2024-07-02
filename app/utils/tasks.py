
from celery import Celery
from celery.schedules import crontab
import redis
from os.path import abspath, dirname
import sys


parent_dir = dirname(dirname(abspath(__file__)))
sys.path.insert(0, parent_dir)
import config
from utils import cache
from config import REDIS_DB, REDIS_HOST, REDIS_PORT

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True)
app = Celery('tasks', broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')
app.conf.timezone = 'UTC'

app.conf.update(
    task_serializer='json',
    result_serializer='json',
    accept_content=['json',],
    worker_concurrency=1,
    worker_prefetch_multiplier=1,
)

app.conf.beat_schedule = {
    'check-stream-every-10-seconds': {
        'task': 'tasks.checker',
        'schedule': 10.0,
    },
}

# تنظیم صف‌ها
app.conf.task_queues = {
    'downloader_queue': {
        'exchange': 'downloader',
        'exchange_type': 'direct',
        'binding_key': 'downloader'
    },
    
}

@app.task(name='tasks.checker', bind=True, default_retry_delay=1, queue='downloader_queue')
def checker(self):
    downloader.delay()



@app.task(name='tasks.downloader', bind=True, default_retry_delay=1, queue='downloader_queue')
def downloader(self):
    print('hi user mother fucker ')



#celery -A recorder_tasks worker --beat -Q downloader_queue --concurrency=1 -n downloader_worker@%h
#celery -A recorder_tasks worker -Q uploader_queue --concurrency=1 -n uploader_worker@%h




























