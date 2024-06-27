from pyrogram import Client , filters
from utils.utils import  alert , get_date_info , smtp_to_date
from utils import text , btn 
from utils import filters as f
from utils import logger


@Client.on_message(filters.private & f.user_is_join ,group=1)
async def user_panel(client , message ):
    data  = get_date_info()
    await client.send_message(chat_id = message.from_user.id , text = text.records_lists(data) , reply_markup = btn.parliran_lists_btn(data))



@Client.on_callback_query( f.user_is_join , group=1)
async def call_user_panel(client , call ):
    status = call.data.split(':')

    if status[0] == 'date' : 

        time = get_date_info(int(status[1]))
        
        try :
                    await client.edit_message_text(
                                                chat_id = call.from_user.id ,
                                                message_id = call.message.id ,
                                                text = text.records_lists(time)  ,
                                                reply_markup =btn.parliran_lists_btn(time) ,
                                                 )
        except Exception as e :print(e)
