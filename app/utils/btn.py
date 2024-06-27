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


def parliran_lists_btn(data , now_records):
    
    buttons = []
    

    for i in range(0, len(now_records), 3):
        row = []
        row.append(InlineKeyboardButton(text=now_records[i], callback_data=f'get_record:{now_records[i]}'))
        if i + 1 < len(now_records):
            row.append(InlineKeyboardButton(text=now_records[i + 1], callback_data=f'get_record:{now_records[i + 1]}'))
        if i + 2 < len(now_records):
            row.append(InlineKeyboardButton(text=now_records[i + 2], callback_data=f'get_record:{now_records[i + 2]}'))
        buttons.append(row)

    buttons.append([
        InlineKeyboardButton(text='◀️',callback_data=f'date:{data["before_smtp"]}'),
        InlineKeyboardButton(text=data['now_date'],callback_data=f'date:{data["now_smtp"]}'),
        InlineKeyboardButton(text='▶️',callback_data=f'date:{data["after_smtp"]}'),
        ])
    return InlineKeyboardMarkup(buttons)
    




def to_day_records_btn(records):
        
    buttons = []
    persian_numbers = ['اول', 'دوم', 'سوم', 'چهارم', 'پنجم']  
    buttons = []
    for idx, record in enumerate(records):
        print(record)
        text = f"دریافت نوبت {persian_numbers[idx]}"
        buttons.append([InlineKeyboardButton(text=text, callback_data=f'get_rec_file:{record.replace("recorder:" , "")}')])

    buttons.append([
        InlineKeyboardButton(text='🔙',callback_data=f'to_day_record:back'),
        ])
    return InlineKeyboardMarkup(buttons)
    










































































