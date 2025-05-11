from telegram import Update
from telegram.ext import ContextTypes
from database import get_user_data

async def handle_pet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    telegram_id = query.from_user.id
    user_data = get_user_data(telegram_id)
    pets = user_data.get("pets", [])
    if not pets:
        text = "🐾 **Thú Cưng** 🐾\n❌ Bạn chưa có thú cưng nào!\nHãy đến **Shop** để nhận nuôi một người bạn đồng hành! 🐉\nQuay lại /menu."
    else:
        text = "🐾 **Thú Cưng** 🐾\n**Danh sách thú cưng**:\n" + "\n".join([f"- **{pet['name']}** (Sức mạnh: {pet['power']})" for pet in pets]) + "\nQuay lại /menu."
    await query.edit_message_text(
        text=text,
        parse_mode="Markdown"
    )