from pyrogram.types import (ReplyKeyboardMarkup, InlineKeyboardMarkup,InlineKeyboardButton , KeyboardButton)
import jdatetime

def join_channels_url(channels):
    persian_numbers = ['اول', 'دوم', 'سوم', 'چهارم', 'پنجم']  
    buttons = []
    for idx, channel in enumerate(channels):
        text = f"کانال {persian_numbers[idx]}"
        buttons.append([InlineKeyboardButton(text=text, url=channel)])
    buttons.append([InlineKeyboardButton(text='عضو شدم',callback_data='join:joined')])
    return InlineKeyboardMarkup(buttons)


def parliran_lists_btn(data):
    
    buttons = []
    buttons.append([
        InlineKeyboardButton(text='◀️',callback_data=f'date:{data["before_smtp"]}'),
        InlineKeyboardButton(text=data['now_date'],callback_data=f'date:{data["now_smtp"]}'),
        InlineKeyboardButton(text='▶️',callback_data=f'date:{data["after_smtp"]}'),
        ])
    return InlineKeyboardMarkup(buttons)
    





# def parliran_records():

#     # دریافت تاریخ امروز
#     today = jdatetime.date.today()
#     print(today)
#     # استخراج سال و ماه
#     year = today.year
#     month = today.month

#     print(f"تاریخ امروز: {year}-{month:02}")










































































