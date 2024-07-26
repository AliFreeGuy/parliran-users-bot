
from pyrogram.errors import UserNotParticipant
import jdatetime
import re
from utils.cache import cache
import jdatetime
import datetime
import arabic_reshaper
from bidi.algorithm import get_display



def convert_numbers_to_persian(text):
    english_to_persian = str.maketrans("0123456789", "۰۱۲۳۴۵۶۷۸۹")
    return text.translate(english_to_persian)


def convert_date_to_farsi(date_str):
    date_obj = jdatetime.date(*map(int, date_str.split('-')))
    days_of_week = ["شنبه", "یک‌شنبه", "دوشنبه", "سه‌شنبه", "چهارشنبه", "پنج‌شنبه", "جمعه"]
    day_of_week = days_of_week[date_obj.weekday()]
    months_of_year = ["فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور", "مهر", "آبان", "آذر", "دی", "بهمن", "اسفند"]
    month_name = months_of_year[date_obj.month - 1]
    final_str = f"{day_of_week} {date_obj.day} {month_name} {date_obj.year}"
    return final_str

def smtp_to_date(timestamp):
    gregorian_date = datetime.datetime.fromtimestamp(timestamp)
    jalali_date = jdatetime.datetime.fromgregorian(datetime=gregorian_date)
    
    year = jalali_date.year
    month = jalali_date.month
    day = jalali_date.day

    date_info = {
        "ym": f"{year}-{month:02}",
        "ymd": f"{year}-{month:02}-{day:02}",
        "full": jalali_date.strftime('%Y-%m-%d %H:%M:%S')
    }
    
    return date_info


def get_date_info(timestamp=None):
    if timestamp is None:now = jdatetime.datetime.now()
    else:now = jdatetime.datetime.fromtimestamp(timestamp)
    numeric_timestamp = int(now.timestamp())
    one_month_before = now - jdatetime.timedelta(days=30)
    one_month_after = now + jdatetime.timedelta(days=30)
    before_timestamp = int(one_month_before.timestamp())
    after_timestamp = int(one_month_after.timestamp())
    date_info = {
        "now_date": now.strftime("%Y-%m"),
        "now_smtp": numeric_timestamp,
        "before_date": one_month_before.strftime("%Y-%m"),
        "before_smtp": before_timestamp,
        "after_date": one_month_after.strftime("%Y-%m"),
        "after_smtp": after_timestamp
    }

    return date_info




async def join_checker(cli , msg , channels ):
   
    my_channels = []
    not_join = []
    for channel in channels :
        data = channel.split(' ')
        if len(data) == 2 :
            my_channels.append({'link' : data[0] , 'chat_id' : data[1]})
            
   
    for i in my_channels : 
        try :  
            data = await cli.get_chat_member(int(i['chat_id']), msg.from_user.id )
        except UserNotParticipant :
            not_join.append(i['link'])
            continue
        except Exception as e  :
            print(e)
            continue
    return not_join




async def alert(client ,call , msg = None ):
    try :
        if msg is None : await call.answer('خطا لطفا دوباره تلاش کنید', show_alert=True)
        else : await call.answer(msg , show_alert = True)
    except Exception as e : print('alert ' , str(e))
    
   