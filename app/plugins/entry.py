from pyrogram import Client , filters
from utils import cache



@Client.on_message(filters.private ,group=0)
async def user_entry_manager(client , message ):
    cache.redis.hmset(f'majles-user:{str(message.from_user.id)}' , {'name' : message.from_user.first_name , 'chat_id' : message.from_user.id})
    print(cache.redis.hgetall(f'majles-user:{str(message.from_user.id)}'))