from pyrogram import Client , filters
from utils import cache
from config import CHANNEL1 , CHANNEL2
from utils.utils import join_checker , alert
from utils import text , btn
from utils import filters as f
from utils import logger








@Client.on_message(filters.private & f.user_not_join , group=0)
async def user_not_join(client , message ):
      channels = [CHANNEL1 , CHANNEL2]
      not_join_channels = await join_checker(client , message ,channels)
      if not_join_channels :
            await client.send_message(message.from_user.id   , text = text.user_not_join  , reply_markup = btn.join_channels_url(not_join_channels))








@Client.on_callback_query( group=0)
async def callback_query_handler(client , call ):
    router = call.data.split(':')[0]
    if router == 'join' :await joined_handler(client , call )




async def joined_handler(client , call ):
        channels = [CHANNEL1 , CHANNEL2]
        not_join_channels = await join_checker(client , call ,channels)
        if not_join_channels :
            try :
                    await client.edit_message_text(
                                                chat_id = call.from_user.id ,
                                                message_id = call.message.id ,
                                                text = text.user_not_join  ,
                                                reply_markup =btn.join_channels_url(not_join_channels) ,
                                                 )
            except Exception as e :print(e)
            await alert(client , call , 'هنوز که تو کانالا جوین نشدی !')
            logger.info(f'user not join channel : {str(call.from_user.id)}')
        else :
            await client.delete_messages(call.from_user.id , call.message.id)
            await client.send_message(call.from_user.id , text = text.start_text)
            logger.info(f'user is join channel : {str(call.from_user.id)}')

