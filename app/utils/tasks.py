
from celery import Celery
from celery.schedules import crontab
import redis
from os.path import abspath, dirname
import sys
import requests
from pyrogram import Client
import jdatetime
import time
from PIL import Image, ImageDraw, ImageFont
from bs4 import BeautifulSoup
import yt_dlp
import os

parent_dir = dirname(dirname(abspath(__file__)))
sys.path.insert(0, parent_dir)
import config
from utils import cache
from config import REDIS_DB, REDIS_HOST, REDIS_PORT
from utils.utils import convert_numbers_to_persian

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




def convert_date_to_farsi(date_str):
    date_obj = jdatetime.date(*map(int, date_str.split('-')))
    days_of_week = ["شنبه", "یک‌شنبه", "دوشنبه", "سه‌شنبه", "چهارشنبه", "پنج‌شنبه", "جمعه"]
    day_of_week = days_of_week[date_obj.weekday()]
    months_of_year = ["فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور", "مهر", "آبان", "آذر", "دی", "بهمن", "اسفند"]
    month_name = months_of_year[date_obj.month - 1]
    final_str = f"{day_of_week} {date_obj.day} {month_name} {date_obj.year}"
    return final_str

def draw_bold_text(draw, text, position, font, fill):
    offsets = [(0, 0), (1, 0)]
    for offset in offsets:
        x_offset, y_offset = offset
        draw.text((position[0] + x_offset, position[1] + y_offset), text, font=font, fill=fill)

def create_thumbnail(data):
    image = Image.open("/root/record-users/parliran-users-bot/app/utils/img.jpg")
    draw = ImageDraw.Draw(image)
    font_1 = ImageFont.truetype("vazir.ttf", 20)
    font_2 = ImageFont.truetype("vazir.ttf", 16)

    date_text = convert_date_to_farsi(data["date"])
    date_position = (100, 95)
    draw_bold_text(draw, date_text, date_position, font_1, "white")

    start_time_parts = data["start_time"].split("-")
    formatted_start_time = f'{start_time_parts[0]}:{start_time_parts[1]}'
    end_time_parts = data["end_time"].split("-")
    formatted_end_time = f'{end_time_parts[0]}:{end_time_parts[1]}'
    other_text = f'از ساعت {formatted_start_time} تا {formatted_end_time}'
    other_position = (120, 148)
    draw_bold_text(draw, other_text, other_position, font_2, "black")

    thumbnail_path = "/root/record-users/parliran-users-bot/app/utils/img_with_text.jpg"
    image.save(thumbnail_path)
    return thumbnail_path











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
                        if not video_name.endswith('_none.mp4') and not video_name.endswith('_none.mkv'):
                            if video_name != 'd608ff0f-1e84-456a-a4fa-eb385149cc45.mp4' :
                                video_url = full_url + video_name
                                records_data = video_name.split('_')
                                rec_date = records_data[0]
                                start_time = records_data[1]
                                end_time = records_data[2].replace('.mp4' , '').replace('.mkv', '')
                                
                                if not cache.redis.exists(f'recorder:{video_name}'):
                                    print('@@@@@@@@@@@@@@@@@@@@@@2viddo is @@@@@@@@@@@@@@@@@@@@@@@@@@@@2')
                                    data = {
                                        'url' : video_url ,
                                        'date'  : rec_date , 
                                        'start_time' : start_time , 
                                        'end_time' : end_time ,
                                        'id' : f'recorder:{video_name}'
                                    }
                                    downloader.delay(data)
                                else : print('..................... video already ..........................')
                                


                else:
                    print(f"Failed to retrieve data for {full_url}. Status code: {date_response.status_code}")
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")



@app.task(name='tasks.downloader', bind=True, default_retry_delay=1, queue='downloader_queue')
def downloader(self, data):
    time.sleep(2)
    print(data)

    if not os.path.exists('files'):
        os.makedirs('files')

    folder_path = os.path.abspath('files')
    file_path = f'{folder_path}/{data["id"].replace("recorder:", "")}.mp4'
    
    ydl_opts = {
        'format': 'best',
        'outtmpl': file_path,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([data['url']])

    thumbnail_path = create_thumbnail(data)

    if config.DEBUG == 'True':
        bot = Client('uploader', api_id=config.API_ID, api_hash=config.API_HASH, bot_token=config.BOT_TOKEN, proxy=config.PROXY)
    else:
        bot = Client('uploader', api_id=config.API_ID, api_hash=config.API_HASH, bot_token=config.BOT_TOKEN)

    with bot:
        print('... upload starting ... ')
        date_parts = data["date"].split("-")
        formatted_date = f'{date_parts[0]}/{date_parts[1]}/{date_parts[2]}'
        start_time_parts = data["start_time"].split("-")
        formatted_start_time = f'{start_time_parts[0]}:{start_time_parts[1]}'
        end_time_parts = data["end_time"].split("-")
        formatted_end_time = f'{end_time_parts[0]}:{end_time_parts[1]}'
        caption = f'🎥 ضبط صحن علنی مجلس : {formatted_date}\nساعت شروع : {formatted_start_time}\nساعت پایان : {formatted_end_time}\n\n✅ @AkhbarMajles_ir | اخبار مجلس'
        caption = convert_numbers_to_persian(caption)
        vid_data = bot.send_video(chat_id=config.BACKUP_CHANNEL, video=file_path, caption=caption, thumb=thumbnail_path)
        vid_data.copy(config.PARLIRAN_CHANNEL)
        data['file_id'] = vid_data.video.file_id
        data['mid'] = vid_data.id
        cache.redis.hmset(data['id'], data)
        try:
            os.remove(file_path)
        except OSError as e:
            print(f'ERROR : {file_path} - {str(e)}')

        try:
            os.remove(thumbnail_path)
        except OSError as e:
            print(f'ERROR : {thumbnail_path} - {str(e)}')






























#celery -A tasks worker --beat -Q downloader_queue --concurrency=1 -n downloader_worker@%h



#celery -A tasks worker -Q uploader_queue --concurrency=1 -n uploader_worker@%h




























