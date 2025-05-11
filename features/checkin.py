from telegram import Update
from telegram.ext import ContextTypes
from database import get_user_data, update_user_data
import datetime

async def handle_checkin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    telegram_id = query.from_user.id
    user_data = get_user_data(telegram_id)
    today = datetime.date.today().isoformat()
    last_checkin = user_data.get("last_checkin", "")
    
    if last_checkin == today:
        await query.edit_message_text(
            text="📜 **Điểm Danh Hàng Ngày** 📜\n❌ Bạn đã điểm danh hôm nay rồi!\nHãy quay lại vào ngày mai! ✨\nQuay lại /menu.",
            parse_mode="Markdown"
        )
        return
    
    user_data["gold"] += 100
    user_data["last_checkin"] = today
    user_data["checkin_count"] = user_data.get("checkin_count", 0) + 1
    update_user_data(telegram_id, user_data)
    
    await query.edit_message_text(
        text="📜 **Điểm Danh Hàng Ngày** 📜\n✅ Bạn nhận được **100 vàng**! ✨\nQuay lại /menu.",
        parse_mode="Markdown"
    )