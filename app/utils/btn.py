from pyrogram.types import (ReplyKeyboardMarkup, InlineKeyboardMarkup,InlineKeyboardButton , KeyboardButton)


def join_channels_url(channels):
    persian_numbers = ['اول', 'دوم', 'سوم', 'چهارم', 'پنجم']  
    buttons = []
    for idx, channel in enumerate(channels):
        text = f"کانال {persian_numbers[idx]}"
        buttons.append([InlineKeyboardButton(text=text, url=channel)])
    buttons.append([InlineKeyboardButton(text='عضو شدم',callback_data='join:joined')])
    return InlineKeyboardMarkup(buttons)













































































