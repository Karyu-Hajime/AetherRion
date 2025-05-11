from telegram import Update
from telegram.ext import ContextTypes
from database import get_user_data, read_items

async def handle_inventory(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    telegram_id = query.from_user.id
    user_data = get_user_data(telegram_id)
    items = read_items()
    inventory = user_data.get("inventory", [])
    if not inventory:
        text = "🎒 **Túi Đồ** 🎒\n❌ Túi đồ trống!\nHãy mua vật phẩm ở **Shop** hoặc quay **Gacha**! 🛒\nQuay lại /menu."
    else:
        text = (
            "🎒 **Túi Đồ** 🎒\n**Danh sách vật phẩm**:\n" +
            "\n".join([f"- **{items[item_id]['name']}** ({items[item_id]['tier']}, {items[item_id]['category']}) (ID: {item_id})"
                       for item_id in inventory]) +
            "\nQuay lại /menu."
        )
    await query.edit_message_text(
        text=text,
        parse_mode="Markdown"
    )