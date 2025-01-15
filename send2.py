import telebot
import requests
import os

# توكن البوت
BOT_TOKEN = '7195659074:AAHltAWlmetWlKLMLVrpLrBJyHbct1e2TLA'
bot = telebot.TeleBot(BOT_TOKEN)

# دالة لتحميل الملف
def download_file(url, file_name):
    response = requests.get(url, stream=True)
    with open(file_name, 'wb') as file:
        for chunk in response.iter_content(chunk_size=1024):
            file.write(chunk)
    return file_name

# دالة لمعالجة الرسائل
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    url = message.text  # الرابط الذي أرسله المستخدم
    file_name = url.split("/")[-1]  # استخراج اسم الملف من الرابط
    bot.reply_to(message, "جاري تحميل الملف...")

    try:
        file_path = download_file(url, file_name)  # تحميل الملف من الرابط
        bot.reply_to(message, "تم التحميل! جاري الإرسال...")

        with open(file_path, 'rb') as file:
            # إرسال الملف كما هو
            if file_name.endswith(".pdf") or file_name.endswith(".apk"):  # PDF أو APK
                bot.send_document(message.chat.id, file, caption="تنسيق الملف محفوظ!")
            elif file_name.endswith(".mp4") or file_name.endswith(".avi"):  # فيديو
                bot.send_video(message.chat.id, file, caption="فيديو تم تحميله!")
            else:
                bot.send_document(message.chat.id, file, caption="تم إرسال الملف!")

        os.remove(file_path)  # حذف الملف بعد الإرساله
    except Exception as e:
        bot.reply_to(message, f"حدث خطأ أثناء التحميل: {str(e)}")

# بدء البوت
bot.polling()
