from telegram import Update
from telegram.ext import ContextTypes
from database import get_user_data, update_user_data

async def handle_quest(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    telegram_id = query.from_user.id
    user_data = get_user_data(telegram_id)
    quests = user_data.get("quests", [])
    if not quests:
        user_data["quests"] = [{"title": "Săn 5 quái vật", "progress": 0, "total": 5, "reward": 300}]
        update_user_data(telegram_id, user_data)
        quests = user_data["quests"]
    
    text = "📋 **Nhiệm Vụ** 📋\n**Danh sách nhiệm vụ**:\n" + "\n".join([f"- **{q['title']}** ({q['progress']}/{q['total']})" for q in quests]) + "\nQuay lại /menu."
    await query.edit_message_text(
        text=text,
        parse_mode="Markdown"
    )