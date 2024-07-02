from pyrogram import Client , filters
from utils.utils import  alert , get_date_info , smtp_to_date
from utils import text , btn 
from utils import filters as f
from pyrogram.types import InputMediaVideo
from utils import logger
from utils import cache
from config import ADMIN

@Client.on_message(filters.private & f.user_is_join ,group=1)
async def user_panel(client , message ):
    if message.text :
        if message.text == '/start' : 
            await start_manager(client , message)
        
        elif message.text == 'امار' : 
             await users_count(client ,message )





async def users_count(client , message ):
    if message.from_user.id == ADMIN : 
         counts  = len(cache.redis.keys(f'majles-user:*'))
         await client.send_message(chat_id = message.from_user.id , text = f'امار کاربران ربات : {str(counts)}')
        




async def start_manager(client, message ):
    data  = get_date_info()
    time = get_date_info()
    record_keys = cache.redis.keys(f'recorder:*')
    print(record_keys)
    now_records = []
    for record_date in record_keys:
        now = time['now_date'].replace('/' , '-')
        rdate = cache.redis.hget(record_date , 'date')[:-3].replace('/' , '-')
        if now == rdate:
                now_records.append(cache.redis.hget(record_date , 'date'))
    now_records = sorted(list(set(now_records)))
    await client.send_message(chat_id = message.from_user.id ,
                               text = text.records_lists(data) ,
                                 reply_markup = btn.parliran_lists_btn(data , now_records)
                                 )



@Client.on_callback_query( f.user_is_join , group=1)
async def call_user_panel(client , call ):
    status = call.data.split(':')
    print(status)
    

    if status[0] == 'date' : 
        await show_days(client , call )
    
    elif status[0] == 'get_record' : 
        await get_record(client , call )
    
    elif status[1] == 'back' :
          await show_days(client  , call)

    elif status[0] == 'get_rec_file' :
          await get_record_file(client , call )
          


async def get_record_file(client , call ):
    try :
        recorder_id = call.data.split(':')[1]
        recorder = cache.redis.hgetall(f'recorder:{recorder_id}')
        caption = f'''
    ضبط صحن علنی مجلس : `{recorder['date']}`
    ساعت شروع : `{recorder['start_time']}`
    ساعت پایان : `{recorder['end_time']}`

    @AkhbarMajles_ir
    '''
        await client.send_video(chat_id = call.from_user.id , video = recorder['file_id']  , caption = caption)
    except Exception as e :
          await alert(client , call , msg='فایلی یافت نشد !')
          print(e)






async def get_record(client , call ):
    record_date = call.data.split(':')[1].replace('/' , '-')
    records = []
    for record in cache.redis.keys('recorder:*'):
        if cache.redis.hget(record , 'date').replace('/' , '-') == record_date :
              records.append(record)


    def extract_number(item):
        return item.split(':')[1]
    sorted_items = sorted(records, key=extract_number)
    print(sorted_items)
    try :
            await client.edit_message_text(
                                        chat_id = call.from_user.id ,
                                        message_id = call.message.id ,
                                        text = text.get_record  ,
                                        reply_markup =btn.to_day_records_btn(sorted_items) ,
                                            )
    except Exception as e :
         print('hi user mother fucker ')
         print(e)


    


async def show_days(client , call):
        status = call.data.split(':')
        try :time = get_date_info(int(status[1]))
        except : time = get_date_info()
        record_keys = cache.redis.keys(f'recorder:*')
        now_records = []
        for record_date in record_keys:
            now = time['now_date'].replace('/' , '-')
            rdate = cache.redis.hget(record_date , 'date')[:-3].replace('/' , '-')
            if now == rdate:
                    now_records.append(cache.redis.hget(record_date , 'date'))
        now_records = sorted(list(set(now_records)))
        try :
                    await client.edit_message_text(
                                                chat_id = call.from_user.id ,
                                                message_id = call.message.id ,
                                                text = text.records_lists(time)  ,
                                                reply_markup =btn.parliran_lists_btn(time , now_records) ,
                                                 )
        except Exception as e :print(e)
