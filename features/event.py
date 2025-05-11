from telegram import Update
from telegram.ext import ContextTypes

async def handle_event(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    text = (
        "🎉 **Sự Kiện Đặc Biệt** 🎉\n"
        "─────────────────\n"
        "- 🐉 **Săn Rồng Huyền Thoại**: Đối mặt với rồng cổ đại!\n"
        "- ✨ **Lễ Hội Phép Thuật**: Nhận thưởng độc quyền!\n"
        "─────────────────\n"
        "Tham gia sự kiện để nhận phần thưởng! (Chưa khả dụng)\nQuay lại /menu."
    )
    await query.edit_message_text(
        text=text,
        parse_mode="Markdown"
    )