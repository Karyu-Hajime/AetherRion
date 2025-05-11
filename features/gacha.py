from telegram import Update
from telegram.ext import ContextTypes
from database import get_user_data, update_user_data, read_items
import random

async def handle_gacha(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    telegram_id = query.from_user.id
    user_data = get_user_data(telegram_id)
    items = read_items()
    
    if user_data["gold"] < 200:
        await query.edit_message_text(
            text="🎰 **Gacha May Mắn** 🎰\n❌ Bạn cần **200 vàng** để quay!\nHãy kiếm thêm vàng! 💰\nQuay lại /menu.",
            parse_mode="Markdown"
        )
        return
    
    user_data["gold"] -= 200
    rewards = [item_id for item_id, item in items.items() if item["tier"] in ["sơ cấp", "trung cấp"]]
    reward_id = random.choice(rewards)
    user_data["inventory"].append(reward_id)
    update_user_data(telegram_id, user_data)
    
    await query.edit_message_text(
        text=f"🎰 **Gacha May Mắn** 🎰\n✅ Bạn nhận được **{items[reward_id]['name']}** (ID: {reward_id})! 🎉\nQuay lại /menu.",
        parse_mode="Markdown"
    )