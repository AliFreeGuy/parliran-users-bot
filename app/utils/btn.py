from pyrogram.types import (ReplyKeyboardMarkup, InlineKeyboardMarkup,InlineKeyboardButton , KeyboardButton)
import jdatetime
from utils.utils import convert_numbers_to_persian





def join_channels_url(channels):
    persian_numbers = ['اول', 'دوم', 'سوم', 'چهارم', 'پنجم']  
    buttons = []
    for idx, channel in enumerate(channels):
        text = f"کانال {persian_numbers[idx]}"
        buttons.append([InlineKeyboardButton(text=text, url=channel)])
    buttons.append([InlineKeyboardButton(text='عضو شدم',callback_data='join:joined')])
    return InlineKeyboardMarkup(buttons)


def parliran_lists_btn(data, now_records):
    print(now_records)
    
    # دیکشنری تبدیل اعداد ماه به نام‌های فارسی
    months = {
        '01': 'فروردین',
        '02': 'اردیبهشت',
        '03': 'خرداد',
        '04': 'تیر',
        '05': 'مرداد',
        '06': 'شهریور',
        '07': 'مهر',
        '08': 'آبان',
        '09': 'آذر',
        '10': 'دی',
        '11': 'بهمن',
        '12': 'اسفند'
    }
    
    # تفکیک سال و ماه از تاریخ فعلی
    year, month = data['now_date'].split('-')
    persian_month = months.get(month, month)
    persian_date = f"🗓 {year} {persian_month}"
    
    # لیست برای دکمه‌ها
    buttons = []
    
    # دکمه‌های تغییر ماه
    buttons.append([
        InlineKeyboardButton(text='ماه قبل 👈', callback_data=f'date:{data["before_smtp"]}'),
        InlineKeyboardButton(text=convert_numbers_to_persian(persian_date), callback_data=f'date:{data["now_smtp"]}'),
        InlineKeyboardButton(text='👉 ماه بعد ', callback_data=f'date:{data["after_smtp"]}'),
    ])
    
    # تقسیم رکوردها به ردیف‌های سه‌تایی
    for i in range(0, len(now_records), 3):
        row = []
        for j in range(i, min(i + 3, len(now_records))):
            record = now_records[j]
            formatted_record = f'🎥 {convert_numbers_to_persian(record).replace("-", "/")}'
            row.append(InlineKeyboardButton(text=formatted_record, callback_data=f'get_record:{record}'))
        buttons.append(row)
    
    return InlineKeyboardMarkup(buttons)


def to_day_records_btn(records):
    buttons = []
    persian_numbers = ['اول', 'دوم', 'سوم', 'چهارم', 'پنجم' , 'ششم' , 'هفتم' , 'هشتم' , 'نهم' , 'دهم' , 'یازدهم' , 'دوازدهم' , 'سیزدهم' , 'چهاردهم' , 'پانزدهم']  
    buttons = []
    for idx, record in enumerate(records):
        print(record)
        text = f"📥 دریافت نوبت {persian_numbers[idx]}"
        buttons.append([InlineKeyboardButton(text=text, callback_data=f'get_rec_file:{record.replace("recorder:" , "")}')])

    buttons.append([
        InlineKeyboardButton(text='🔙',callback_data=f'to_day_record:back'),
        ])
    return InlineKeyboardMarkup(buttons)
    










































































