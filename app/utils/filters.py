from pyrogram import filters
from utils.utils import join_checker
from config import CHANNEL1  , CHANNEL2
    

async def user_is_join(_ , cli , msg ):
        
        channels = [CHANNEL2 ,CHANNEL1 ]
        is_join = await join_checker(cli , msg , channels)
        if not is_join : return True
        else :return False



async def user_not_join(_ , cli , msg ):
        channels = [CHANNEL2 ,CHANNEL1 ]
        is_join = await join_checker(cli , msg , channels)
        if not is_join : return False
        else :return True


user_not_join=filters.create(user_not_join)
user_is_join = filters.create(user_is_join)

