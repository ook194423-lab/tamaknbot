import os
from flask import Flask
from threading import Thread
import telebot
from openai import OpenAI

# 1. إعدادات الاتصال والتوكنات
TELEGRAM_TOKEN = "8617730400:AAHUA-1e7Cay2w51x6hbrtZEeSQ50-YarmU"
OPENAI_API_KEY = "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"

bot = telebot.TeleBot(TELEGRAM_TOKEN)
client = OpenAI(api_key=OPENAI_API_KEY)

# 2. سيرفر Flask الوهمي لإرضاء بورتات Render المجانية
app = Flask('')

@app.route('/')
def home():
    return "Bot is alive!"

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

# 3. قاعدة المعرفة والروابط الرسمية لمنصة "تمكن"
BOT_KNOWLEDGE = """
معلومات ومصادر منصة وروابط "تمكن":
1. القناة الأساسية لتمكن: القناة الرسمية العامة للمنصة. رابط القناة: https://t.me/y1yby
2. قناة الكويزات (تمكن): مخصصة لاختبارات والكويزات التدريبية. رابط القناة: https://t.me/y6yby
3. قناة جداول قدرات (تمكن): مخصصة لجداول وتخطيط مذاكرة القدرات. رابط القناة: https://t.me/y2yby
4. قروب القدرات (تمكن): يختص بشرح تجميعات القدرات (لفظي وكمي). رابط القروب: https://t.me/y0yby
5. التحصيلي (تمكن): مواد الدراسة والمذاكرة للتحصيلي متوفرة، ولا يوجد له قروب حالياً. رابط قناة التحصيلي: https://t.me/yb7yy
6. اختبار ستيب STEP (تمكن): مواد الدراسة لقواعد اللغة الإنجليزية وقراءة النصوص. رابط قناة ستيب: https://t.me/y5yby
7. التعليمات: إذا سأل الطالب عن أي رابط يخص "تمكن" (مثل القناة الأساسية، الكويزات، الجداول، القدرات، التحصيلي، أو ستيب)، قم بإعطائه الرابط الصحيح والمخصص له من هذه القائمة مباشرة وبكل وضوح. ممنوع تأليف روابط خارجية.
"""

# 4. معالجة رسائل تيليجرام والذكاء الاصطناعي
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_text = message.text
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system", 
                    "content": f"أنت مساعد رسمي لمنصة ومجموعات وقنوات 'تمكن' الدراسية. مهمتك هي الرد على استفسارات الطلاب وتزويدهم بالروابط الصحيحة والدقيقة الخاصة بكل قسم أو قناة بناءً على طلبهم ومستعيناً حصرياً بالمعلومات الموجودة في الأسفل. يمنع منعاً باتاً تأليف أي روابط غير موجودة هنا. إذا سأل عن شيء غير متوفر، اعتذر بلطف. اذا قام شخص بقول أشياء للمزاح أو اللعب، رد عليه بأسلوب ساخر لطيف واقترح عليه أن يذهب للدراسة ويسيب عنه العيارة.\n\nالمعلومات المعتمدة:\n{BOT_KNOWLEDGE}"
                },
                {"role": "user", "content": user_text}
            ]
        )
        
        reply_text = response.choices[0].message.content
        bot.reply_to(message, reply_text)
        
    except Exception as e:
        print(f"صار خطأ: {e}")

# 5. تشغيل السيرفر والبوت معاً بشكل نظيف وآمن
if __name__ == "__main__":
    keep_alive()
    bot.infinity_polling()
