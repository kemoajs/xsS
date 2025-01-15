import telebot
import requests
import os

# أدخل التوكن الخاص بالبوت
BOT_TOKEN = "7195659074:AAHltAWlmetWlKLMLVrpLrBJyHbct1e2TLA"
bot = telebot.TeleBot(BOT_TOKEN)

# دالة لتحميل الملف
def download_file(url, file_name):
    response = requests.get(url, stream=True)
    with open(file_name, 'wb') as file:
        for chunk in response.iter_content(chunk_size=1024):
            file.write(chunk)
    return file_name

# أمر /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "أرسل رابط التحميل، وسأقوم بتنزيل الملف وإرساله إليك.")

# معالجة الرسائل النصية (الروابط)
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    url = message.text
    file_name = url.split("/")[-1]  # استخراج اسم الملف من الرابط
    bot.reply_to(message, "جاري تحميل الملف...")
    try:
        file_path = download_file(url, file_name)
        bot.reply_to(message, "تم التحميل! جاري الإرسال...")
        with open(file_path, 'rb') as file:
            bot.send_document(message.chat.id, file)
        os.remove(file_path)  # حذف الملف بعد الإرسال
    except Exception as e:
        bot.reply_to(message, f"حدث خطأ أثناء التحميل: {str(e)}")

# تشغيل البوت
bot.polling()
