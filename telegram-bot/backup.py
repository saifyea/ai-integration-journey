from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler
from anthropic import Anthropic
from dotenv import load_dotenv
from datetime import datetime
import os

load_dotenv()

# Clients
ai_client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# 🆔 আপনার আসল Telegram User ID এখানে বসান
ADMIN_ID = 123456789 

# 🔗 আপনার ফেসবুক পেজের আসল লিংকটি এখানে দিন
FACEBOOK_PAGE_URL = "https://facebook.com"

# 🧠 গ্লোবাল ডিকশনারি - সাধারণ চ্যাট মেমোরি
chat_histories = {}

# 🔢 ConversationHandler এর স্টেপগুলোর স্টেট (States)
PRODUCT, QUANTITY, ADDRESS, PHONE, CONFIRM = range(5)

# Products info
STORE_INFO = f"""
Saif's Kids Store Products:
১. Bangladesh Map Puzzle — ৪৫০ টাকা, বয়স ৫-১২ বছর।
২. Magic Drawing Board — ৩৫০ টাকা, বয়স ৩-১০ বছর।
৩. Flash Cards — ২৫০ টাকা, বয়স ৩-৬ বছর।

Delivery: ঢাকায় ১-২ দিন, ঢাকার বাইরে ৩-৫ দিন।
"""

# 🛠️ ফেসবুক বাটন
def get_facebook_button():
    keyboard = [[InlineKeyboardButton("💬 Order on Facebook", url=FACEBOOK_PAGE_URL)]]
    return InlineKeyboardMarkup(keyboard)

# ==================== 🛒 ORDER SYSTEM (CONVERSATION) ====================

# 🎬 ১. অর্ডার শুরু (/order)
async def order_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # প্রোডাক্ট সিলেক্ট করার জন্য কীবোর্ড বাটন
    reply_keyboard = [['Bangladesh Map Puzzle', 'Magic Drawing Board', 'Flash Cards']]
    
    await update.message.reply_text(
        "🛒 আপনি সরাসরি বটের মাধ্যমেই অর্ডার করতে যাচ্ছেন।\n\n"
        "**ধাপ ১:** নিচের বাটন থেকে কোন Product-টি নিতে চান সিলেক্ট করুন (অথবা টাইপ করুন):",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True)
    )
    return PRODUCT

# 📦 ২. প্রোডাক্ট রিসিভ এবং পরিমাণ জিজ্ঞাসা
async def order_product(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['order_product'] = update.message.text
    
    # পরিমাণ সিলেক্ট করার বাটন
    reply_keyboard = [['১ টি', '২ টি', '৩ টি']]
    
    await update.message.reply_text(
        f"✅ প্রোডাক্ট: {update.message.text}\n\n"
        f"**ধাপ ২:** আপনি কতটি (Quantity) নিতে চান সিলেক্ট করুন বা লিখে জানান:",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True)
    )
    return QUANTITY

# 🔢 ৩. পরিমাণ রিসিভ এবং ঠিকানা জিজ্ঞাসা
async def order_quantity(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['order_qty'] = update.message.text
    
    await update.message.reply_text(
        "**ধাপ ৩:** আপনার সম্পূর্ণ ঠিকানা (Full Address) লিখে দিন:\n"
        "उदाहरण: হাউস# ১২, রোড# ৫, ধানমন্ডি, ঢাকা।",
        reply_markup=ReplyKeyboardRemove() # কীবোর্ড বাটন সরিয়ে ফেলার জন্য
    )
    return ADDRESS

# 📍 ৪. ঠিকানা রিসিভ এবং ফোন নম্বর জিজ্ঞাসা
async def order_address(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['order_address'] = update.message.text
    
    await update.message.reply_text(
        "**ধাপ ৪:** আপনার সচল মোবাইল নম্বরটি (Phone Number) দিন:"
    )
    return PHONE

# 📱 ৫. ফোন নম্বর রিসিভ এবং সামারি দেখানো
async def order_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['order_phone'] = update.message.text
    
    # কনফার্মেশন বাটন
    reply_keyboard = [['হ্যাঁ, কনফার্ম করছি', 'অর্ডার বাতিল করুন']]
    
    summary = (
        f"📝 **Order Summary (অর্ডারের বিবরণ):**\n"
        f"━━━━━━━━━━━━━━━━━━━\n"
        f"📦 Product: {context.user_data['order_product']}\n"
        f"🔢 Quantity: {context.user_data['order_qty']}\n"
        f"📍 Address: {context.user_data['order_address']}\n"
        f"📱 Phone: {context.user_data['order_phone']}\n"
        f"━━━━━━━━━━━━━━━━━━━\n\n"
        f"সব তথ্য কি ঠিক আছে? অর্ডারটি কনফার্ম করতে নিচের বাটনে ক্লিক করুন:"
    )
    
    await update.message.reply_text(
        summary,
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True)
    )
    return CONFIRM

# 🏁 ৬. ফাইনাল কনফার্মেশন ও অ্যাডমিন নোটিফিকেশন
async def order_confirm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_choice = update.message.text
    user_name = update.effective_user.first_name
    user_id = update.effective_user.id
    current_time = datetime.now().strftime("%I:%M %p")
    
    if user_choice == 'হ্যাঁ, কনফার্ম করছি':
        # ১. কাস্টমারকে থ্যাঙ্ক ইউ মেসেজ
        await update.message.reply_text(
            "🎉 আলহামদুলিল্লাহ্! আপনার অর্ডারটি সফলভাবে গ্রহণ করা হয়েছে।\n\n"
            "আমাদের প্রতিনিধি খুব দ্রুত আপনার সাথে যোগাযোগ করবেন। আমাদের সাথে থাকার জন্য ধন্যবাদ! 😊",
            reply_markup=ReplyKeyboardRemove()
        )
        
        # ২. অ্যাডমিনকে সম্পূর্ণ অর্ডারের নোটিফিকেশন পাঠানো
        admin_notification = (
            f"🚀 **New Order Placed!**\n"
            f"━━━━━━━━━━━━━━━━━━━\n"
            f"👤 Customer: {user_name} (ID: {user_id})\n"
            f"📦 Product: {context.user_data['order_product']}\n"
            f"🔢 Qty: {context.user_data['order_qty']}\n"
            f"📍 Address: {context.user_data['order_address']}\n"
            f"📱 Phone: {context.user_data['order_phone']}\n"
            f"⏰ Time: {current_time}\n"
            f"━━━━━━━━━━━━━━━━━━━"
        )
        
        try:
            await context.bot.send_message(chat_id=ADMIN_ID, text=admin_notification)
        except Exception as admin_err:
            print(f"Admin Order Notification Error: {admin_err}")
            
    else:
        await update.message.reply_text(
            "❌ অর্ডারটি বাতিল করা হয়েছে। নতুন করে অর্ডার করতে আবার /order লিখুন।",
            reply_markup=ReplyKeyboardRemove()
        )
        
    return ConversationHandler.END

# 🚫 অর্ডার চলাকালীন কাস্টমার চাইলে বাতিল করতে পারবে
async def order_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🚫 অর্ডার প্রক্রিয়াটি বাতিল করা হয়েছে।", 
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END

# ========================================================================

# ✅ /start command
async def start(update:Update, context:ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_name = update.effective_user.first_name
    chat_histories[user_id] = []
    
    await update.message.reply_text(
        f"🛍️ আস্সালামু আলাইকুম {user_name}!\n\n"
        f"আমি Saif's Kids Store এর AI Assistant।\n\n"
        f"অর্ডার করতে সরাসরি টাইপ করুন: /order\n\n"
        f"অন্যান্য Commands:\n"
        f"/products — সব products দেখুন\n"
        f"/price — product এর দাম\n"
        f"/delivery — Delivery এর সময়\n"
        f"/clear — চ্যাট মেমোরি মুছুন"
    )

# ✅ /products command
async def products(update:Update,context:ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🛍️ আমাদের Products:\n\n"
        "1️⃣ Bangladesh Map Puzzle | 💰 ৪৫০ টাকা\n"
        "2️⃣ Magic Drawing Board | 💰 ৩৫০ টাকা\n"
        "3️⃣ Flash Cards | 💰 ২৫০ টাকা\n\n"
        "🛒 বটের মাধ্যমে অর্ডার করতে লিখুন: /order",
        reply_markup=get_facebook_button()
    )

# ✅ AI Message Handler (সাধারণ চ্যাটের জন্য)
async def handle_message(update:Update, context:ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    user_id = update.effective_user.id

    if user_id not in chat_histories:
        chat_histories[user_id] = []

    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    chat_histories[user_id].append({"role": "user", "content": user_message})

    if len(chat_histories[user_id]) > 10:
        chat_histories[user_id] = chat_histories[user_id][-10:]

    try:
        response = ai_client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=300,
            system=f"তুমি Saif's Kids Store এর AI Assistant। বাংলায় উত্তর দাও। কাস্টমার অর্ডার করতে চাইলে তাকে সরাসরি /order কমান্ডটি ব্যবহার করতে বলো।\n\nStore Info:\n{STORE_INFO}",
            messages=chat_histories[user_id]
        )
        ai_response = response.content.text
        chat_histories[user_id].append({"role": "assistant", "content": ai_response})
        await update.message.reply_text(ai_response, reply_markup=get_facebook_button())
    except Exception as e:
        await update.message.reply_text("❌ দুঃখিত, সমস্যা হয়েছে। আবার চেষ্টা করুন।")
        print(f"Error:{e}")
    
# Main Function
def main():
    print("🤖 Telegram Bot চালু হচ্ছে...")
    app = Application.builder().token(BOT_TOKEN).build()

    # 🛒 Order System Conversation Handler রেজিস্ট্রেশন
    order_handler = ConversationHandler(
        entry_points=[CommandHandler("order", order_start)],
        states={
            PRODUCT: [MessageHandler(filters.TEXT & ~filters.COMMAND, order_product)],
            QUANTITY: [MessageHandler(filters.TEXT & ~filters.COMMAND, order_quantity)],
            ADDRESS: [MessageHandler(filters.TEXT & ~filters.COMMAND, order_address)],
            PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, order_phone)],
            CONFIRM: [MessageHandler(filters.TEXT & ~filters.COMMAND, order_confirm)],
        },
        fallbacks=[CommandHandler("cancel", order_cancel)],
    )
    
    app.add_handler(order_handler) # অর্ডার হ্যান্ডলারটি সবার আগে যুক্ত করতে হবে
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("products", products))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("✅ Bot চালু! Telegram এ test করো।")
    app.run_polling()

if __name__ == '__main__':
    main()
