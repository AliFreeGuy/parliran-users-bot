
from celery import Celery
from celery.schedules import crontab
import redis
from os.path import abspath, dirname
import sys
import requests
from pyrogram import Client
import time
from bs4 import BeautifulSoup
import yt_dlp
import os

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

app.conf.task_queues = {
    'downloader_queue': {
        'exchange': 'downloader',
        'exchange_type': 'direct',
        'binding_key': 'downloader'
    },
    
}

@app.task(name='tasks.checker', bind=True, default_retry_delay=1, queue='downloader_queue')
def checker(self):

    response = requests.get(config.WEB_URL)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        links = soup.find_all('a')

        for link in links:
            date = link.get('href')
            if date.endswith('/'):
                full_url = config.WEB_URL + date
                date_response = requests.get(full_url)
                if date_response.status_code == 200:
                    date_soup = BeautifulSoup(date_response.text, 'html.parser')
                    video_links = date_soup.find_all('a')

                    for video_link in video_links:
                        video_name = video_link.get('href')
                        if not video_name.endswith('_none.mp4'):
                            if video_name != 'd608ff0f-1e84-456a-a4fa-eb385149cc45.mp4' :
                                video_url = full_url + video_name
                                records_data = video_name.split('_')
                                rec_date = records_data[0]
                                start_time = records_data[1]
                                end_time = records_data[2].replace('.mp4' , '')
                                if not cache.redis.exists(f'recorder:{video_name}'):
                                    data = {
                                        'url' : video_url ,
                                        'date'  : rec_date , 
                                        'start_time' : start_time , 
                                        'end_time' : end_time ,
                                        'id' : f'recorder:{video_name}'
                                    }
                                    downloader.delay(data)
                                


                else:
                    print(f"Failed to retrieve data for {full_url}. Status code: {date_response.status_code}")
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")




@app.task(name='tasks.downloader', bind=True, default_retry_delay=1, queue='downloader_queue')
def downloader(self , data ):
    time.sleep(2)
    print(data)

    if not os.path.exists('files'):
        os.makedirs('files')

    folder_path = os.path.abspath('files')
    file_path = f'{folder_path}/{data["id"].replace("recorder:" ,"" )}'
    
    ydl_opts = {
        'format': 'best',
        'outtmpl': 'files/%(title)s.%(ext)s',
    }


    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([data['url']])

    
    if config.DEBUG =='True':
        bot = Client('dl-task', api_id=config.API_ID, api_hash=config.API_HASH, bot_token=config.BOT_TOKEN, proxy=config.PROXY)
    else:
        bot = Client('dl-task', api_id=config.API_ID, api_hash=config.API_HASH, bot_token=config.BOT_TOKEN)

    
    with bot : 
        caption = f'ضبط صحن علنی مجلس : {data["date"]}\nساعت شروع : {data["start_time"]}\nساعت پایان : {data["end_time"]}'
        vid_data = bot.send_video(chat_id=config.BACKUP_CHANNEL , video=file_path  , caption=caption)
        print(vid_data)

    
































#celery -A tasks worker --beat -Q downloader_queue --concurrency=1 -n downloader_worker@%h
#celery -A tasks worker -Q uploader_queue --concurrency=1 -n uploader_worker@%h




























