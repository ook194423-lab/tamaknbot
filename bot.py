import telebot
from openai import OpenAI

# ضع هنا التوكن اللي أخذته من BotFather
TELEGRAM_TOKEN = "8617730400:AAHUA-1e7Cay2w51x6hbrtZEeSQ50-YarmU"
# ضع هنا مفتاح الـ API الخاص بـ OpenAI (أو النموذج اللي تفضله)
OPENAI_API_KEY = "8617730400:AAHUA-1e7Cay2w51x6hbrtZEeSQ50-YarmU"

bot = telebot.TeleBot(TELEGRAM_TOKEN)
client = OpenAI(api_key=OPENAI_API_KEY)

# دالة للرد على أي رسالة يرسلها خويك في الخاص أو القروب
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_text = message.text
    
    # رسالة مؤقتة أو تفكير (اختياري)
    print(f"رسالة جديدة من المستخدم: {user_text}")

    try:
        # إرسال النص إلى الذكاء الاصطناعي ليولد رداً ذكياً وطبيعياً
        response = client.chat.completions.create(
            model="gpt-4o-mini", # أو أي نموذج مناسب وسريع
            messages=[
                {"role": "system", "content": "انت مساعد ذكي وودود، ترد بطريقة طبيعية وكأنك شخص حقيقي في مجموعة أصدقاء."},
                {"role": "user", "content": user_text}
            ]
        )
        
        reply_text = response.choices[0].message.content
        
        # إرسال الرد لنفس المحادثة (خاص أو قروب)
        bot.reply_to(message, reply_text)
        
    except Exception as e:
        print(f"صار خطأ: {e}")

# تشغيل البوت باستمرار
print("البوت شغال الآن...")
bot.infinity_polling()
