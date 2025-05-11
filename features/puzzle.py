from telegram import Update
from telegram.ext import ContextTypes
import random

async def handle_puzzle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    telegram_id = query.from_user.id
    riddles = [
        {"question": "Tôi không có cánh, nhưng tôi bay. Tôi không có mắt, nhưng tôi khóc. Tôi là gì?", "answer": "đám mây"},
        {"question": "Càng lấy đi càng lớn, tôi là gì?", "answer": "lỗ"}
    ]
    riddle = random.choice(riddles)
    context.user_data["current_puzzle"] = riddle
    context.user_data["awaiting_puzzle_answer"] = True
    await query.edit_message_text(
        text=f"🧩 **Giải Đố Bí Ẩn** 🧩\n**Câu đố**: {riddle['question']}\nGửi **câu trả lời** của bạn:\n(Hủy bằng /menu)",
        parse_mode="Markdown"
    )