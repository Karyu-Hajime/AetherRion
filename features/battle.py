from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from database import get_user_data

async def handle_battle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    telegram_id = query.from_user.id
    user_data = get_user_data(telegram_id)
    
    keyboard = [
        [InlineKeyboardButton("🔙 Quay lại", callback_data="menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    text = (
        "⚔️ **Đấu Trường Phép Thuật** ⚔️\n"
        "─────────────────\n"
        f"Chào **{user_data['username']}**! Chức năng chiến đấu đang được phát triển.\n"
        "Sắp tới, bạn sẽ có thể:\n"
        "- 🆚 Chiến đấu với quái vật.\n"
        "- 🏟️ Thách đấu bạn bè.\n"
        "- 🏆 Tham gia giải đấu.\n"
        "Hãy quay lại sau nhé! 😊"
    )
    
    await query.edit_message_text(
        text=text,
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )