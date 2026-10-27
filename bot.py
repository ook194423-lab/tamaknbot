import os
import threading
from flask import Flask
import telebot
from openai import OpenAI

# 1. إعدادات التوكنات
TELEGRAM_TOKEN = "8877911474:AAFpbatdHsPQvLqEX0NYcc0M--okOCqLCLw"
OPENAI_API_KEY = "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"

bot = telebot.TeleBot(TELEGRAM_TOKEN)
client = OpenAI(api_key=OPENAI_API_KEY)

# 2. إعداد سيرفر Flask الوهمي (فقط لإبقاء الخدمة حية في Render)
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is alive!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port, use_reloader=False)

# 3. قاعدة المعرفة والروابط
BOT_KNOWLEDGE = """
معلومات ومصادر منصة وروابط "تمكن":
1. القناة الأساسية لتمكن: القناة الرسمية العامة للمنصة. رابط القناة: https://t.me/y1yby
2. قناة الكويزات (تمكن): مخصصة لاختبارات والكويزات التدريبية. رابط القناة: https://t.me/y6yby
3. قناة جداول قدرات (تمكن): مخصصة لجداول وتخطيط مذاكرة القدرات. رابط القناة: https://t.me/y2yby
4. قروب القدرات (تمكن): يختص بشرح تجميعات القدرات (لفظي وكمي). رابط القروب: https://t.me/y0yby
5. التحصيلي (تمكن): مواد الدراسة والمذاكرة للتحصيلي متوفرة، ولا يوجد له قروب حالياً. رابط قناة التحصيلي: https://t.me/yb7yy
6. اختبار ستيب STEP (تمكن): مواد الدراسة لقواعد اللغة الإنجليزية وقراءة النصوص. رابط قناة ستيب: https://t.me/y5yby
"""

# 4. معالجة رسائل تيليجرام
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_text = message.text
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system", 
                    "content": f"أنت مساعد رسمي لمنصة ومجموعات وقنوات 'تمكن' الدراسية. مهمتك الرد على استفسارات الطلاب وتزويدهم بالروابط الصحيحة حصرياً من هذه القائمة:\n{BOT_KNOWLEDGE}\nإذا قام شخص بالمزاح، رد عليه بأسلوب ساخر لطيف وأقترح عليه الدراسة."
                },
                {"role": "user", "content": user_text}
            ]
        )
        reply_text = response.choices[0].message.content
        bot.reply_to(message, reply_text)
    except Exception as e:
        print(f"خطأ: {e}")

if __name__ == "__main__":
    # تنظيف أي Webhook قديم عشان ما يتعارض مع الـ Polling
    try:
        bot.remove_webhook()
    except:
        pass

    # تشغيل سيرفر Flask في خلفية منفصلة
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()

    print("Bot is starting polling...")
    # تشغيل البوت بنظام الـ Polling المستمر
    bot.infinity_polling(skip_pending=True)
