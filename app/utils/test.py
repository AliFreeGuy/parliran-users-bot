import arabic_reshaper
from bidi.algorithm import get_display

def convert_text_to_persian(text):
    # تابعی برای تبدیل اعداد انگلیسی به اعداد فارسی
    def convert_numbers_to_persian(text):
        english_to_persian = str.maketrans("0123456789", "۰۱۲۳۴۵۶۷۸۹")
        return text.translate(english_to_persian)
    
    # تبدیل اعداد انگلیسی به اعداد فارسی در متن
    persian_text = convert_numbers_to_persian(text)
    
    # تبدیل متن به شکلی که به درستی در متن‌های راست به چپ نمایش داده شود
    reshaped_text = arabic_reshaper.reshape(persian_text)
    bidi_text = get_display(reshaped_text)
    
    return bidi_text

