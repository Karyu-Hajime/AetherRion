from telegram import Update
from telegram.ext import ContextTypes

async def handle_map(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    text = (
        "🗺️ **Bản Đồ Phiêu Lưu** 🗺️\n"
        "─────────────────\n"
        "- 🌲 **Rừng Huyền Bí**: Nơi ẩn chứa kho báu!\n"
        "- 🌋 **Núi Lửa Rực Cháy**: Thử thách khắc nghiệt!\n"
        "- 🏰 **Thành Phố Phép Thuật**: Trung tâm giao thương!\n"
        "─────────────────\n"
        "Chọn khu vực để khám phá! (Chưa khả dụng)\nQuay lại /menu."
    )
    await query.edit_message_text(
        text=text,
        parse_mode="Markdown"
    )